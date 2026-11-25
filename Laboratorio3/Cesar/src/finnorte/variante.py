"""Motor de cuatro etapas de v2-revisor. No ejecuta el código recibido."""
from __future__ import annotations
import ast
import json
import time
from . import controles,trazas,revisor
from .config import RAIZ,config as configuracion
from .pipeline import Etapa,Pipeline
from .retrieval import Indice,Resultado,contexto_para_prompt

VARIANTE="v2-revisor"
_INDICE={}
CONFIG_POR_DEFECTO=dict(version_prompt=2,usar_rag=True,controles=True,k=4,umbral=0.35)

def indice():
    c=configuracion()
    clave=(c.emb_proveedor,c.emb_modelo)
    if clave not in _INDICE: _INDICE[clave]=Indice.desde_carpeta(RAIZ/"corpus"/VARIANTE)
    return _INDICE[clave]

def leer_entrada(entrada):
    if "archivo" in entrada:
        ruta=(RAIZ/entrada["archivo"]).resolve()
        raiz=(RAIZ/"datos"/VARIANTE/"codigo").resolve()
        if not ruta.is_relative_to(raiz) or ruta.suffix.lower()!=".py":
            raise ValueError("Solo archivos Python de datos/v2-revisor/codigo")
        return ruta.read_text(encoding="utf-8")
    if isinstance(entrada.get("codigo"),str): return entrada["codigo"]
    raise ValueError("Se recibe codigo Python o archivo de ejemplos")

def crear_flujo(version):
    etapas=[]
    for nombre,usa in [("reglas",[]),("explicar",["reglas"]),("parche",["reglas","explicar"]),("verificar",["parche"])]:
        etapas.append(Etapa(nombre,"revisor_"+nombre,version=version,usa=usa,
            validar=revisor.validar_parches if nombre in ("parche","verificar") else revisor.validar_hallazgos,temperatura=0.0))
    return Pipeline(etapas,nombre=VARIANTE)

FLUJO,FLUJO_V1=crear_flujo(2),crear_flujo(1)

def resumen_etapas(flujo):
    return [{k:v for k,v in e.items() if k != "salida"} for e in flujo.bitacora()]

def armar_salida(t0,respuesta,fuentes=None,abstuvo=False,errores_citas=None,artefacto=None,costo_usd=0.0,**extra):
    return dict(respuesta=respuesta,fuentes=fuentes or [],abstuvo=abstuvo,errores_citas=errores_citas or [],
        artefacto=artefacto or {},latencia_ms=round((time.perf_counter()-t0)*1000,1),costo_usd=costo_usd,**extra)

def sistema(entrada,config=None):
    cfg={**CONFIG_POR_DEFECTO,**(config or {})}
    # Umbral de desarrollo de hash, separado del umbral semántico pendiente de calibración real.
    if configuracion().emb_proveedor == "hash" and (not config or "umbral" not in config):
        cfg["umbral"] = 0.20
    t0=time.perf_counter()
    def abstener(motivo,**extra):
        return armar_salida(t0,controles.RESPUESTA_ABSTENCION,abstuvo=True,motivo=motivo,**extra)
    try:
        codigo=leer_entrada(entrada)
        if len(codigo)>60000 or not codigo.strip(): return abstener("Entrada vacía o extensa")
        if not ast.parse(codigo).body: return abstener("No hay instrucciones Python")
    except (SyntaxError,ValueError,OSError) as exc:
        return abstener(type(exc).__name__+": entrada no admitida")
    senales=revisor.analizar(codigo)
    consultas=[h["regla"]+" "+h["explicacion"] for h in senales] or ["SEC-04 validación entrada monto Decimal límites"]
    recuperados=[]
    if cfg["usar_rag"]:
        mejores={}
        for consulta in consultas:
            for r in indice().buscar(consulta,k=cfg["k"]):
                if cfg["controles"] and r.fragmento.clasificacion not in ("publica","interna"): continue
                anterior=mejores.get(r.fragmento.id)
                if anterior is None or r.puntaje>anterior.puntaje: mejores[r.fragmento.id]=r
        # Consulta híbrida: una regla identificada por AST también se busca por su ID exacto.
        # El puntaje 1.0 indica coincidencia de identificador, no similitud coseno.
        reglas = {h["regla"].lower() for h in senales}
        for frag in indice().fragmentos:
            if frag.doc_id in reglas and (not cfg["controles"] or frag.clasificacion in ("publica", "interna")):
                mejores[frag.id] = Resultado(frag, 1.0)
        if reglas:
            trazas.registrar("busqueda_identificador", reglas=sorted(reglas), modo="id_exacto")
        recuperados=sorted(mejores.values(),key=lambda r:-r.puntaje)
        if cfg["controles"] and controles.debe_abstenerse(recuperados,cfg["umbral"]): return abstener("Contexto por debajo del umbral")
    ids={r.fragmento.doc_id for r in recuperados}
    if cfg["controles"] and cfg["usar_rag"] and any(h["regla"].lower() not in ids for h in senales):
        return abstener("No se recuperó una política necesaria")
    datos=dict(senales=senales,recuperados=sorted(ids))
    flujo=FLUJO_V1 if cfg["version_prompt"]==1 else FLUJO
    r=flujo.ejecutar(dict(entrada=codigo,contexto=contexto_para_prompt(recuperados,max_chars=14000) or "(sin contexto)",datos=datos,senales=senales))
    if not r.ok or len(r.etapas)!=4:
        return abstener("Falló la validación de una etapa",costo_usd=r.costo_usd,etapas=resumen_etapas(r))
    final=r.salidas["verificar"]
    fuentes=final["fuentes"]
    errores=controles.verificar_citas(fuentes,recuperados)
    if cfg["controles"] and cfg["usar_rag"]:
        citadas={str(f).removeprefix("doc:").split("#")[0] for f in fuentes}
        errores += ["Regla del hallazgo sin cita" for h in final["hallazgos"] if h["regla"].lower() not in citadas]
        # Código limpio no exige una cita inventada a una regla infringida.
        if not final["hallazgos"] and not fuentes: errores=[]
        if errores: return abstener("Fuentes inválidas",errores_citas=errores,costo_usd=r.costo_usd)
    texto=json.dumps(final,ensure_ascii=False)
    avisos=[]
    if cfg["controles"]:
        texto,avisos=controles.sanear_salida(texto)
        final=json.loads(texto)
    trazas.registrar("revision",variante=VARIANTE,hallazgos=len(final["hallazgos"]),fuentes=fuentes,proveedor=configuracion().llm_proveedor,config=cfg)
    return armar_salida(t0,texto,fuentes,errores_citas=errores,artefacto=final,costo_usd=r.costo_usd,
        avisos=avisos,simulado=configuracion().llm_proveedor=="fake",etapas=resumen_etapas(r))
