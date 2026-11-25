"""Ejemplo local. Nunca ejecuta el archivo revisado."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from finnorte.variante import sistema
entrada={"archivo":sys.argv[1] if len(sys.argv)>1 else "datos/v2-revisor/codigo/transferencias.py"}
print(json.dumps(sistema(entrada),ensure_ascii=False,indent=2))
