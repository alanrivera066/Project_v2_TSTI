# Dictamen: comparar con rev_dictamen.v1

Ejecución con proveedor real.
Proveedor: gemini. Modelo: gemini-3.1-flash-lite. Fecha UTC: 2026-11-06T02:26:55.814958+00:00.
Estado: completo.

| Caso | Rep. | Archivo | Esperado | Detectado | Reporte | Coincide | Intentos dictamen | Primer intento válido | Errores del validador |
|---|---|---|---|---|---|---|---|---|---|
| d6 | inicial | dos_problemas.py | SEC-01, SEC-02 | SEC-01, SEC-02 | hallazgos | True | 2 | False | El resumen agrega texto que no está en los datos recibidos: seguridad |
| d3 | inicial | credencial.py | SEC-01 | SEC-01 | hallazgos | True | 2 | False | El resumen agrega texto que no está en los datos recibidos: detalla, medida, mitigacion, propone, reporte, variables |
| d1 | inicial | limites.py | - | - | sin hallazgos | True | 1 | True | ninguno |
| d6 | 1 | dos_problemas.py | SEC-01, SEC-02 | SEC-01, SEC-02 | hallazgos | True | 2 | False | El resumen agrega texto que no está en los datos recibidos: seguridad |
| d6 | 2 | dos_problemas.py | SEC-01, SEC-02 | SEC-01, SEC-02 | hallazgos | True | 2 | False | El resumen agrega texto que no está en los datos recibidos: prevencion |
| d6 | 3 | dos_problemas.py | SEC-01, SEC-02 | SEC-01, SEC-02 | hallazgos | True | 2 | False | El resumen agrega texto que no está en los datos recibidos: seguridad |

Flujos: 6. Reporte correcto para lo esperado: 6/6. Dictamen válido al primer intento: 1/6. Revisiones fallidas: 0.
Repetición de d6: [['hallazgos', [['SEC-01', 1], ['SEC-02', 5]]], ['hallazgos', [['SEC-01', 1], ['SEC-02', 5]]], ['hallazgos', [['SEC-01', 1], ['SEC-02', 5]]]]; iguales: True; redacciones distintas del resumen: 3.
