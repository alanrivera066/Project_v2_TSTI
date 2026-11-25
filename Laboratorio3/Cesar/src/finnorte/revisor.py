"""Preanálisis AST conservador. Nunca ejecuta el código o sus parches."""
from __future__ import annotations
import ast
import re

SEVERIDAD = {1:"critica",2:"critica",3:"alta",4:"alta",5:"media",6:"alta",7:"alta",8:"critica",9:"critica",10:"baja"}
DETALLES = {
1: ("Secreto literal; usar variables de entorno o gestor y revocar la credencial.",
    "import os\nAPI_KEY = os.environ['API_KEY']"),
2: ("SQL interpolado o concatenado; usar parámetros.",
    "cursor.execute('SELECT saldo FROM cuentas WHERE id = ?', (origen_id,))"),
3: ("PII completa en print/log; registrar identificadores o enmascarar.",
    "log.info('operacion completada; trace_id=%s', trace_id)"),
4: ("Operación monetaria sin validación explícita del monto positivo.",
    "from decimal import Decimal\nif Decimal(str(monto)) <= 0:\n    raise ValueError('Monto no positivo')"),
5: ("Excepción amplia ignorada; registrar y responder un error genérico. Usar timeout finito en HTTP.",
    "import logging\nlogging.getLogger(__name__).error('Fallo de la operacion')"),
6: ("Criptografía insegura: sustituir md5 por PBKDF2 con sal, random por secrets y == por hmac.compare_digest.",
    "import secrets\ncodigo = secrets.randbelow(900000) + 100000"),
7: ("Dinero con float/round; usar Decimal y ROUND_HALF_EVEN al final.",
    "from decimal import Decimal, ROUND_HALF_EVEN\nimporte = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)"),
8: ("Recurso por ID externo sin comprobación visible de propiedad.",
    "if cuenta['cliente_id'] != usuario['id']:\n    raise PermissionError('Acceso denegado')"),
9: ("Deserialización/comandos inseguros: pickle, yaml.load, eval/exec o shell=True.",
    "import json\nreporte = json.loads(datos_texto)"),
10: ("Función extensa, compleja o con parámetros de una letra.",
     "LIMITE_OPERACIONES = 10"),
}
def nombre(n):
    if isinstance(n, ast.Name): return n.id
    if isinstance(n, ast.Attribute): return nombre(n.value) + "." + n.attr
    return ""

def analizar(codigo):
    """Señales verificables; no sustituye auditoría ni análisis de flujo de datos."""
    arbol = ast.parse(codigo)
    hallazgos, alias, asignadas = {}, {}, {}
    def agregar(regla, nodo):
        clave = (f"SEC-{regla:02d}", nodo.lineno)
        explicacion, parche = DETALLES[regla]
        hallazgos[clave] = dict(regla=clave[0], linea=nodo.lineno,
            severidad=SEVERIDAD[regla], explicacion=explicacion, parche=parche)
        if regla == 1:
            objetivo = nodo.targets[0] if isinstance(nodo, ast.Assign) else nodo.target
            if isinstance(objetivo, ast.Name):
                hallazgos[clave]["parche"] = f"import os\n{objetivo.id} = os.environ[{objetivo.id!r}]"
        if regla == 6 and isinstance(nodo, ast.Call):
            fn = nombre(nodo.func)
            if fn.endswith(("md5", "sha1", "sha256")) or "password" in ast.unparse(nodo):
                hallazgos[clave]["severidad"] = "critica" if fn.endswith(("md5", "sha1")) else "alta"
                hallazgos[clave]["parche"] = "import hashlib, secrets\nsal = secrets.token_bytes(16)\nhuella = hashlib.pbkdf2_hmac('sha256', password.encode(), sal, 600000)\n# Guardar sal y huella por usuario; migrar y verificar las contraseñas existentes."
        if regla == 6 and isinstance(nodo, ast.Compare):
            hallazgos[clave]["parche"] = "import hmac\nvalido = hmac.compare_digest(token, guardado)\n# Conservar además la comprobación de expiración."
        if regla == 9 and isinstance(nodo, ast.Call):
            fn = nombre(nodo.func)
            if fn == "yaml.load":
                hallazgos[clave]["parche"] = "import yaml\nconfig = yaml.safe_load(texto)"
            elif fn.startswith("subprocess."):
                hallazgos[clave]["parche"] = "import subprocess\nsubprocess.run(['zip', 'reportes.zip', '--', nombre_archivo], check=True)\n# Validar nombre_archivo y su ruta antes de ejecutar."
    for n in ast.walk(arbol):
        if isinstance(n, ast.Import): alias.update({a.asname or a.name:a.name for a in n.names})
        if isinstance(n, ast.ImportFrom): alias.update({a.asname or a.name:f"{n.module}.{a.name}" for a in n.names})
    def llamada(n):
        primero, *resto = nombre(n).split(".")
        return ".".join([alias.get(primero,primero),*resto])
    for n in ast.walk(arbol):
        if isinstance(n,(ast.Assign,ast.AnnAssign)):
            objetivos = n.targets if isinstance(n,ast.Assign) else [n.target]
            for obj in objetivos:
                if isinstance(obj,ast.Name):
                    asignadas[obj.id] = n.value
                    if re.search(r"(api_?key|password|passwd|secret|token)",obj.id,re.I) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str) and n.value.value:
                        agregar(1,n)
    for f in [n for n in ast.walk(arbol) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]:
        fuente = ast.get_source_segment(codigo,f) or ""
        dinero = bool(re.search(r"(monto|saldo|importe|comisi|transferir|precio)",fuente,re.I)) or f.name == "calc"
        args = f.args.posonlyargs + f.args.args + f.args.kwonlyargs
        complejidad = 1 + sum(isinstance(n,(ast.If,ast.For,ast.While,ast.ExceptHandler,ast.IfExp)) for n in ast.walk(f))
        if f.end_lineno-f.lineno+1 > 40 or complejidad > 10 or any(len(a.arg)==1 for a in args): agregar(10,f)
        if "transferir" in f.name and any(a.arg=="monto" for a in args):
            if not any("monto" in ast.unparse(n) and re.search(r"[<>]=?\s*0",ast.unparse(n)) for n in ast.walk(f) if isinstance(n,ast.Compare)): agregar(4,f)
        if any("usuario" in a.arg for a in args) and "cuenta_id" in fuente and "DB[" in fuente:
            if not re.search(r"(propietario|cliente_id|usuario_id|owner_id).*?(==|!=)",fuente): agregar(8,f)
        for n in ast.walk(f):
            if isinstance(n,ast.Call):
                fn = llamada(n.func)
                if fn in ("hashlib.md5","hashlib.sha1","hashlib.sha256") and re.search(r"(password|passwd|contrase)",fuente,re.I): agregar(6,n)
                if fn.startswith("random.") and re.search(r"(token|codigo|otp|password)",fuente,re.I): agregar(6,n)
                if dinero and fn in ("float","round"): agregar(7,n)
            if isinstance(n,ast.Compare) and any(isinstance(op,ast.Eq) for op in n.ops) and "token" in ast.unparse(n).lower(): agregar(6,n)
    for n in ast.walk(arbol):
        if isinstance(n,ast.ExceptHandler) and (n.type is None or nombre(n.type) in ("Exception","BaseException")) and all(isinstance(x,ast.Pass) for x in n.body): agregar(5,n)
        if not isinstance(n,ast.Call): continue
        fn = llamada(n.func)
        if fn.endswith(".execute") and n.args:
            q = n.args[0]
            if isinstance(q,ast.Name): q = asignadas.get(q.id,q)
            if isinstance(q,(ast.JoinedStr,ast.BinOp)) or isinstance(q,ast.Call) and nombre(q.func).endswith(".format"): agregar(2,n)
        if fn in ("pickle.loads","pickle.load"): agregar(9,n)
        if fn=="yaml.load" and not any(k.arg=="Loader" and llamada(k.value) in ("yaml.SafeLoader","yaml.CSafeLoader") for k in n.keywords): agregar(9,n)
        if fn in ("eval","exec","os.system") and n.args and not isinstance(n.args[0],ast.Constant): agregar(9,n)
        if fn.startswith("subprocess.") and any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords): agregar(9,n)
        if fn=="print" or fn.split(".")[-1] in ("info","warning","error","debug","exception"):
            texto=ast.unparse(n)
            if re.search(r"(password|token|correo|telefono|clabe|curp|tarjeta)",texto,re.I) and "[-4:]" not in texto and "enmascar" not in texto: agregar(3,n)
    return sorted(hallazgos.values(),key=lambda h:(h["linea"],h["regla"]))

def validar_hallazgos(salida,contexto):
    permitidos={(h["regla"],h["linea"]) for h in contexto.get("senales",[])}
    vistos,errores=set(),[]
    if not isinstance(salida,dict): return ["Se espera un objeto"]
    for h in salida.get("hallazgos",[]):
        clave=(h.get("regla"),h.get("linea"))
        if clave not in permitidos: errores.append("Hallazgo sin señal estática o línea válida")
        if clave in vistos: errores.append("Hallazgo duplicado")
        vistos.add(clave)
    if vistos!=permitidos: errores.append("El resultado debe cubrir todas las señales estáticas")
    if bool(salida.get("hallazgos")) != (salida.get("estado") == "hallazgos"):
        errores.append("Estado inconsistente con los hallazgos")
    por_clave = {(h["regla"],h["linea"]):h for h in contexto.get("senales",[])}
    for h in salida.get("hallazgos",[]):
        original = por_clave.get((h.get("regla"),h.get("linea")))
        if original and h.get("severidad") != original["severidad"]:
            errores.append("Severidad incompatible con la señal verificada")
    return errores

def validar_parches(salida,contexto):
    errores=validar_hallazgos(salida,contexto)
    for h in salida.get("hallazgos",[]):
        try:
            if not h.get("parche","").strip(): raise SyntaxError("Parche vacío")
            ast.parse(h["parche"])
        except (SyntaxError,TypeError): errores.append("Parche Python no compilable")
    return errores

def simular(prompt):
    """Fixture fake basada en señales AST. No consulta resultados esperados."""
    import json
    if "DATOS_JSON\n" not in prompt: return None
    d=json.loads(prompt.split("DATOS_JSON\n",1)[1].split("\nFIN_DATOS",1)[0])
    hs=d["senales"]
    fuentes=sorted({h["regla"].lower() for h in hs}&set(d["recuperados"]))
    return json.dumps(dict(hallazgos=hs,fuentes=fuentes,estado="hallazgos" if hs else "sin hallazgos"),ensure_ascii=False)
