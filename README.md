# FinNorte · Equipo 2 · v2-revisor

Publicación progresiva de las partes asignadas a Luis (detectar), Alan (explicar) y César (parche).
Los siguientes commits incorporan las etapas y su integración. La cuarta etapa y la integración del documento final quedan PENDIENTES · Kevin y se excluyen de este repositorio, también sus componentes históricos.

Preparación con asistencia de ChatGPT mediante Codex. Los responsables asignados deben revisar y defender sus partes; esta publicación no acredita programación ni pruebas personales de cada integrante. Los commits usan la cuenta autenticada que realiza la publicación y fechas reales.

Python 3.10 o posterior. Crear un entorno virtual, instalar `python -m pip install -r requirements.txt` y `python -m pip install -e .`. Consultar `python -m finnorte info`. `.env.example` es una plantilla sin llave; nunca publicar `.env`.

## Alcance publicado

Tres etapas: detectar → explicar → parche. No se incluyen prompts, esquemas, validadores, pruebas, respuestas preparadas, evidencias ni ejecutores de dictamen. Tampoco el documento técnico final integrado ni las seis pruebas asignadas a esa etapa.

Las versiones históricas del Lab 2 de las etapas publicadas son 3/4/4; el perfil mejorado del Avance 1 usa 4/5/5. A=1/1/1; B, C y D=4/5/5. Los prompts medidos se copian sin cambios. `sistema()` entrega los datos de las tres etapas; el reporte narrativo final queda pendiente. El archivo limpio conserva `sin hallazgos` y su código idéntico como condiciones de las etapas publicadas.

## Pruebas y ejecución

`pytest -q` ejecuta pruebas sin red con fake/hash. Estas pruebas NO miden la calidad de un modelo real.

`python guia/a2_flujo_variante.py --demo` prueba el encadenamiento de las tres etapas con respuestas preparadas. Sin `--demo` requiere configuración y cuota del proveedor real.

Para revisar un archivo con modelo real, después de configurar `.env` desde la plantilla:

```python
from finnorte.variante import sistema
r = sistema({'archivo': 'datos/v2-revisor/codigo/transferencias.py'})
print(r['artefacto'])
```

`python guia/av1_configuraciones.py --casos evals/v2-revisor.jsonl --rep 3 --salida bitacora/publicacion_av1_nueva` genera una medición NUEVA con la configuración real. Necesita llave y cuota. No reutilizar respuestas antiguas de otra firma de código. Su salida es evidencia técnica, no el reporte final asignado a la cuarta etapa.

## Procedencia de evidencias

Los extractos históricos que se incorporan en la fase de pruebas mantienen valores medidos y SHA-256 de su archivo fuente. No son nuevas ejecuciones de esta copia. La exclusión de la cuarta etapa y el cambio de presentación modifican la firma del código; las mediciones históricas del proyecto anterior no acreditan una nueva medición de esta publicación.

Los documentos individuales de `Actividad 2/` son borradores existentes y conservan sus notas de asistencia de IA y pendientes personales. Sus referencias históricas pueden consultarse mediante los extractos publicados y el mapa de procedencia; no se publican los registros completos que contienen la cuarta etapa.
