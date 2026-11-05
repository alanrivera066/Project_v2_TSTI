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
| `bitacora/av1_gemini31_20261105/` | Comparación independiente iniciada el 5 de noviembre con Gemini 3.1 Flash-Lite. No reutiliza respuestas de Gemini 3.5. El resumen y el verificador indican si terminó. |
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

Para continuar la comparación de Gemini 3.1, configura `LLM_MODEL=gemini-3.1-flash-lite`, `EMB_PROVIDER=gemini` y `EMB_MODEL=gemini-embedding-001` en el entorno o en tu `.env` local:

```text
python guia/av1_configuraciones.py --casos evals/v2-revisor.jsonl --rep 3 --salida bitacora/av1_gemini31_20261105 --continuar
```

Mantener el mismo proveedor, modelo, embeddings, contrato y archivos. `--env RUTA_AL_ENV` permite leer una configuración sin copiar la llave al repositorio. Los fallos del proveedor se registran aparte y detienen la corrida. Las metas se conservan aunque alguna no se alcance.

## Actividad 2

Los borradores individuales están en `Actividad 2/Luis/`, `Actividad 2/Cesar/` y `Actividad 2/Alan/`. Sus comparaciones son históricas y sus fuentes de las tres etapas ahora están publicadas. Cada persona debe revisarlos y registrar su participación real. El documento técnico integrado sigue pendiente de la cuarta etapa.

## Antecedente de Gemini 3.5 · 5 de noviembre

A terminó 60/60 ejecuciones y B conserva 2/60; C y D siguen pendientes. Hay 62/240 respuestas reales guardadas. Gemini respondió repetidamente HTTP 503 UNAVAILABLE y tiempos de espera; después de varios reintentos sin progreso se detuvo la corrida. No se sustituyeron respuestas por salidas fake ni se reutilizaron las 240 históricas de otra firma.

Esas 62 respuestas corresponden al código del commit `87427960918c2c87fdcc277a70757da13eb157cb`, con firma `1fd3da80456dbb8ade55a0cba3093ba0ac8af2478bbd9e74e48efdd1e69f0230`. Se conservan intactas como comparación parcial anterior. Su manifiesto permite comprobar los 67 archivos en ese commit. No deben verificarse contra el código posterior ni mezclarse con Gemini 3.1.

Antes de esta actualización, la etiqueta `avance1` identificaba la entrega de tres etapas con esa medición parcial. La nueva comparación completa está en el pull request de esta rama; la etiqueta se actualizará al estado final después de la revisión y fusión en `main`. Kevin y los usos personales conservan sus pendientes.

## Nueva comparación con Gemini 3.1

El usuario autorizó iniciar A/B/C/D desde cero con otro modelo porque Gemini 3.5 devolvió 503. Gemini 3.1 Flash-Lite respondió a una prueba real de disponibilidad; el buscador también respondió usando `gemini-embedding-001`. Ambas comprobaciones se guardan aparte de las 240 ejecuciones de evaluación.

Se mantienen los prompts, casos, metas, embeddings y flujo de tres etapas. Solo cambian el modelo declarado y la estimación del costo por modelo: 0.25 USD de entrada y 1.50 USD de salida por millón de tokens de texto, a tarifa Standard de pago verificada el 5 de noviembre. Fuente: [precios de Google](https://aistudio.google.com/docs/pricing#gemini-3.1-flash-lite). Es una estimación con tokens reales; excluye embeddings y no representa una factura ni confirma cargos en una cuenta gratuita.

El verificador usa por defecto `bitacora/av1_gemini31_20261105/`. La nueva firma distingue este código y contrato de las comparaciones anteriores. Las metas no se ajustan para hacer pasar resultados; la calidad se informa aunque no alcance el contrato.

### Interrupción anterior: 163/240

La corrida se interrumpió en A=60, B=60, C=43 y D=0. Gemini 3.1 devolvió HTTP 429 al alcanzar 500 llamadas diarias por proyecto/modelo. La respuesta completa está en `bitacora/av1_gemini31_20261105/av1_cuota_agotada.json`. El usuario proporcionó otra credencial autorizada y se continuaron las 77 ejecuciones restantes sin cambiar de modelo, embeddings, prompts, casos ni metas. El cambio de acceso se registra en `av1_cambio_credencial.json`; las dos llaves quedaron fuera de Git.

Los archivos `av1_comparacion_parcial.md`, `av1_estado_verificado.json` y `av1_interrupcion*.json` conservan ese corte y sus errores como antecedentes. El estado final se consulta en `av1_estado_medicion.json`, `av1_resumen.json` y el verificador.

### Resultado final: 240/240

Las cuatro configuraciones completaron 20 casos con tres repeticiones. La firma de los 67 archivos coincide con el código publicado en esta rama. Fuente y tabla completa: `bitacora/av1_gemini31_20261105/av1_comparacion.md`; respuestas y métricas: `av1_A.json` a `av1_D.json` y `av1_resumen.json`.

| Configuración | Ejecuciones | Exactitud | Consistencia |
|---|---:|---:|---:|
| A | 60 | 0.60 | 0.90 |
| B | 60 | 0.70 | 0.90 |
| C | 60 | 0.75 | 0.95 |
| D | 60 | 0.95 | 0.95 |

D obtuvo fuga PII=0.00, citas correctas=0.95 y abstención correcta=0.95 en estos casos. Cumplió siete de las ocho metas; falló latencia p95: 66,173.0 ms frente a 12,000 ms. El contrato completo no se declara aprobado. La estimación de costo por ejecución completada fue 0.001570 USD para D; excluye embeddings, ejecuciones interrumpidas y solicitudes sin reporte de tokens, y no es una factura. El costo de todas las llamadas con tokens registrados figura aparte en `av1_integridad.json`.

Los intervalos pareados por caso están en `av1_resumen.json` y en la tabla completa. La prueba de reanudación conservó las 240 respuestas sin llamadas nuevas al modelo: `av1_qa_reanudacion.json`. La evidencia de pruebas locales y CI corresponde a 56 pruebas aprobadas, sin medir calidad de IA. La cuarta etapa y el documento final de Kevin siguen pendientes.

Con cuota disponible en el proyecto actual o en otro proyecto autorizado, desde la raíz del repositorio:

```text
python guia/av1_reanudar_gemini31.py --env "RUTA_AL_ENV"
python guia/verificar_evidencias.py
```

El primer comando funciona en Windows, Mac y Linux. Fuerza el mismo modelo y embeddings, lee la llave del archivo elegido y conserva las respuestas existentes. No guarda la llave. El segundo certifica las 240 ejecuciones; si faltan datos termina con código 2. Cambiar solo la llave dentro del mismo proyecto no aumenta su cuota.
