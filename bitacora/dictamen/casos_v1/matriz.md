# Dictamen: casos con rev_dictamen.v1

Ejecución con proveedor real.
Proveedor: gemini. Modelo: gemini-3.1-flash-lite. Fecha UTC: 2026-11-06T02:22:10.474391+00:00.
Estado: completo.

| Caso | Rep. | Archivo | Esperado | Detectado | Reporte | Coincide | Intentos dictamen | Primer intento válido | Errores del validador |
|---|---|---|---|---|---|---|---|---|---|
| d1 | unica | limites.py | - | - | sin hallazgos | True | 1 | True | ninguno |
| d2 | unica | limpio_enmascarado.py | - | - | sin hallazgos | True | 1 | True | ninguno |
| d3 | unica | credencial.py | SEC-01 | SEC-01 | hallazgos | True | 1 | True | ninguno |
| d4 | unica | consulta_sql.py | SEC-02 | SEC-02 | hallazgos | True | 1 | True | ninguno |
| d5 | unica | deserializar.py | SEC-09 | SEC-09 | hallazgos | True | 1 | True | ninguno |
| d6 | unica | dos_problemas.py | SEC-01, SEC-02 | SEC-01, SEC-02 | hallazgos | True | 1 | True | ninguno |

Flujos: 6. Reporte correcto para lo esperado: 6/6. Dictamen válido al primer intento: 6/6. Revisiones fallidas: 0.
