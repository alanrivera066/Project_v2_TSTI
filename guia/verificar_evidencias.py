"""Comprueba que las respuestas A/B/C/D corresponden al código disponible."""
import argparse
import json
import runpy
import hashlib
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def verificar(carpeta, revision=None):
    medidor = runpy.run_path(str(RAIZ/'guia/av1_configuraciones.py'))
    if revision:
        commit = subprocess.check_output(['git','rev-parse','--verify',revision+'^{commit}'],cwd=RAIZ,text=True).strip()
        meta = json.loads((carpeta/'av1_A.json').read_text(encoding='utf-8'))['metadata']
        archivos = {p:hashlib.sha256(subprocess.check_output(['git','show',commit+':'+p],cwd=RAIZ)).hexdigest()
                    for p in meta['archivos']}
        firma = hashlib.sha256(json.dumps(archivos,sort_keys=True).encode('utf-8')).hexdigest()
        casos_texto = subprocess.check_output(['git','show',commit+':evals/v2-revisor.jsonl'],cwd=RAIZ).decode('utf-8')
    else:
        firma, archivos = medidor['huella_medicion']()
        casos_texto = (RAIZ/'evals/v2-revisor.jsonl').read_text(encoding='utf-8')
    total = 0
    incompletas = []
    for letra in 'ABCD':
        ruta = carpeta/f'av1_{letra}.json'
        if not ruta.exists():
            incompletas.append(letra)
            continue
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        meta = datos['metadata']
        if meta.get('demo') or meta.get('firma') != firma or meta.get('archivos') != archivos:
            raise ValueError(f'{letra}: la firma difiere o la evidencia es una demostración')
        filas = datos['ejecuciones_guardadas']
        parejas = {(r['id'], r['repeticion']) for r in filas}
        casos = [json.loads(l) for l in casos_texto.splitlines() if l.strip()]
        esperadas = {(c['id'], n) for c in casos for n in range(1, 4)}
        if len(filas) != len(parejas) or not parejas <= esperadas:
            raise ValueError(f'{letra}: respuestas duplicadas o casos inesperados')
        if any(str(r['salida'].get('error','')).startswith('LLMError:') for r in filas):
            raise ValueError(f'{letra}: contiene fallos del proveedor contados como respuestas')
        if any(r['salida'].get('demo') is True for r in filas):
            raise ValueError(f'{letra}: contiene respuestas simuladas')
        if meta.get('dictamen') == 'incluido en A/B/C/D':
            if not datos['config'].get('incluir_dictamen'):
                raise ValueError(f'{letra}: falta dictamen en la configuración')
            if any(not r['salida'].get('abstuvo') and not r['salida'].get('error')
                   and 'dictamen' not in r['salida'].get('artefacto',{}) for r in filas):
                raise ValueError(f'{letra}: respuesta completa sin artefacto dictamen')
        if parejas != esperadas:
            incompletas.append(letra)
        total += len(filas)
    print(json.dumps({'firma': firma, 'archivos_verificados': len(archivos),
                      'respuestas_reales_guardadas': total, 'esperadas': 240,
                      'configuraciones_pendientes': incompletas}, ensure_ascii=False, indent=2))
    if incompletas:
        print('PENDIENTE DE MEDIR. Reanudar el medidor con --continuar y la misma configuración.')
        return 2
    resumen = json.loads((carpeta/'av1_resumen.json').read_text(encoding='utf-8'))
    if resumen['metadata']['firma'] != firma:
        raise ValueError('La firma del resumen difiere de la de las respuestas')
    print('Las 240 respuestas tienen la firma del código, entradas y contrato ' +
          (f'del commit {commit}.' if revision else 'del directorio actual.'))
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--carpeta', default='bitacora/av1_cuatro_etapas_20261105')
    ap.add_argument('--revision', help='Commit o etiqueta contra el cual comprobar una medición histórica sin alterar sus firmas')
    args = ap.parse_args()
    raise SystemExit(verificar(RAIZ/args.carpeta, args.revision))
