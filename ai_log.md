# Registro de asistencia de IA

ChatGPT

## Luis Alfonso Juárez Amaro — Uso personal de IA

**Herramienta utilizada:** ChatGPT mediante Codex.

**¿Para qué la utilicé?**

la detección de problemas, conexión del buscador de reglas y controles de citas.

**¿Qué acepté del apoyo recibido?**

Acepté propuestas de código y ajustes de prompts que se incorporaron al proyecto con sus evidencias. También acepté utilizar las bitácoras para respaldar las cifras, en lugar de presentar resultados que no estuvieran medidos.

**¿Qué cambié o pedí ajustar?**

Fui precisando el alcance del trabajo y la distribución de las etapas. Pedí conservar los prompts anteriores y trabajar con versiones nuevas para mantener un registro de los cambios. También pedí que los registros personales permanecieran pendientes hasta preparar su contenido.

**¿Cómo se validó?**

La validación se hizo mediante pruebas de código, ejecuciones reales con Gemini y revisión de las bitácoras, realizadas con asistencia de la herramienta. En la evidencia de mi etapa, detectar mantuvo los mismos cinco hallazgos en las tres repeticiones de transferencias.py.

Los resultados pueden consultarse en bitacora/lab2_cuatro_etapas_20261105/a2_matriz.md y a2_trazabilidad.json. La coincidencia fue de reglas y líneas.

## Alan — Uso personal de IA

**Herramienta utilizada:** ChatGPT mediante Codex.

**¿Para qué la utilicé?**

Para comprender mi etapa `rev_explicar`, revisar las evidencias del proyecto y completar mi documento «Mi etapa» y este registro.

**¿Qué acepté del apoyo recibido?**

Acepté las explicaciones sobre el funcionamiento de mi etapa y el apoyo para comprobar los resultados de la bitácora, localizar mis aportaciones en GitHub y preparar los ajustes del documento y su PDF.

**¿Qué cambié o pedí ajustar?**

Pedí conservar las secciones existentes y concentrar los cambios en los avisos de borrador, los pendientes y las referencias desactualizadas. Aclaré que realicé personalmente las tres repeticiones de v4 sobre reportes.py. También solicité incluir mis aprobaciones de propuestas del equipo y conservar la fuente, los colores y el formato original del PDF.

**¿Cómo lo validé?**

Realicé las tres ejecuciones de v4 sobre reportes.py registradas en `bitacora/lab2_cierre/casos/alan_trazabilidad__v4__r1.json`, `r2.json` y `r3.json`, con el mismo prefijo de nombre.

Con asistencia de Codex se contrastaron el documento, el prompt, las validaciones y las evidencias. Se comprobaron nueve aprobaciones de mi cuenta en ocho PR.

Los ajustes de mi documento y PDF quedaron publicados e incorporados mediante el [PR #19](https://github.com/alanrivera066/Project_v2_TSTI/pull/19). Estas actualizaciones documentales no representan nuevas ejecuciones del modelo.

## César
ChatGPT y Codex / Para comprender mi etapa de parches y analizar el prompt, el validador y las evidencias / Acepté las explicaciones y el apoyo para preparar mi documento / Solicité ajustes en la redacción y agregué mi commit y uso de IA / Con apoyo de Codex se revisaron las versiones del prompt y los resultados guardados, y se comprobaron casos de archivo limpio y sintaxis incorrecta.

## Kevin
Ver «Etapa dictamen · 2026-11-05» al final de este archivo.

## Corrección de evidencias · 2026-11-05

Herramienta: ChatGPT mediante Codex. Modelo exacto: no verificado en los registros del proyecto.

Se cambió la comprobación del archivo limpio por verificaciones de hallazgos, parches y código original, y la firma ahora cubre también corpus, entradas, contrato y medidor.

Validación realizada por el asistente: pytest pasó de 46 a 54 pruebas aprobadas; tests/test_a2_pipeline.py se restauró desde el proyecto original. Se inició una nueva medición real, con resultados en bitacora/av1_publicado_20261105; los errores del proveedor se registran como interrupciones y no como mediciones completas. La evidencia histórica de bitacora/av1_cierre se conserva por separado y no se presenta como una ejecución de este código corregido.

### Resultado comprobado de esta sesión

La API real de Gemini permitió guardar 60 respuestas de A y 2 de B. Se reintentaron fallos temporales conservando respuestas válidas; se detuvo después de tres intentos consecutivos sin progreso por HTTP 503. La comparación de 240 respuestas quedó PENDIENTE DE MEDIR. El verificador detecta correctamente la incompletitud y termina con código 2. Los 67 archivos de la firma se compararon con los blobs de Git publicados, conservando sus bytes mediante .gitattributes. No se presentan los resultados históricos como mediciones del código corregido.

## Nueva comparación autorizada · 2026-11-05

Herramienta: ChatGPT mediante Codex. Modelo exacto del asistente: no verificable en los registros del proyecto. Modelo del sistema evaluado: Gemini 3.1 Flash-Lite.

Se pidió probar otro modelo e iniciar una comparación nueva de A/B/C/D. Se aceptó conservar las 62 respuestas de Gemini 3.5 por separado. El asistente consultó los modelos disponibles con la llave ya autorizada: la prueba de Gemini 2.5 Flash-Lite recibió 404 por acceso restringido y la de Gemini 3.1 Flash-Lite recibió 200. También comprobó el buscador con embeddings reales. Estas pruebas de disponibilidad no cuentan entre las 240 evaluaciones.

Se cambió el modelo declarado en el contrato y la configuración de ejemplo. El cálculo de costo ahora distingue Gemini 3.1 de Gemini 3.5; se verificó la tarifa Standard de texto de Google, no la facturación de la cuenta. No se modificaron prompts, casos, metas ni la etapa pendiente. La nueva comparación se guarda en bitacora/av1_gemini31_20261105 con otra firma.

Validación realizada por el asistente antes de medir: 56 pruebas aprobadas; las dos nuevas comprueban que modelos con tarifas diferentes producen el costo correspondiente a sus tokens. La ejecución real y su completitud deben comprobarse con las respuestas, las trazas y guia/verificar_evidencias.py. No se registra una revisión humana que no haya ocurrido.

Resultado real de esta comparación hasta la interrupción: A=60, B=60, C=43 y D=0; total 163/240. La API confirmó HTTP 429 por límite de 500 llamadas diarias del modelo en ese proyecto. Se guardó su respuesta completa y se verificaron las tarifas de las 491 llamadas exitosas con tokens registradas en las trazas; ese conteo no incluye todas las solicitudes sin reporte de uso ni equivale a una factura. No se calcularon métricas finales de C/D ni una comparación completa.

### Continuación y cierre de la medición

Se comprobó acceso al mismo Gemini 3.1 Flash-Lite y a gemini-embedding-001; las pruebas están separadas de la evaluación. Se conservaron 163 respuestas y se ejecutaron las 77 pendientes. No se mezclaron respuestas de Gemini 3.5.

Resultado: 240/240 ejecuciones, 60 por configuración. Exactitud A/B/C/D: 0.60/0.70/0.75/0.95. Fuentes: bitacora/av1_gemini31_20261105/av1_A.json a av1_D.json y av1_resumen.json. El verificador comprobó la firma de los 67 archivos. El asistente verificó las tarifas de las trazas, generó la tabla y ejecutó una prueba de reanudación que conservó las 240 respuestas sin llamadas nuevas ni alteraciones: av1_integridad.json y av1_qa_reanudacion.json.

D cumplió siete metas y falló latencia p95; no se rebajó la meta ni se declara aprobado todo el contrato. Se actualizó README con estos resultados y se prepararon las evidencias para el PR de Lolmastercraft. La revisión humana y la fusión no se dan por realizadas antes de comprobarlas en GitHub. Los usos personales y Kevin siguen pendientes.


## Actualización documental del Avance 1 · 2026-11-05

Herramienta: ChatGPT 

Se incorporaron las 240 ejecuciones reales de Gemini 3.1, la tabla A/B/C/D, los intervalos, las metas cumplidas y la latencia incumplida. Se conservaron las metas y la firma del sistema medido. Se corrigieron referencias al estado de publicación, a la etiqueta y a carpetas antiguas en README y las notas compartidas de A2. Los cuerpos personales de Mi etapa permanecen sin cambios. La sección 11 del documento se deja PENDIENTE · Kevin.

Validación documental del asistente: contraste con av1_resumen.json y av1_A/B/C/D.json, fuentes de las trazas, comprobación de las 11 secciones y revisión del DOCX exportado a PDF. La evidencia de la revisión visual y las comprobaciones se registra en bitacora/av1_documentacion_20261105.json. La aprobación de Alan al PR #1 acredita ese PR anterior; la revisión humana de esta actualización documental no se presume. Los registros personales siguen PENDIENTES.

## Etapa dictamen · 2026-11-05

Uos de Claude code para el apoyo en redacción de prompts, código y pruebas. Kevin pidió crear y conectar la etapa dictamen a partir de la lista de la actividad, puso su llave en .env sin compartirla y autorizó las ejecuciones reales.

El asistente preparó rev_dictamen.v1 y v2, el esquema, dictamen.py, guia/a2_dictamen.py, los seis casos, las pruebas y la conexión en variante.py, y ajustó pruebas y guías del equipo para cuatro etapas. También preparó el borrador de Mi etapa y estas actualizaciones. Se comprobó con 92 pruebas sin red y con ejecuciones reales de Gemini 3.1 Flash-Lite guardadas en bitacora/dictamen/.

La v1 pasó 12/12 con el primer validador. Al leer sus resúmenes se vio texto ajeno a los datos y redacciones distintas; se agregó esa regla, se repitió la v1 sin editarla (1/6 válido al primer intento) y se creó la v2 (6/6). La regla se ajustó una vez tras probarla sobre salidas guardadas, porque rechazaba palabras neutras.

Participación de Kevin: definió el alcance con la lista de la actividad, configuró su llave, autorizó las ejecuciones reales y la publicación del pull request #3, y ajustó la redacción del uso de IA en Mi etapa y en este registro. Los prompts, el código y las pruebas se aceptaron como los preparó el asistente, sin cambios propios. Su validación consta en las 92 pruebas sin red y en las ejecuciones reales de bitacora/dictamen/; la revisión del código queda a cargo del equipo en el pull request #3.

## Documento técnico final · 2026-11-05

Herramienta: Claude Code con Claude Opus 5.5 (claude-opus-5-5). Kevin pidió completar su documentación después de que Alan fusionara el PR #3. El asistente redactó la sección 11, integró la etapa dictamen en las secciones 4, 5, 10 y el anexo, y exportó el PDF con Word.

Se conservaron los resultados de A/B/C/D y los registros personales pendientes de Luis, Alan y César. Validación: contraste de cifras con av1_resumen.json y bitacora/dictamen/comparacion.md, 92 pruebas aprobadas en GitHub Actions y revisión visual de las páginas modificadas.

## Reanudación real y corte 180/240 · 2026-11-06

- Herramienta: ChatGPT mediante Codex}
- Solicitud: el usuario pidió reintentar con la configuración actual. El asistente reanudó la comparación con Gemini 3.1 Flash-Lite, manteniendo código, prompts, casos y contrato.
- Resultado: A, B y C terminaron con 60 ejecuciones cada una. Al comenzar D se agotó la cuota; otra configuración autorizada respondió a una prueba pequeña, pero la corrida y la comprobación posterior devolvieron 429 diario. El usuario decidió dejar lista la continuación tras el reinicio.
- Cambios aceptados: conservar las 180 respuestas y todas las interrupciones; actualizar el estado compartido y el documento con ese corte. No se cambian textos de Kevin ni registros personales.
- Validación: verificador con 71 archivos y 180 respuestas, código 2 por D pendiente; comparación de las 59 respuestas iniciales y de las 180 guardadas, sin modificaciones. La ejecución real sigue incompleta. Esta entrada no acredita revisión humana de los integrantes.

## Medición de cuatro etapas completada · 2026-11-06

Herramienta: ChatGPT mediante Codex.

- Medidor y verificación: el asistente añadió --cuatro-etapas, fijó dictamen v1 en A y v2 en B/C/D, protegió la reanudación frente a alcances distintos y permitió verificar firmas históricas contra un commit. Se conservaron todos los prompts medidos. Validación: 92 pruebas iniciales y 98 después de los cambios; la firma histórica se comprobó contra 5939a14.
- Ejecuciones reales: el asistente ejecutó matrices del Lab 2 y las 240 respuestas A/B/C/D con Gemini 3.1 Flash-Lite, usando las configuraciones privadas autorizadas en memoria. Se conservaron fallos, intentos y datos históricos. El código calculó las métricas.
- GitHub: publicación con Lolmastercraft y etiqueta histórica de tres etapas.

## Actualización final del documento · 2026-11-06

Herramienta: ChatGPT mediante Codex; modelo exacto del asistente no verificado. 

El usuario solicitó actualizar Varias secciones en el repositorio
