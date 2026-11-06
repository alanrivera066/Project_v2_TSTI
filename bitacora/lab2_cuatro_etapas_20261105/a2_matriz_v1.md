# Laboratorio 2: matriz del revisor

Ejecución con proveedor real, sin Mini-RAG.
Proveedor: gemini. Modelo: gemini-3.1-flash-lite.

| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |
|---|---|---|---|---|---|---|---|
| transferencias.py | inicial | detectar | rev_detectar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 2 | [] |
| transferencias.py | inicial | explicar | rev_explicar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 2 | [] |
| transferencias.py | inicial | parche | rev_parche.v1 | 5 parches; archivo de 17 líneas | True | 1 | [] |
| transferencias.py | inicial | dictamen | rev_dictamen.v1 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| tokens.py | inicial | detectar | rev_detectar.v1 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | explicar | rev_explicar.v1 | Salida inválida: {"hallazgos": [{"id": "H1", "regla": "SEC-09", "linea": 6, "descripcion": "Uso de yaml.load inseguro | False | 2 | ['La explicación de H1 debe identificar su regla SEC'] |
| limites.py | inicial | detectar | rev_detectar.v1 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | explicar | rev_explicar.v1 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | parche | rev_parche.v1 | Salida inválida: {"parches": [], "codigo_corregido": "from decimal import Decimal, ROUND_HALF_EVEN\n\nLIMITE_NIVEL_1  | False | 2 | ['Sin hallazgos se debe conservar exactamente el código original'] |
| transferencias.py | 1 | detectar | rev_detectar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-03 L12, H4 SEC-07 L10, H5 SEC-02 L11 | True | 2 | [] |
| transferencias.py | 1 | explicar | rev_explicar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-03 L12, H4 SEC-07 L10, H5 SEC-02 L11 | True | 2 | [] |
| transferencias.py | 1 | parche | rev_parche.v1 | 5 parches; archivo de 20 líneas | True | 1 | [] |
| transferencias.py | 1 | dictamen | rev_dictamen.v1 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| transferencias.py | 2 | detectar | rev_detectar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 2 | [] |
| transferencias.py | 2 | explicar | rev_explicar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 2 | [] |
| transferencias.py | 2 | parche | rev_parche.v1 | 5 parches; archivo de 20 líneas | True | 1 | [] |
| transferencias.py | 2 | dictamen | rev_dictamen.v1 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| transferencias.py | 3 | detectar | rev_detectar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 2 | [] |
| transferencias.py | 3 | explicar | rev_explicar.v1 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 2 | [] |
| transferencias.py | 3 | parche | rev_parche.v1 | 5 parches; archivo de 19 líneas | True | 1 | [] |
| transferencias.py | 3 | dictamen | rev_dictamen.v1 | con_hallazgos: 5 hallazgos | True | 1 | [] |

Consistencia (transferencias.py x 3), reglas y líneas: [[('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)], [('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)], [('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)]]
Tres flujos completos y mismos hallazgos: True.
La coincidencia no demuestra exactitud; revisar el contenido y los errores en las trazas.
