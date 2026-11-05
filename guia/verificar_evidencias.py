"""Comprueba que las respuestas A/B/C/D corresponden al código disponible."""
import argparse
import json
import runpy
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def verificar(carpeta):
    medidor = runpy.run_path(str(RAIZ/'guia/av1_configuraciones.py'))
    firma, archivos = medidor['huella_medicion']()
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
        casos = [json.loads(l) for l in (RAIZ/'evals/v2-revisor.jsonl').read_text(encoding='utf-8').splitlines()]
        esperadas = {(c['id'], n) for c in casos for n in range(1, 4)}
        if len(filas) != len(parejas) or not parejas <= esperadas:
            raise ValueError(f'{letra}: respuestas duplicadas o casos inesperados')
        if any(str(r['salida'].get('error','')).startswith('LLMError:') for r in filas):
            raise ValueError(f'{letra}: contiene fallos del proveedor contados como respuestas')
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
    print('Las 240 respuestas tienen la firma del código, entradas y contrato publicados.')
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--carpeta', default='bitacora/av1_gemini31_20261105')
    args = ap.parse_args()
    raise SystemExit(verificar(RAIZ/args.carpeta))
