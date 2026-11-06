# Laboratorio 2: matriz del revisor

Ejecución con proveedor real, sin Mini-RAG.
Proveedor: gemini. Modelo: gemini-3.1-flash-lite.

| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |
|---|---|---|---|---|---|---|---|
| transferencias.py | inicial | detectar | rev_detectar.v3 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | inicial | explicar | rev_explicar.v4 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | inicial | parche | rev_parche.v4 | 5 parches; archivo de 16 líneas | True | 1 | [] |
| transferencias.py | inicial | dictamen | rev_dictamen.v2 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| tokens.py | inicial | detectar | rev_detectar.v3 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | explicar | rev_explicar.v4 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | parche | rev_parche.v4 | 1 parches; archivo de 10 líneas | True | 1 | [] |
| tokens.py | inicial | dictamen | rev_dictamen.v2 | con_hallazgos: 1 hallazgos | True | 1 | [] |
| limites.py | inicial | detectar | rev_detectar.v3 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | explicar | rev_explicar.v4 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | parche | rev_parche.v4 | 0 parches; archivo de 12 líneas | True | 1 | [] |
| limites.py | inicial | dictamen | rev_dictamen.v2 | sin_hallazgos: 0 hallazgos | True | 1 | [] |
| transferencias.py | 1 | detectar | rev_detectar.v3 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 1 | explicar | rev_explicar.v4 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 1 | parche | rev_parche.v4 | 5 parches; archivo de 17 líneas | True | 1 | [] |
| transferencias.py | 1 | dictamen | rev_dictamen.v2 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| transferencias.py | 2 | detectar | rev_detectar.v3 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 2 | explicar | rev_explicar.v4 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 2 | parche | rev_parche.v4 | 5 parches; archivo de 16 líneas | True | 1 | [] |
| transferencias.py | 2 | dictamen | rev_dictamen.v2 | con_hallazgos: 5 hallazgos | True | 1 | [] |
| transferencias.py | 3 | detectar | rev_detectar.v3 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 3 | explicar | rev_explicar.v4 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-03 L12, H5 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 3 | parche | rev_parche.v4 | 5 parches; archivo de 16 líneas | True | 1 | [] |
| transferencias.py | 3 | dictamen | rev_dictamen.v2 | con_hallazgos: 5 hallazgos | True | 1 | [] |

Consistencia (transferencias.py x 3), reglas y líneas: [[('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)], [('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)], [('SEC-01', 3), ('SEC-02', 8), ('SEC-02', 11), ('SEC-03', 12), ('SEC-07', 10)]]
Tres flujos completos y mismos hallazgos: True.
La coincidencia no demuestra exactitud; revisar el contenido y los errores en las trazas.
