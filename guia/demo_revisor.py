"""Respuestas preparadas para probar el encadenamiento. NO es un detector de código."""


def respuestas_para(nombre, codigo):
    candidatos = {
        "transferencias.py": [("SEC-01", 3, "Credencial escrita en el código"),
                              ("SEC-02", 8, "SQL mediante f-string"),
                              ("SEC-02", 11, "SQL mediante concatenación"),
                              ("SEC-03", 12, "Registro con CLABE completa")],
        "tokens.py": [("SEC-09", 6, "Deserialización YAML insegura")],
        "limites.py": [],
    }[nombre]
    hallazgos = [dict(id=f"H{i}", regla=r, linea=l, descripcion=d)
                 for i, (r, l, d) in enumerate(candidatos, 1)]
    explicados = [dict(h, explicacion=f"{h['regla']}, línea {h['linea']}: ejemplo preparado; no es una inferencia del modelo.")
                  for h in hallazgos]
    corregido = codigo
    if nombre == "tokens.py":
        corregido = codigo.replace("yaml.load(texto)", "yaml.safe_load(texto)")
    elif nombre == "transferencias.py":
        corregido = codigo.replace("import sqlite3", "import sqlite3\nimport os")
        original = next(l for l in codigo.splitlines() if l.startswith("API_KEY ="))
        corregido = corregido.replace(original, 'API_KEY = os.environ["API_KEY"]')
        corregido = corregido.replace('cur.execute(f"SELECT saldo FROM cuentas WHERE id = \'{origen_id}\'")',
                                     'cur.execute("SELECT saldo FROM cuentas WHERE id = ?", (origen_id,))')
        original_sql = next(l for l in codigo.splitlines() if 'UPDATE cuentas' in l)
        corregido = corregido.replace(original_sql, '        cur.execute("UPDATE cuentas SET saldo = saldo - ? WHERE id = ?", (monto, origen_id))')
        corregido = corregido.replace('{destino_clabe}', '{str(destino_clabe)[-4:]}')
    parches = [dict(id=h["id"], regla=h["regla"], linea=h["linea"], cambio="Corrección preparada para la demostración")
               for h in hallazgos]
    cambios = {p["id"]: p["cambio"] for p in parches}
    dictamen = {"estado": "con_hallazgos" if hallazgos else "sin_hallazgos", "total_hallazgos": len(hallazgos),
                "hallazgos": [dict(h, cambio=cambios[h["id"]]) for h in explicados],
                "resumen": (f"Se encontraron {len(hallazgos)} hallazgos: "
                            + "; ".join(f"{h['regla']} en línea {h['linea']}" for h in hallazgos)
                            + ". Los parches son propuestas.") if hallazgos else "sin hallazgos"}
    return {
        "Eres revisor de seguridad": {"hallazgos": hallazgos},
        "Eres revisor técnico": {"hallazgos": explicados},
        "Eres desarrollador Python": {"parches": parches, "codigo_corregido": corregido},
        "Eres redactor técnico": dictamen,
    }
