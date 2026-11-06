API_KEY = "sk_live_sintetica_1234"


def buscar(cur, nombre):
    return cur.execute("SELECT * FROM usuarios WHERE nombre = '" + nombre + "'")
