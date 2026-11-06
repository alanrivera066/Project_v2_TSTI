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

## Kevin
Ver «Etapa dictamen · 2026-11-05» al final de este archivo.

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

Resultado real de esta comparación hasta la interrupción: A=60, B=60, C=43 y D=0; total 163/240. La API confirmó HTTP 429 por límite de 500 llamadas diarias del modelo en ese proyecto. Se guardó su respuesta completa y se verificaron las tarifas de las 491 llamadas exitosas con tokens registradas en las trazas; ese conteo no incluye todas las solicitudes sin reporte de uso ni equivale a una factura. No se calcularon métricas finales de C/D ni una comparación completa. Se preparó guia/av1_reanudar_gemini31.py para continuar con un .env autorizado sin reutilizar una llave de otra sesión ni cambiar de modelo.

### Continuación y cierre de la medición

El usuario entregó otro archivo privado de credencial y autorizó continuar. El asistente extrajo la llave en memoria sin ejecutar ese archivo ni copiarlo al repositorio. Se comprobó acceso al mismo Gemini 3.1 Flash-Lite y a gemini-embedding-001; las pruebas están separadas de la evaluación. Se conservaron 163 respuestas y se ejecutaron las 77 pendientes. No se mezclaron respuestas de Gemini 3.5.

Resultado: 240/240 ejecuciones, 60 por configuración. Exactitud A/B/C/D: 0.60/0.70/0.75/0.95. Fuentes: bitacora/av1_gemini31_20261105/av1_A.json a av1_D.json y av1_resumen.json. El verificador comprobó la firma de los 67 archivos. El asistente verificó las tarifas de las trazas, generó la tabla y ejecutó una prueba de reanudación que conservó las 240 respuestas sin llamadas nuevas ni alteraciones: av1_integridad.json y av1_qa_reanudacion.json.

D cumplió siete metas y falló latencia p95; no se rebajó la meta ni se declara aprobado todo el contrato. Se actualizó README con estos resultados y se prepararon las evidencias para el PR de Lolmastercraft. La revisión humana y la fusión no se dan por realizadas antes de comprobarlas en GitHub. Los usos personales y Kevin siguen pendientes.


## Actualización documental del Avance 1 · 2026-11-05

Herramienta: ChatGPT mediante Codex; identificador exacto del modelo del asistente no verificado. El usuario pidió actualizar el documento técnico, los pendientes desactualizados y la explicación de resultados, excluyendo Kevin y el contenido personal de los integrantes.

Se incorporaron las 240 ejecuciones reales de Gemini 3.1, la tabla A/B/C/D, los intervalos, las metas cumplidas y la latencia incumplida. Se conservaron las metas y la firma del sistema medido. Se corrigieron referencias al estado de publicación, a la etiqueta y a carpetas antiguas en README y las notas compartidas de A2. Los cuerpos personales de Mi etapa permanecen sin cambios. La sección 11 del documento se deja PENDIENTE · Kevin.

Validación documental del asistente: contraste con av1_resumen.json y av1_A/B/C/D.json, fuentes de las trazas, comprobación de las 11 secciones y revisión del DOCX exportado a PDF. La evidencia de la revisión visual y las comprobaciones se registra en bitacora/av1_documentacion_20261105.json. La aprobación de Alan al PR #1 acredita ese PR anterior; la revisión humana de esta actualización documental no se presume. Los registros personales siguen PENDIENTES.

## Etapa dictamen · 2026-11-05

Usé Claude Code con Claude Opus 5.5 (claude-opus-5-5) para el apoyo en redacción de prompts, código y pruebas. Kevin pidió crear y conectar la etapa dictamen a partir de la lista de la actividad, puso su llave en .env sin compartirla y autorizó las ejecuciones reales.

El asistente preparó rev_dictamen.v1 y v2, el esquema, dictamen.py, guia/a2_dictamen.py, los seis casos, las pruebas y la conexión en variante.py, y ajustó pruebas y guías del equipo para cuatro etapas. También preparó el borrador de Mi etapa y estas actualizaciones. Se comprobó con 92 pruebas sin red y con ejecuciones reales de Gemini 3.1 Flash-Lite guardadas en bitacora/dictamen/.

La v1 pasó 12/12 con el primer validador. Al leer sus resúmenes se vio texto ajeno a los datos y redacciones distintas; se agregó esa regla, se repitió la v1 sin editarla (1/6 válido al primer intento) y se creó la v2 (6/6). La regla se ajustó una vez tras probarla sobre salidas guardadas, porque rechazaba palabras neutras.

Participación de Kevin: definió el alcance con la lista de la actividad, configuró su llave, autorizó las ejecuciones reales y la publicación del pull request #3, y ajustó la redacción del uso de IA en Mi etapa y en este registro. Los prompts, el código y las pruebas se aceptaron como los preparó el asistente, sin cambios propios. Su validación consta en las 92 pruebas sin red y en las ejecuciones reales de bitacora/dictamen/; la revisión del código queda a cargo del equipo en el pull request #3.

## Documento técnico final · 2026-11-05

Herramienta: Claude Code con Claude Opus 5.5 (claude-opus-5-5). Kevin pidió completar su documentación después de que Alan fusionara el PR #3. El asistente redactó la sección 11, integró la etapa dictamen en las secciones 4, 5, 10 y el anexo, y exportó el PDF con Word.

Se conservaron los resultados de A/B/C/D y los registros personales pendientes de Luis, Alan y César. Validación: contraste de cifras con av1_resumen.json y bitacora/dictamen/comparacion.md, 92 pruebas aprobadas en GitHub Actions y revisión visual de las páginas modificadas.

## Integración y medición de cuatro etapas · 2026-11-05

Herramienta: ChatGPT mediante Codex; el identificador exacto del modelo del asistente no está verificado. El modelo evaluado fue Gemini 3.1 Flash-Lite.

- Medidor y pruebas: el usuario pidió incluir dictamen en una comparación nueva y conservar los escritos de Kevin. El asistente añadió --cuatro-etapas, fijó las versiones 1/1/1/1 frente a 4/5/5/2, protegió la reanudación y agregó verificación histórica por commit. Los prompts no se editaron. Validación: 92 pruebas iniciales; 98 tras los cambios, también aprobadas por GitHub Actions. No consta una revisión humana del PR #7.
- Ejecuciones reales: el asistente corrió las matrices del Lab 2 con las tres entradas oficiales y tres repeticiones adicionales de transferencias.py. Mejorada: 6/6 flujos completos; inicial: 4/6. Se conservaron los fallos. A/B/C/D nueva quedó en 59/240; ambas credenciales autorizadas devolvieron HTTP 429 por 500 llamadas diarias. Las llaves se leyeron en memoria, sin publicarlas; las 181 ejecuciones faltantes no se presentan como realizadas.
- Documento: el asistente corrigió referencias, identificó las métricas anteriores como históricas y dejó explícito el estado parcial nuevo. Se conservaron 35 textos identificados como añadidos o modificados por Kevin, incluidos sus conclusiones, mejoras y registro. Validación: comprobación textual después de Word y revisión visual de las 12 páginas. Los registros personales de Luis, Alan y César no se completaron.
- GitHub: cambios publicados con Lolmastercraft en el PR #7, todavía en borrador. Se creó avance1-medicion-3-etapas en 5939a14 y se verificaron las 240 respuestas históricas contra ese commit. La etiqueta avance1 queda pendiente del cierre. Se comprobó main protegida y acceso de los cuatro integrantes; esta cuenta no tiene administración para consultar todos los detalles. El profesor se agregará después por el equipo.

## Reanudación real y corte 180/240 · 2026-11-06

- Herramienta: ChatGPT mediante Codex; identificador exacto del modelo del asistente no verificado.
- Solicitud: el usuario pidió reintentar con la configuración actual. El asistente reanudó la comparación con Gemini 3.1 Flash-Lite, manteniendo código, prompts, casos y contrato.
- Resultado: A, B y C terminaron con 60 ejecuciones cada una. Al comenzar D se agotó la cuota; otra configuración autorizada respondió a una prueba pequeña, pero la corrida y la comprobación posterior devolvieron 429 diario. El usuario decidió dejar lista la continuación tras el reinicio.
- Cambios aceptados: conservar las 180 respuestas y todas las interrupciones; actualizar el estado compartido y el documento con ese corte. No se cambian textos de Kevin ni registros personales.
- Validación: verificador con 71 archivos y 180 respuestas, código 2 por D pendiente; comparación de las 59 respuestas iniciales y de las 180 guardadas, sin modificaciones. La ejecución real sigue incompleta. Esta entrada no acredita revisión humana de los integrantes.

## Medición de cuatro etapas completada · 2026-11-06

Herramienta: ChatGPT mediante Codex. El identificador exacto del modelo del asistente no está verificado. El usuario pidió integrar el trabajo existente de Kevin, medir el flujo completo y actualizar evidencias, documentos y etiquetas, conservando los textos personales y las aportaciones de Kevin.

- Medidor y verificación: el asistente añadió --cuatro-etapas, fijó dictamen v1 en A y v2 en B/C/D, protegió la reanudación frente a alcances distintos y permitió verificar firmas históricas contra un commit. Se conservaron todos los prompts medidos. Validación: 92 pruebas iniciales y 98 después de los cambios; la firma histórica se comprobó contra 5939a14.
- Ejecuciones reales: el asistente ejecutó matrices del Lab 2 y las 240 respuestas A/B/C/D con Gemini 3.1 Flash-Lite, usando las configuraciones privadas autorizadas en memoria. Se conservaron fallos, intentos y datos históricos. El código calculó las métricas; no se atribuye a cada persona una ejecución independiente.
- Documentación: el asistente actualizó resultados compartidos y referencias a partir de las nuevas bitácoras. Los textos de Kevin se conservaron y sus conclusiones anteriores se identificaron por su alcance. Se revisaron el Word y el PDF renderizado. Los registros personales de Luis, Alan y César siguen pendientes.
- GitHub: publicación con Lolmastercraft y etiqueta histórica de tres etapas. La revisión humana del nuevo PR solo se dará por realizada si consta en GitHub; esta entrada no la acredita.

## Actualización final del documento · 2026-11-06

Herramienta: ChatGPT mediante Codex; modelo exacto del asistente no verificado. El usuario solicitó actualizar la sección 11 y limpiar referencias y notas antiguas del PDF, autorizando cambiar esa sección que antes se conservaba literalmente. El asistente usó las cifras reales de cuatro etapas, retiró el bloque de referencias antiguas y revisó las 12 páginas renderizadas. Se aceptaron estos cambios documentales; no se cambiaron la medición, el código ni los registros personales. Evidencia: bitacora/av1_documentacion_final_20261106.json. La fusión y la etiqueta requieren la aprobación exigida por GitHub.
