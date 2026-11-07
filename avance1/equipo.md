# Equipo 2 · v2-revisor

Repositorio: https://github.com/alanrivera066/Project_v2_TSTI

Canal: WhatsApp. Horario de revisión: por la tarde, sin hora fija confirmada.

## Dueños de etapa

La asignación indica quién debe revisar y defender cada parte. La preparación asistida y la publicación desde una cuenta no acreditan programación, pruebas ni revisión personal.

| Integrante | Usuario | Etapa | Recibe | Entrega | Validación en código |
|---|---|---|---|---|---|
| Luis | Lolmastercraft | detectar · rev_detectar | Archivo Python numerado y señales estáticas | Hallazgos: id, regla, linea y descripcion | Línea existente, regla permitida, duplicados y cobertura de registros sensibles reconocibles |
| Alan | alanrivera066 | explicar · rev_explicar | Hallazgos de detectar y código | Los mismos hallazgos con explicación; en AV1 añade fuente | Conserva datos originales, regla y línea; esquema y reintento en pipeline.py |
| César | MajesDo63 | parche · rev_parche | Hallazgos explicados y código original | Parches y codigo_corregido | Correspondencia por hallazgo, compilación sin ejecutar y archivo limpio idéntico |
| Kevin | KevinAdmp | dictamen · rev_dictamen | Hallazgos explicados y parches propuestos | Estado, total, hallazgos con su cambio y resumen; reporte final armado por código | No omite, inventa ni cambia datos recibidos; resumen sin texto ajeno; coherencia de estado y total |

El motor tiene cuatro etapas: detectar → explicar → parche → dictamen.

## Versiones y reparto del Avance 1

| Parte | Responsable asignado | Versión o archivo |
|---|---|---|
| Detección del Lab 2 | Luis | rev_detectar.v3 |
| Explicación del Lab 2 | Alan | rev_explicar.v4 |
| Parche del Lab 2 | César | rev_parche.v4 |
| Dictamen y reporte final | Kevin | rev_dictamen.v2, dictamen.py y guia/a2_dictamen.py |
| Detección con contexto, buscador y citas/abstención | Luis | rev_detectar.v4, retrieval.py y controles.py |
| Explicación con fuente y 20 casos | Alan | rev_explicar.v5 y evals/v2-revisor.jsonl |
| Parche con contexto y contrato | César | rev_parche.v5 y contrato_calidad.yaml |
| Conexión del motor y comparación A/B/C/D | Luis | variante.py y guia/av1_configuraciones.py |

La comparación histórica usa A=1/1/1 y B/C/D=4/5/5. La nueva opción --cuatro-etapas fija A=1/1/1/1 y B/C/D=4/5/5/2. El esquema y reintento están presentes en las cuatro configuraciones. D añade controles de negocio, dominio, citas y saneo. La exclusión mínima del corpus confidencial está activa también en C; no completa los controles del Avance 2.

## Decisión de fusión

| Pieza | Decisión | Evidencia |
|---|---|---|
| Buscador | Luis | bitacora/a1_comparacion.json: semántico acierto@1 9/10 y @3 10/10; BM25 8/10 en ambos. Son resultados históricos. |
| Motor | Mantener Pipeline y el flujo integrado de cuatro etapas | tests/test_a2_pipeline.py, tests/test_lab2_revisor.py y tests/test_dictamen.py |
| Prompts | Conservar todas las versiones medidas sin editarlas | prompts/ y procedencia de bitacora/ |

## Cierre de cuatro etapas · 2026-11-05

Se integra documento-final-kevin en el PR #7 conservando los textos de Kevin. Se completaron las matrices reales del Lab 2: mejorada 6/6 e inicial 4/6 flujos completos. La comparación nueva quedó en 59/240 por cuota de ambas configuraciones autorizadas; faltan 181. Se conserva la firma de 71 archivos y se continúa con --cuatro-etapas --continuar. La etiqueta avance1-medicion-3-etapas conserva 5939a14; avance1 se moverá después del cierre. Los registros personales, los comentarios eliminados, el historial y agregar al profesor quedan fuera de estos cambios.

## Continuación de la medición · 2026-11-06

El corte anterior de 59/240 es histórico. Ahora están guardadas 180/240: A=60, B=60, C=60 y D=0. Las tres configuraciones autorizadas agotaron la cuota diaria; el proveedor indicó reinicio a las 02:00 de Ciudad de México del 6 de noviembre. Se eligió dejar preparada la continuación. Se verificaron 71 archivos y la conservación de las respuestas anteriores. No se modifica el código medido. El PR #7 sigue en borrador; avance1 se moverá al cerrar la comparación y la integración. Evidencia: bitacora/av1_cuatro_etapas_20261105/av1_estado_medicion.json y av1_verificacion_parcial_180.txt.

## Medición de cuatro etapas completada · 2026-11-06

Los cortes de 59/240 y 180/240 registrados arriba son antecedentes. Ahora se completaron las 240 ejecuciones en bitacora/av1_cuatro_etapas_20261105/. Se integra el documento de Kevin. El antecedente de tres etapas conserva su firma y la etiqueta avance1-medicion-3-etapas. Los registros personales permanecen a cargo de cada autor; no se modifican los comentarios eliminados ni el historial.

## Documento final · 2026-11-06

Por solicitud del usuario se actualiza la sección 11 con los resultados de cuatro etapas y se retiran referencias obsoletas del anexo. PDF: 12 páginas, 11 secciones. La medición y los archivos personales permanecen intactos. La fusión del PR #7 y la etiqueta avance1 se cerrarán después de obtener la aprobación requerida en GitHub.

## Referencias de la entrega · 2026-11-06

El PR #7 quedó fusionado en main, commit 279280f. La etiqueta de entrega es avance1 y debe identificar el commit final de main con estas correcciones documentales. Las 240 respuestas históricas de tres etapas se verifican con avance1-medicion-3-etapas; las 240 actuales de cuatro etapas verifican con el código integrado.
