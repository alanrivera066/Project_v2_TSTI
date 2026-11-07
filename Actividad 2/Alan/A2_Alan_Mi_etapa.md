# Mi etapa del flujo de FinNorte

Alan · Equipo 2 · v2-revisor

## 1 Mi etapa

Mi etapa asignada es explicar, con id rev_explicar. Recibe hallazgos de detectar y código y entrega los mismos hallazgos más explicacion. Mi responsabilidad es revisar y defender esta parte de la revisión de código. Realicé personalmente las tres repeticiones de v4 sobre reportes.py citadas en este documento. La preparación y revisión del texto contaron con asistencia de IA.

## 2 Mi prompt v1

En prompts/rev_explicar.v1.md identifico un rol, restricciones, datos de entrada, formato JSON y manejo de información faltante. Un ejemplo literal es: «Mantén exactamente id, regla y línea de cada uno.». La tarea se divide en etapas; el formato permite comprobar resultados antes de continuar. Si falta información, se pide reconocer el límite y evitar inventar datos.

## 3 Mi validación en código

Mi parte usa reglas.py y la validación de esquema de pipeline.py. Comprueba identidad de los hallazgos, descripción original, referencia a regla y línea, y ciertos identificadores completos. Es código porque debe rechazar el incumplimiento aunque el modelo ignore una instrucción.

Caso guardado: En la comparación real v3/v4, una repetición v3 no cumplió la nueva referencia de línea. Fuente: bitacora/lab2_cierre/casos/alan_trazabilidad__v3__r1.json. Se trata de un requisito ampliado, no de un fallo del contrato anterior.

Error guardado: «La explicación de H1 no identifica la línea 9; el texto debe ser trazable por sí solo».

## 4 Evidencia de ejecución

Extracto del caso real bitacora/lab2_cierre/casos/alan_trazabilidad__v4__r1.json:

```text
prompt: rev_explicar.v4
modelo: gemini-3.5-flash-lite
fecha UTC: 2026-11-01T05:58:25.929964+00:00
etapa: explicar; valida: True; intentos: 1
```

Mi fila en bitacora/av1_a2_matriz.md: explicar | rev_explicar.v4 | 3 hallazgos | válida True | 1 intento(s). La matriz se generó a partir de JSON históricos y no representa nuevas ejecuciones.

## 5 Consistencia

Las tres repeticiones v4 cumplieron el requisito de trazabilidad. Esto no exige texto idéntico ni acredita cobertura universal. Fuente: bitacora/lab2_cierre/metricas.json. Realicé personalmente estas tres ejecuciones; sus resultados se conservan como evidencia histórica en la bitácora.

## 6 Mi mejora y el antes y después

Regla y línea explícitas: 6/9 explicaciones en v3 y 9/9 en v4; casos válidos al primer intento: 2/3 y 3/3. Son tres repeticiones de reportes.py por versión con las mismas entradas previas.

La rúbrica llama a la mejora «v2». Aquí explico la evolución con los números reales de archivo: v1/v2 históricos, revisión v3 y, cuando corresponde, cierre v4. No renombro versiones medidas. En el Avance 1 se añade contexto con detectar v4, explicar v5 y parche v5. Los resultados históricos A/B/C/D de esa configuración de tres etapas están en bitacora/av1_cierre. La medición final de cuatro etapas está en bitacora/av1_cuatro_etapas_20261105 e incluye dictamen v2 en B/C/D. Estas mediciones evalúan el motor conjunto; el antes y después individual sigue siendo el histórico.

## 7 Mis commits y uso de IA

Participé en la revisión e integración del trabajo del equipo. Con mi cuenta alanrivera066 registré nueve aprobaciones en ocho propuestas de cambio (PR); el PR #5 tiene dos aprobaciones mías. Enlaces a las aprobaciones:

- [PR #1: Medición A/B/C/D con Gemini 3.1](https://github.com/alanrivera066/Project_v2_TSTI/pull/1#pullrequestreview-5786390171).
- [PR #2: Documento técnico con medición completa](https://github.com/alanrivera066/Project_v2_TSTI/pull/2#pullrequestreview-5787249625).
- [PR #3: Etapa dictamen y reporte final](https://github.com/alanrivera066/Project_v2_TSTI/pull/3#pullrequestreview-5795442743).
- [PR #5: Sección 11 del documento técnico](https://github.com/alanrivera066/Project_v2_TSTI/pull/5#pullrequestreview-5798642848).
- [PR #7: Integración y medición de cuatro etapas](https://github.com/alanrivera066/Project_v2_TSTI/pull/7#pullrequestreview-5798680749).
- [PR #8: Correcciones de referencias de entrega](https://github.com/alanrivera066/Project_v2_TSTI/pull/8#pullrequestreview-5798822747).
- [PR #10: Actualización de Mi etapa de César](https://github.com/alanrivera066/Project_v2_TSTI/pull/10#pullrequestreview-5808488137).
- [PR #17: Actualización de equipo.md](https://github.com/alanrivera066/Project_v2_TSTI/pull/17#pullrequestreview-5808719906).

También incorporé los cambios de integración de cuatro etapas ([commit 279280f](https://github.com/alanrivera066/Project_v2_TSTI/commit/279280f7ad7c0d36a0fa027a3b0c7028899144ea)) y de referencias de entrega ([commit b5cbc0b](https://github.com/alanrivera066/Project_v2_TSTI/commit/b5cbc0bb06e8795ef9d2921567d65656b56b8274)).

Utilicé ChatGPT mediante Codex para comprender mi etapa, revisar las evidencias y preparar ajustes al documento. Acepté el apoyo para localizar y comprobar los resultados guardados y mis aportaciones en GitHub. Pedí conservar las secciones existentes y corregir los avisos de borrador, los pendientes y los datos de mi participación. La revisión asistida contrastó el documento con el prompt, las validaciones en código, las bitácoras y los registros de aprobación. El registro personal en ai_log.md se actualizará por separado.
