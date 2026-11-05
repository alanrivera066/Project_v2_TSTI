# FinNorte · Equipo 2 · v2-revisor

Revisa código Python mediante detectar → explicar → parche y entrega sus datos estructurados. La cuarta etapa, su reporte, sus seis pruebas y la integración del documento final quedan **PENDIENTES · Kevin**, fuera de esta publicación.

## Responsabilidades

| Persona | Parte asignada |
|---|---|
| Luis · Lolmastercraft | Detectar, buscador, Mini-RAG, fuentes, citas y abstención |
| Alan · alanrivera066 | Explicar, esquema y reintento, 20 casos de evaluación |
| César · MajesDo63 | Parche, reglas de negocio y contrato de calidad |
| Kevin | PENDIENTE · Kevin |

Dueños, entradas, salidas, fusión y decisiones fechadas: `avance1/equipo.md`. La preparación y las pruebas tienen asistencia de IA registrada en `ai_log.md`. Los usos personales quedan **PENDIENTES**, por instrucción del usuario; la asignación y la cuenta que publica no acreditan ejecución individual.

## Instalación y pruebas

Python 3.10 o posterior:

```text
python -m venv .venv
```

Windows: `.\.venv\Scripts\Activate.ps1`. Mac/Linux: `source .venv/bin/activate`.

```text
python -m pip install -r requirements.txt
python -m pip install -e .
python -m finnorte info
pytest -q
```

Las pruebas usan fake/hash, sin red: comprueban código, no calidad de un modelo real. Para Gemini, crea `.env` desde `.env.example` y configura la llave solo en ese archivo local, excluido de Git.

## Laboratorio 2

La guía común del profesor está en `guia/s2_flujo_cambios.py`: analizar → plan → checklist → nota. Sus prompts `cambio_*`, esquemas y pruebas originales `tests/test_a2_pipeline.py` están publicados. Este ejemplo de solicitudes de cambio es independiente de la cuarta etapa pendiente del revisor.

```text
python guia/s2_flujo_cambios.py --plan-version 1 --directorio bitacora/s2_nuevo_v1
python guia/s2_flujo_cambios.py --plan-version 2 --directorio bitacora/s2_nuevo_v2
```

Con Gemini configurado son llamadas reales; con `LLM_PROVIDER=fake` son demostraciones. Cada corrida escribe en una carpeta nueva y rechaza sobrescribir una anterior sin `--continuar`.

Las matrices históricas reales de la guía están en `bitacora/s2_trazabilidad_plan_v1.json`, `s2_trazabilidad_plan_v2.json` y sus registros de consistencia. Las matrices del revisor están en `bitacora/a2_matriz.md` y `a2_matriz_v1.md`, respaldadas por `a2_trazabilidad*.json` y las trazas de `bitacora/lab2_tres_etapas/`. Se conservan resultados y errores históricos de las tres etapas; se excluyó la cuarta etapa de esas copias. Procedencia y hashes: `bitacora/procedencia_importacion_20261105.json`.

`python guia/a2_flujo_variante.py --demo` comprueba tres etapas con respuestas preparadas; no mide calidad de IA. Sin `--demo`, requiere un proveedor real y escribe nuevas evidencias en `bitacora/publicacion_lab2/flujo/`.

## Avance 1 y mediciones

Versiones del Lab 2: detectar v3, explicar v4, parche v4. Perfil mejorado del Avance 1: v4/v5/v5. A usa v1/v1/v1; B, C y D usan el perfil mejorado. Los prompts medidos no se editaron. El esquema y reintento están activos en las cuatro configuraciones; D añade controles de negocio, dominio, citas y saneo.

Los 20 casos tienen 12 normales, 4 fuera de dominio y 4 límite/adversariales. r06 comprueba que el archivo limpio no tenga hallazgos ni parches, conserve su código y no se abstenga. r09 tiene su texto corregido en UTF-8.

| Evidencia | Qué demuestra |
|---|---|
| `bitacora/av1_cierre/` | Medición histórica completa del 2 de noviembre: 240 respuestas originales y trazas, con sus bytes conservados. Respalda antecedentes citados en A2; su firma no corresponde al código corregido. |
| `bitacora/av1_publicado_20261105/` | Medición nueva del código corregido. Consultar su resumen o el estado **PENDIENTE DE MEDIR** si hubo interrupción. No mezclar firmas distintas. |
| `bitacora/correccion_av1_pytest_antes.txt` | Pruebas de la copia antes de corregirla. |
| `bitacora/correccion_av1_pytest_despues.txt` | Pruebas ejecutadas después de corregirla; sin modelo real. |

La firma incluye código del sistema, prompts y esquemas, corpus, archivos de entrada, casos, contrato y medidor. Para comprobarla contra las respuestas guardadas:

```text
python guia/verificar_evidencias.py
```

Termina con código 2 si falta medir; no certifica una comparación parcial como completa. Para una medición nueva con la llave real ya configurada:

```text
python guia/av1_configuraciones.py --casos evals/v2-revisor.jsonl --rep 3 --salida bitacora/av1_medicion_nueva
```

Para continuar la medición corregida sin repetir respuestas válidas:

```text
python guia/av1_configuraciones.py --casos evals/v2-revisor.jsonl --rep 3 --salida bitacora/av1_publicado_20261105 --continuar
```

Mantener el mismo proveedor, modelo, embeddings, contrato y archivos. `--env RUTA_AL_ENV` permite leer una configuración sin copiar la llave al repositorio. Los fallos del proveedor se registran aparte y detienen la corrida. Las metas se conservan aunque alguna no se alcance.

## Actividad 2

Los borradores individuales están en `Actividad 2/Luis/`, `Actividad 2/Cesar/` y `Actividad 2/Alan/`. Sus comparaciones son históricas y sus fuentes de las tres etapas ahora están publicadas. Cada persona debe revisarlos y registrar su participación real. El documento técnico integrado sigue pendiente de la cuarta etapa.
