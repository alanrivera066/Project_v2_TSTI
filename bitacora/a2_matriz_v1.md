# Laboratorio 2: matriz histórica de las tres etapas publicadas

Importada de ejecuciones reales anteriores. Se excluye la cuarta etapa. No es una ejecución nueva de esta copia.
Proveedor: gemini; modelo: gemini-3.1-flash-lite; fecha original: 2026-11-01T02:44:53.894203+00:00.

| Entrada | Repetición | Etapa | Prompt | Artefacto | Válida | Intentos | Errores |
|---|---|---|---|---|---|---|---|
| transferencias.py | inicial | detectar | rev_detectar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | inicial | explicar | rev_explicar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | inicial | parche | rev_parche.v1 | 4 parches; archivo de 20 líneas | True | 1 | [] |
| tokens.py | inicial | detectar | rev_detectar.v1 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | explicar | rev_explicar.v1 | 1 hallazgos: H1 SEC-09 L6 | True | 1 | [] |
| tokens.py | inicial | parche | rev_parche.v1 | 1 parches; archivo de 10 líneas | True | 1 | [] |
| limites.py | inicial | detectar | rev_detectar.v1 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | explicar | rev_explicar.v1 | 0 hallazgos:  | True | 1 | [] |
| limites.py | inicial | parche | rev_parche.v1 | Salida inválida: {"parches": [], "codigo_corregido": "from decimal import Decimal, ROUND_HALF_EVEN\n\nLIMITE_NIVEL_1  | False | 2 | ['Sin hallazgos se debe conservar exactamente el código original'] |
| transferencias.py | 1 | detectar | rev_detectar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 1 | explicar | rev_explicar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-02 L11, H4 SEC-07 L10 | True | 1 | [] |
| transferencias.py | 1 | parche | rev_parche.v1 | 4 parches; archivo de 20 líneas | True | 1 | [] |
| transferencias.py | 2 | detectar | rev_detectar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | 2 | explicar | rev_explicar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | 2 | parche | rev_parche.v1 | 4 parches; archivo de 20 líneas | True | 1 | [] |
| transferencias.py | 3 | detectar | rev_detectar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | 3 | explicar | rev_explicar.v1 | 4 hallazgos: H1 SEC-01 L3, H2 SEC-02 L8, H3 SEC-07 L10, H4 SEC-02 L11 | True | 1 | [] |
| transferencias.py | 3 | parche | rev_parche.v1 | 4 parches; archivo de 20 líneas | True | 1 | [] |

Datos completos de estas etapas: a2_trazabilidad_v1.json. La procedencia y el hash de la fuente están dentro del JSON.
Los errores históricos se conservan: una salida inválida no se convierte en éxito al importar.
