# Laboratorio 2: matriz histórica de las tres etapas publicadas

Importada de ejecuciones reales anteriores. Se excluye la cuarta etapa. No es una ejecución nueva de esta copia.
Proveedor: gemini; modelo: gemini-3.1-flash-lite; fecha original: 2026-11-01T02:49:36.169218+00:00.

| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |
|---|---|---|---|---|---|---|---|
| transferencias.py | inicial | detectar | rev_detectar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | inicial | explicar | rev_explicar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | inicial | parche | rev_parche.v2 | 5 parches; archivo de 17 líneas | True | 1 | [] |
| tokens.py | inicial | detectar | rev_detectar.v2 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | explicar | rev_explicar.v2 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | parche | rev_parche.v2 | 1 parches; archivo de 10 líneas | True | 1 | [] |
| limites.py | inicial | detectar | rev_detectar.v2 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | explicar | rev_explicar.v2 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | parche | rev_parche.v2 | 0 parches; archivo de 12 líneas | True | 1 | [] |
| transferencias.py | 1 | detectar | rev_detectar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 1 | explicar | rev_explicar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 1 | parche | rev_parche.v2 | 5 parches; archivo de 18 líneas | True | 1 | [] |
| transferencias.py | 2 | detectar | rev_detectar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 2 | explicar | rev_explicar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 2 | parche | rev_parche.v2 | 5 parches; archivo de 16 líneas | True | 1 | [] |
| transferencias.py | 3 | detectar | rev_detectar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 3 | explicar | rev_explicar.v2 | 5 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11, H5 SEC-03 L12 | True | 1 | [] |
| transferencias.py | 3 | parche | rev_parche.v2 | 5 parches; archivo de 17 líneas | True | 1 | [] |

Datos completos de estas etapas: a2_trazabilidad.json. La procedencia y el hash de la fuente están dentro del JSON.
Los errores históricos se conservan: una salida inválida no se convierte en éxito al importar.
