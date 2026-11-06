# Dictamen: comparación de versiones

Modelo: gemini gemini-3.1-flash-lite. Solo cambia rev_dictamen; detectar v3, explicar v4 y parche v4 se conservan.

| Medición | Prompt | Validador | Flujos | Reporte correcto | Válido al primer intento | Redacciones en 3 repeticiones | Revisiones fallidas |
|---|---|---|---:|---:|---:|---:|---:|
| comparar_v1 | rev_dictamen.v1 | inicial | 6 | 6/6 | 6/6 | 3 | 0 |
| comparar_v1_regla_resumen | rev_dictamen.v1 | con regla de resumen | 6 | 6/6 | 1/6 | 3 | 0 |
| comparar_v2 | rev_dictamen.v2 | con regla de resumen | 6 | 6/6 | 6/6 | 1 | 0 |
| casos_v1 | rev_dictamen.v1 | inicial | 6 | 6/6 | 6/6 | - | 0 |
| casos_v2 | rev_dictamen.v2 | con regla de resumen | 6 | 6/6 | 6/6 | - | 0 |

comparar_v1 y comparar_v1_regla_resumen usan el mismo prompt: la diferencia es la regla agregada al validador. La comparación antes y después es comparar_v1_regla_resumen contra comparar_v2.

Son seis flujos por versión con archivos pequeños. Una plantilla reduce la variación del resumen; no demuestra mejor detección, que depende de etapas anteriores.
