"""Continúa la comparación con el mismo modelo y un .env autorizado."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--env', required=True, help='Ruta a la configuración privada; no se copia ni imprime')
    args = ap.parse_args()
    archivo = Path(args.env).expanduser().resolve()
    if not archivo.is_file():
        ap.error('No se encontró el archivo .env indicado')
    raiz = Path(__file__).resolve().parents[1]
    entorno = dict(os.environ)
    # La llave del archivo seleccionado prevalece sobre sesiones anteriores.
    for clave in ('GEMINI_API_KEY', 'GOOGLE_API_KEY'):
        entorno.pop(clave, None)
    entorno.update(LLM_PROVIDER='gemini', LLM_MODEL='gemini-3.1-flash-lite',
                   EMB_PROVIDER='gemini', EMB_MODEL='gemini-embedding-001',
                   PYTHONUNBUFFERED='1')
    comando = [sys.executable, 'guia/av1_configuraciones.py', '--casos', 'evals/v2-revisor.jsonl',
               '--rep', '3', '--env', str(archivo), '--salida', 'bitacora/av1_gemini31_20261105',
               '--intervalo', '4.2', '--continuar']
    resultado = subprocess.run(comando, cwd=raiz, env=entorno).returncode
    if resultado == 0:
        resultado = subprocess.run([sys.executable, 'guia/verificar_evidencias.py'],
                                   cwd=raiz, env=entorno).returncode
    destino = raiz/'bitacora/av1_gemini31_20261105'
    cantidades = {}
    for letra in 'ABCD':
        ruta = destino/f'av1_{letra}.json'
        cantidades[letra] = len(json.loads(ruta.read_text(encoding='utf-8'))['ejecuciones_guardadas']) if ruta.exists() else 0
    estado = {'estado': 'completa' if resultado == 0 else 'PENDIENTE DE MEDIR',
              'modelo': 'gemini-3.1-flash-lite', 'configuraciones': cantidades,
              'respuestas_reales': sum(cantidades.values()),
              'fecha_utc': datetime.now(timezone.utc).isoformat(), 'dictamen': 'PENDIENTE · Kevin'}
    (destino/'av1_estado_medicion.json').write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding='utf-8')
    return resultado


if __name__ == '__main__':
    raise SystemExit(main())
