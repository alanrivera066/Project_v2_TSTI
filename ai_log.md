# Registro de asistencia de IA

2026-11-04 · ChatGPT mediante Codex (el identificador exacto del modelo no se expone de forma verificable en esta sesión).

Se pidió preparar y publicar el proyecto existente por partes, excluyendo todo componente de la cuarta etapa. Se aceptó preparar una copia independiente, conservar los originales y registrar la procedencia de las evidencias históricas. Los cambios de esta publicación fueron preparados por el asistente; no se atribuyen a programación o revisión individual de los integrantes. La validación de esta copia se guarda en bitacora/publicacion_pytest.txt cuando se incorpora la fase de pruebas. El usuario definió el alcance y autorizó publicar; no consta revisión humana del código nuevo de esta copia.

La preparación anterior del Avance 1 también tuvo asistencia de ChatGPT mediante Codex: controles, Mini-RAG, casos, pruebas, ejecución autorizada de mediciones y borradores. Los registros personales siguen pendientes de sus autores.

## Luis
PENDIENTE: herramienta / para qué / qué acepté / qué cambié / cómo lo validé. Lo completa la persona con su uso real.

## Alan
PENDIENTE: herramienta / para qué / qué acepté / qué cambié / cómo lo validé. Lo completa la persona con su uso real.

## César
PENDIENTE: herramienta / para qué / qué acepté / qué cambié / cómo lo validé. Lo completa la persona con su uso real.

Kevin: Pendiente.

## Corrección de evidencias · 2026-11-05

Herramienta: ChatGPT mediante Codex. Modelo exacto: no verificado en los registros del proyecto.

Se pidió corregir las omisiones del Laboratorio 2 y del Avance 1 observadas en las capturas, manteniendo pendiente la cuarta etapa. Se aceptó restaurar la guía común y sus pruebas originales, importar las evidencias históricas sin la cuarta etapa, publicar la tabla de dueños y corregir los casos r06/r09. Se cambió la comprobación del archivo limpio por verificaciones de hallazgos, parches y código original, y la firma ahora cubre también corpus, entradas, contrato y medidor.

Validación realizada por el asistente: pytest pasó de 46 a 54 pruebas aprobadas; tests/test_a2_pipeline.py se restauró desde el proyecto original. Se inició una nueva medición real, con resultados en bitacora/av1_publicado_20261105; los errores del proveedor se registran como interrupciones y no como mediciones completas. La evidencia histórica de bitacora/av1_cierre se conserva por separado y no se presenta como una ejecución de este código corregido.

El usuario indicó que los registros personales de Luis, Alan y César permanezcan PENDIENTES. No consta una revisión humana de estos cambios ni se atribuyen las pruebas del asistente a los integrantes.

### Resultado comprobado de esta sesión

El asistente publicó las correcciones y GitHub Actions pasó. La prueba de la guía común se ejecutó con fake/hash y comprobó también que se rechaza sobrescribir una carpeta anterior; no fue una medición de calidad del modelo. El registro está en bitacora/av1_qa_guia_comun_20261105.json.

La API real de Gemini permitió guardar 60 respuestas de A y 2 de B. Se reintentaron fallos temporales conservando respuestas válidas; se detuvo después de tres intentos consecutivos sin progreso por HTTP 503. La comparación de 240 respuestas quedó PENDIENTE DE MEDIR. El verificador detecta correctamente la incompletitud y termina con código 2. Los 67 archivos de la firma se compararon con los blobs de Git publicados, conservando sus bytes mediante .gitattributes. No se presentan los resultados históricos como mediciones del código corregido.

## Nueva comparación autorizada · 2026-11-05

Herramienta: ChatGPT mediante Codex. Modelo exacto del asistente: no verificable en los registros del proyecto. Modelo del sistema evaluado: Gemini 3.1 Flash-Lite.

Se pidió probar otro modelo e iniciar una comparación nueva de A/B/C/D. Se aceptó conservar las 62 respuestas de Gemini 3.5 por separado. El asistente consultó los modelos disponibles con la llave ya autorizada: la prueba de Gemini 2.5 Flash-Lite recibió 404 por acceso restringido y la de Gemini 3.1 Flash-Lite recibió 200. También comprobó el buscador con embeddings reales. Estas pruebas de disponibilidad no cuentan entre las 240 evaluaciones.

Se cambió el modelo declarado en el contrato y la configuración de ejemplo. El cálculo de costo ahora distingue Gemini 3.1 de Gemini 3.5; se verificó la tarifa Standard de texto de Google, no la facturación de la cuenta. No se modificaron prompts, casos, metas ni la etapa pendiente. La nueva comparación se guarda en bitacora/av1_gemini31_20261105 con otra firma.

Validación realizada por el asistente antes de medir: 56 pruebas aprobadas; las dos nuevas comprueban que modelos con tarifas diferentes producen el costo correspondiente a sus tokens. La ejecución real y su completitud deben comprobarse con las respuestas, las trazas y guia/verificar_evidencias.py. No se registra una revisión humana que no haya ocurrido.

El usuario indicó que los próximos cambios se publiquen con Lolmastercraft. Los registros personales de Luis, Alan y César siguen PENDIENTES. Kevin sigue pendiente.
