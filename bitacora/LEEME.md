# Guía de bitácora: resultados finales e historial

Revisión documental del 6 de noviembre de 2026 (Ciudad de México), sobre el commit `43f284e01f3d504b3a5a65df9152343382b5c565`. Esta guía aclara las referencias; no registra nuevas llamadas al modelo ni cambia las entradas, respuestas, métricas o firmas de las pruebas.

## Resultados finales de cuatro etapas

- **Medición A/B/C/D:** [comparación final](av1_cuatro_etapas_20261105/av1_comparacion.md), [estado completo](av1_cuatro_etapas_20261105/av1_estado_medicion.json) y [verificación](av1_cuatro_etapas_20261105/av1_verificacion.txt). Contiene 240 respuestas: 20 casos por tres repeticiones y cuatro configuraciones. La firma corresponde a 71 archivos. La configuración D cumple siete de ocho metas; la latencia continúa por encima de la meta.
- **Laboratorio 2:** [resumen](lab2_cuatro_etapas_20261105/a2_resumen.json), [matriz inicial](lab2_cuatro_etapas_20261105/a2_matriz_v1.md) y [matriz mejorada](lab2_cuatro_etapas_20261105/a2_matriz.md). La versión inicial tiene cuatro de seis flujos completos y la mejorada seis de seis; los fallos iniciales se conservan.
- **Dictamen:** [comparación de versiones](dictamen/comparacion.md). Distingue los cambios del prompt de los cambios del validador, con sus casos y reintentos.

## Mediciones anteriores y cortes parciales

| Ubicación | Qué conserva | Cómo interpretarla |
|---|---|---|
| [av1_cierre](av1_cierre/LEEME.md) | 240 respuestas históricas del 2 de noviembre, con tres etapas. | Antecedente; no es la medición final de cuatro etapas. |
| [av1_publicado_20261105](av1_publicado_20261105/av1_estado_medicion.json) | Intento interrumpido con Gemini 3.5 y 62 respuestas retenidas. | El nombre de la carpeta no implica que la medición esté completa. |
| [av1_gemini31_20261105](av1_gemini31_20261105/av1_comparacion.md) | Medición posterior de tres etapas, completada con 240 respuestas. | Su estado final está en [av1_estado_medicion.json](av1_gemini31_20261105/av1_estado_medicion.json). El archivo [av1_estado_verificado.json](av1_gemini31_20261105/av1_estado_verificado.json) conserva un corte anterior de 163/240, con 77 faltantes; no es el cierre. |
| [Corte de cuatro etapas 180/240](av1_cuatro_etapas_20261105/av1_comparacion_parcial_180.md) | A, B y C completas antes de terminar D. | Se conserva como corte parcial; lo supera el estado final de 240/240 enlazado arriba. |
| Archivos `av1_verificacion_parcial*.txt`, `av1_interrupcion.json` y `ejecucion_abcd_*.txt` | Interrupciones y reanudaciones de cada medición. | Sus avisos de medición pendiente describen ese momento, no necesariamente el estado final. |

Las menciones de dictamen o de Kevin pendiente en las mediciones de tres etapas describen una etapa que todavía no se ejecutaba allí. La integración posterior está en la medición final de cuatro etapas. Se conservan los indicadores originales dentro de JSON y trazas para mantener la evidencia histórica.

## Registros documentales y personales

Los archivos `av1_documentacion_*.json`, `av1_revision_*.json` y `av1_verificacion_publicado_20261105.json` describen revisiones fechadas. Expresiones como «registros personales pendientes», «borrador» o «medición pendiente» se refieren al corte registrado. Por ejemplo, `av1_documentacion_final_20261106.json` fue generado a las 09:51 UTC del 6 de noviembre y precede a las actualizaciones personales de Alan.

Para Alan, [Mi etapa se actualizó en el PR #19](https://github.com/alanrivera066/Project_v2_TSTI/pull/19) y [su registro personal de IA en el PR #20](https://github.com/alanrivera066/Project_v2_TSTI/pull/20); ambos fueron integrados. El registro de uso de IA se consulta en [ai_log.md](../ai_log.md). Estos cambios no acreditan por sí solos que los registros de los demás integrantes estén completos.

El estado de una revisión o aprobación de GitHub debe comprobarse en el PR correspondiente. Los registros de bitácora no certifican la entrega en Canvas, la coevaluación ni el estado de la etiqueta `avance1`.

## Texto dentro de las pruebas

«Mini-RAG pendiente del Laboratorio 3», comentarios `TODO`, decisiones de negocio pendientes y respuestas con «NO ESPECIFICADO» pueden formar parte de las entradas o salidas originales. «Sin verificar» también puede describir una vulnerabilidad del código analizado. Esas expresiones no se sustituyen por «completo»: hacerlo cambiaría la evidencia de la prueba.
