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
| Kevin | KevinAdmp | PENDIENTE · Kevin | Pendiente | Pendiente | Pendiente |

El motor publicado tiene tres etapas: detectar → explicar → parche. La cuarta etapa, su reporte, sus seis pruebas y la integración del documento final quedan pendientes y fuera de esta publicación.

## Versiones y reparto del Avance 1

| Parte | Responsable asignado | Versión o archivo |
|---|---|---|
| Detección del Lab 2 | Luis | rev_detectar.v3 |
| Explicación del Lab 2 | Alan | rev_explicar.v4 |
| Parche del Lab 2 | César | rev_parche.v4 |
| Detección con contexto, buscador y citas/abstención | Luis | rev_detectar.v4, retrieval.py y controles.py |
| Explicación con fuente y 20 casos | Alan | rev_explicar.v5 y evals/v2-revisor.jsonl |
| Parche con contexto y contrato | César | rev_parche.v5 y contrato_calidad.yaml |
| Conexión del motor y comparación A/B/C/D | Compartido | variante.py y guia/av1_configuraciones.py |

A usa 1/1/1; B, C y D usan 4/5/5. El esquema y reintento están presentes en las cuatro configuraciones. D añade controles de negocio, dominio, citas y saneo. La exclusión mínima del corpus confidencial está activa también en C; no completa los controles del Avance 2.

## Decisión de fusión

| Pieza | Decisión | Evidencia |
|---|---|---|
| Buscador | Mantener el buscador de Luis | bitacora/a1_comparacion.json: semántico acierto@1 9/10 y @3 10/10; BM25 8/10 en ambos. Son resultados históricos. |
| Motor | Mantener Pipeline y el flujo de tres etapas | tests/test_a2_pipeline.py y tests/test_lab2_revisor.py |
| Prompts | Conservar todas las versiones medidas sin editarlas | prompts/ y procedencia de bitacora/ |
| Evidencias | Publicar el historial sin la cuarta etapa y medir por separado el código corregido | bitacora/procedencia_importacion_20261105.json y bitacora/av1_publicado_20261105/ |

## Registro de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-11-01 | Preparar un motor de tres etapas | Alcance solicitado por el usuario; Kevin pendiente. |
| 2026-11-04 | Publicar las partes de Luis, Alan y César con sus cuentas autorizadas | Autorización del usuario. Las fechas de publicación son reales; el trabajo se preparó con asistencia de IA. |
| 2026-11-05 | Restaurar guía común, pruebas oficiales, matrices y trazas de las tres etapas | Corregir las omisiones detectadas sin incluir la parte pendiente. |
| 2026-11-05 | Corregir r06/r09 y validar estructuralmente el archivo limpio | Evitar texto corrupto y falsos éxitos basados solo en una frase. |
| 2026-11-05 | Separar los resultados históricos de la nueva medición | El código publicado cambió al excluir la cuarta etapa; una firma distinta requiere evidencia nueva. |
| 2026-11-05 | Dejar los registros personales de IA como PENDIENTE | Instrucción expresa del usuario; no se inventan usos ni revisiones personales. |

## Acuerdos de publicación

Se verifica la rama remota antes de publicar y no se sobrescriben cambios ajenos. Las llaves permanecen fuera de Git. Las pruebas sin red comprueban funcionamiento; las métricas de modelo requieren API real y bitácora guardada. No se da por realizada una revisión humana que no conste.
