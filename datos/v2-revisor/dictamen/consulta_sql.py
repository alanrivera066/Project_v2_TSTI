def buscar(cur, nombre):
    return cur.execute("SELECT * FROM usuarios WHERE nombre = '" + nombre + "'")
