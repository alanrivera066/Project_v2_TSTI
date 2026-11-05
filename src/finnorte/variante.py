"""TU SISTEMA: el motor de la variante de tu equipo.

Contrato mínimo (lo usa `python -m finnorte evaluar ... --sistema finnorte.variante:sistema`,
la API de la semana 4 y la interfaz de la semana 5):

    sistema(entrada: dict) -> dict con
        respuesta: str        el artefacto final en texto (casos, hallazgos, respuesta, README, triage)
        fuentes: list[str]    ids de fragmentos/documentos del corpus que respaldan la salida
        abstuvo: bool         True si la entrada está fuera de alcance o no hay contexto suficiente
        errores_citas: list   salida de controles.verificar_citas
        artefacto: dict       (opcional) la salida estructurada (JSON) de tu última etapa
        costo_usd, latencia_ms

Construye esto por incrementos:
  A1  → INDICE con el corpus de tu variante (corpus/<variante>/) y búsqueda semántica
  A2  → FLUJO de 3 etapas publicadas con prompts versionados en prompts/ y esquemas en prompts/esquemas/
  Av1 → RAG (contexto en el prompt) + controles + evaluación contra tu contrato de calidad
"""
from __future__ import annotations

import time
import ast
import json
import re
from functools import partial
from dataclasses import replace
from pathlib import Path

from . import controles
from .config import RAIZ
from .pipeline import Etapa, Pipeline
from .retrieval import Indice, contexto_para_prompt, cargar_corpus, fragmentar
from . import pii, trazas
from .config import config as config_runtime
from .reglas import (FlujoRevisor, validar_detectar,
                     validar_explicar, validar_parche)

VARIANTE = "v2-revisor"
_INDICE: Indice | None = None


def indice() -> Indice:
    global _INDICE
    if _INDICE is None:
        # Exclusión mínima AV1 antes de embeddings y del prompt, también en C.
        docs = [d for d in cargar_corpus(RAIZ / "corpus" / VARIANTE)
                if d.id != "sec-11" and d.meta.get("clasificacion") != "confidencial"]
        _INDICE = Indice([f for d in docs for f in fragmentar(d)])
    return _INDICE


def leer_entrada(entrada: dict) -> str:
    """Normaliza la entrada de los casos de evaluación a texto."""
    if "archivo" in entrada:
        return (RAIZ / entrada["archivo"]).read_text(encoding="utf-8")
    for clave in ("requisito", "codigo", "pregunta", "log"):
        if clave in entrada:
            return str(entrada[clave])
    raise ValueError(f"Entrada sin campo reconocido: {list(entrada)}")


def crear_flujo(version=None):
    return FlujoRevisor([
        Etapa("detectar", "rev_detectar", version=version, validar=validar_detectar),  # Luis: ligada al original
        Etapa("explicar", "rev_explicar", version=version, usa=["detectar"], validar=validar_explicar),  # Alan
        Etapa("parche", "rev_parche", version=version, usa=["explicar"], validar=validar_parche),  # Cesar
    ], nombre=VARIANTE)


FLUJO = crear_flujo()
for e in FLUJO.etapas:
    e.version = {"detectar": 3, "explicar": 4, "parche": 4}[e.nombre]
FLUJO_V1 = crear_flujo(version=1)

# Configuración del motor. guia/av1_configuraciones.py la cambia para medir A, B, C y D.
CONFIG_POR_DEFECTO = {
    "version_prompt": 2,   # 1 o 2: qué versión de prompts usa el flujo
    "usar_rag": True,      # recuperar contexto del corpus de la variante (A1)
    "controles": True,     # abstención, filtrado de confidenciales, citas verificadas, saneo
    "k": 6,                # fragmentos a recuperar
    "umbral": 0.35,        # similitud mínima para no abstenerse (ajústalo con tus datos)
}


def armar_salida(t0: float, respuesta: str, fuentes: list[str], abstuvo: bool,
                 errores_citas: list[str] | None = None, artefacto: dict | None = None, costo_usd: float = 0.0) -> dict:
    """Arma el dict que esperan la evaluación, la API (S4) y la interfaz (S5)."""
    return {"respuesta": respuesta, "fuentes": fuentes, "abstuvo": abstuvo, "errores_citas": errores_citas or [],
            "artefacto": artefacto or {}, "costo_usd": costo_usd,
            "latencia_ms": round((time.perf_counter() - t0) * 1000, 1)}


def consulta_codigo(texto):
    """Consulta sin comentarios ni valores literales; no expone credenciales al embedder."""
    try:
        arbol = ast.parse(texto)
    except SyntaxError:
        return "revisión de seguridad de código Python", False
    valido = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                    ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Call, ast.Import,
                    ast.ImportFrom, ast.For, ast.If, ast.With)) for n in ast.walk(arbol))
    nombres = sorted({n.id for n in ast.walk(arbol) if isinstance(n, ast.Name)} |
                     {n.attr for n in ast.walk(arbol) if isinstance(n, ast.Attribute)})
    temas = []
    pistas = [(r'key|password|secret', 'secretos credenciales variables de entorno'),
              (r'execute|cursor|sql', 'SQL consultas parametrizadas'),
              (r'print|log|info', 'registros sin datos personales enmascarar'),
              (r'float|saldo|monto|comision', 'dinero Decimal precisión monetaria'),
              (r'eval|pickle|subprocess|shell', 'deserialización segura comandos externos'),
              (r'token|md5|random|hmac', 'criptografía secrets compare_digest'),
              (r'requests|raise|except', 'manejo de errores timeout'),
              (r'cuenta|usuario|user', 'autorización a nivel recurso')]
    for patron, tema in pistas:
        if re.search(patron, ' '.join(nombres), re.I): temas.append(tema)
    return 'Revisar código Python según reglas internas de seguridad. ' + '; '.join(temas) + '. ' + ' '.join(nombres)[:500], valido


def sanear_av1(valor):
    """Saneo mínimo de salida. No reemplaza los controles completos de AV2."""
    if isinstance(valor, dict): return {k: sanear_av1(v) for k, v in valor.items()}
    if isinstance(valor, list): return [sanear_av1(v) for v in valor]
    if not isinstance(valor, str): return valor
    valor = re.sub(r'\b(?:sk_live_|fn_live_)[A-Za-z0-9_-]+', '[SECRETO]', valor)
    for _, literal in sorted(pii.detectar(valor), key=lambda x: len(x[1]), reverse=True):
        valor = valor.replace(literal, '[DATO OCULTO]')
    return valor


def sistema(entrada: dict, config: dict | None = None) -> dict:
    cfg = {**CONFIG_POR_DEFECTO, **(config or {})}
    if cfg['version_prompt'] not in (1, 2): raise ValueError('version_prompt debe ser 1 o 2')
    if cfg['k'] < 1: raise ValueError('k debe ser positivo')
    t0 = time.perf_counter()
    texto = leer_entrada(entrada)
    consulta, es_python = consulta_codigo(texto)
    recuperados = indice().buscar(consulta, k=cfg['k']) if cfg['usar_rag'] else []
    def cerrar(respuesta, fuentes=None, abstuvo=False, errores=None, artefacto=None, costo=0):
        out = armar_salida(t0, respuesta, fuentes or [], abstuvo, errores, artefacto, costo)
        if cfg['controles']:
            out['respuesta'] = sanear_av1(out['respuesta'])
            out['artefacto'] = sanear_av1(out['artefacto'])
        out['demo'] = config_runtime().llm_proveedor == 'fake' or config_runtime().emb_proveedor == 'hash'
        out['alcance'] = 'Tres etapas: detectar, explicar y parche'
        out['recuperados'] = [r.fragmento.id for r in recuperados]
        trazas.registrar('av1_respuesta', config=cfg, consulta=consulta, **out)
        return out
    insuficiente = controles.debe_abstenerse(recuperados, cfg['umbral']) if cfg['usar_rag'] else True
    # Python válido se revisa aunque su semejanza sea baja: limpio no significa fuera de dominio.
    if cfg['controles'] and not es_python:
        motivo = 'Contexto insuficiente. ' if insuficiente else ''
        return cerrar(motivo + 'Esta herramienta revisa archivos Python. Proporciona código Python válido.', abstuvo=True)
    versiones = {'detectar': 1, 'explicar': 1, 'parche': 1} if cfg['version_prompt']==1 else {'detectar': 4, 'explicar': 5, 'parche': 5}
    validadores = {'detectar': partial(validar_detectar, codigo=texto), 'explicar': validar_explicar,
                   'parche': partial(validar_parche, codigo=texto)}
    etapas = [Etapa(n, 'rev_'+n, version=v, usa=[] if n=='detectar' else ['detectar' if n=='explicar' else 'explicar'],
                    validar=validadores[n] if cfg['controles'] else None) for n,v in versiones.items()]
    from .reglas import registros_del_codigo
    valores = {'entrada': 'Solicitud de revisión: ' + str(entrada.get('solicitud','Revisar el archivo Python')) + '\nCódigo numerado:\n' + '\n'.join(f'{i}: {l}' for i,l in enumerate(texto.splitlines(),1)),
               'codigo_original': texto, 'codigo_original_json': json.dumps(texto, ensure_ascii=False),
               'senales_codigo': json.dumps([{'regla':'SEC-03','linea':r['inicio']} for r in registros_del_codigo(texto) if r['sensible']]),
               'contexto': contexto_para_prompt(recuperados, max_chars=12000) or '(sin contexto)'}
    r = Pipeline(etapas, nombre='av1-'+VARIANTE).ejecutar(valores)
    if not r.ok:
        return cerrar('No fue posible validar la revisión. Se requiere revisión humana.', abstuvo=True,
                      errores=[e for etapa in r.etapas for e in etapa.errores], costo=r.costo_usd)
    hallazgos = r.salidas['explicar']['hallazgos']
    fuentes = sorted({h.get('fuente','') for h in hallazgos if h.get('fuente')})
    errores = controles.verificar_citas(fuentes, recuperados) if hallazgos else []
    for h in hallazgos:
        f = h.get('fuente','').removeprefix('doc:').split('#')[0]
        if cfg['usar_rag'] and f != h['regla'].lower(): errores.append(f"Fuente de {h['id']} no respalda {h['regla']}")
    if cfg['controles'] and cfg['usar_rag'] and errores:
        return cerrar('No hay fuentes verificables para todos los hallazgos; se requiere revisión humana.', abstuvo=True,
                      errores=errores, costo=r.costo_usd)
    artefacto = {'hallazgos': hallazgos, **r.salidas['parche']}
    respuesta = 'sin hallazgos' if not hallazgos else json.dumps(artefacto, ensure_ascii=False)
    return cerrar(respuesta, fuentes, errores=errores, artefacto=artefacto, costo=r.costo_usd)


