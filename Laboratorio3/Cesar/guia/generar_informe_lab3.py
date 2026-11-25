"""Construye el informe de evidencia a partir de archivos medidos, no de valores inventados."""
from pathlib import Path
import json
from html import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

RAIZ=Path(__file__).resolve().parents[1]
SALIDA=RAIZ/"entrega"
SALIDA.mkdir(exist_ok=True)
pdfmetrics.registerFont(TTFont("ArialLab",r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialLabBold",r"C:\Windows\Fonts\arialbd.ttf"))
estilos=getSampleStyleSheet()
for name in ("Normal","BodyText","Title","Heading1","Heading2"):
    estilos[name].fontName="ArialLabBold" if name in ("Title","Heading1","Heading2") else "ArialLab"
    estilos[name].textColor=colors.black
estilos["Normal"].fontSize=10.2
estilos["Normal"].leading=14
estilos["Normal"].spaceAfter=8
estilos["Title"].fontSize=23
estilos["Title"].leading=29
estilos["Title"].spaceAfter=17
estilos["Heading1"].fontSize=16
estilos["Heading1"].leading=20
estilos["Heading1"].spaceAfter=13
estilos["Heading2"].fontSize=12
estilos["Heading2"].leading=16
estilos["Heading2"].spaceBefore=10
estilos["Heading2"].spaceAfter=8
estilos.add(ParagraphStyle(name="SmallLab",fontName="ArialLab",fontSize=8.4,leading=11,spaceAfter=5))
estilos.add(ParagraphStyle(name="CodeLab",fontName="Courier",fontSize=8.2,leading=11,spaceAfter=10))
historia=[]
md=[]
def titulo(t):
    historia.append(Paragraph(escape(t),estilos["Title"]));md.append("# "+t)
def h(t):
    historia.append(Paragraph(escape(t),estilos["Heading1"]));md.append("## "+t)
def h2(t):
    historia.append(Paragraph(escape(t),estilos["Heading2"]));md.append("### "+t)
def par(t,small=False):
    historia.append(Paragraph(escape(t),estilos["SmallLab" if small else "Normal"]));md.append(t)
def tabla(headers,rows,widths):
    datos=[[Paragraph(escape(str(c)),estilos["SmallLab"]) for c in headers]]
    datos += [[Paragraph(escape(str(c)),estilos["SmallLab"]) for c in r] for r in rows]
    t=Table(datos,colWidths=widths,repeatRows=1,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e5ebf2")),
        ("GRID",(0,0),(-1,-1),.5,colors.HexColor("#d9d9d9")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f7f9fb")])]))
    historia.extend([t,Spacer(1,10)])
    md.append("| "+" | ".join(headers)+" |\n|"+"|".join("---" for _ in headers)+"|")
    md.extend("| "+" | ".join(str(c) for c in r)+" |" for r in rows)
def code(t):
    historia.append(Preformatted(t,estilos["CodeLab"]));md.append("~~~powershell\n"+t+"\n~~~")
def pagina(): historia.append(PageBreak())
def leer(p): return json.loads((RAIZ/p).read_text(encoding="utf8"))
resumen=leer("bitacora/laboratorio3/resumen_validacion.json")
guia={c:leer(f"bitacora/laboratorio3/guia_ABCD/av1_{c}.json") for c in "ABCD"}
variante={c:leer(f"bitacora/simulacion/av1_{c}.json") for c in "ABCD"}

titulo("Laboratorio 3\nMotor con recuperación y controles")
par("LSCA2318 · Tópico selecto de tecnologías de la información · Universidad Tecmilenio")
par("Variante de referencia 2 · Revisor de código con políticas internas")
par("Alumno: Cesar Eduardo Valdez Pinto")
par("Etapa A2 del equipo: parche · rev_parche. Guía común: individual.")
par("Repositorio: https://github.com/alanrivera066/Project_v2_TSTI")
par("Actualización: 24 de noviembre de 2026 · ejecuciones fechadas en UTC")
h2("Propósito y resultado")
par("Se implementó la conexión entre el buscador A1 y el flujo A2, junto con citas verificadas, abstención y saneo. La guía común se ejecutó con fake/hash y se registraron las salidas para comparar contexto y controles. Los controles oficiales dieron 3 aprobadas. La suite de esta copia dio 48 aprobadas y 6 omitidas. A1/A2/AV1 del repositorio del equipo dio 11 aprobadas.")
par("Esta evidencia comprueba el funcionamiento local del código. No demuestra la calidad de un modelo generativo real: Se ejecutó pytest 8.4.2 desde fuentes oficiales fijadas por etiqueta, ya que pip no pudo obtenerlo. Google confirmó acceso HTTP 200. La calibración real propuso 0.6386 y acertó ocho consultas de validación; la evaluación quedó en 15/192 respuestas por HTTP 429. No se declara terminada.")
h2("Qué es individual y qué corresponde al equipo")
par("La sección 1 del manual se trabaja en el repositorio individual. La sección 2 integra la variante del equipo para el Avance 1. Revisor de código identifica la variante v2-revisor; no identifica la etapa asignada a una persona.")
par("Como el equipo ya realizó su Avance 1, este paquete funciona como referencia del laboratorio y de su conexión con esa variante. Se actualiza el nombre del alumno y su asignación según avance1/equipo.md: parche, con id rev_parche. No se modificó el repositorio remoto.")
par("Fuentes de la actividad: manual paso a paso del Lab 3, guía del alumno y presentación Lab 03 suministrados; README.md y VARIANTES.md del ZIP docente.",small=True)

pagina()
h("1 Implementación de la guía común")
tabla(["Archivo","Trabajo realizado"],[
["retrieval.py","Normalización L2 sin división por cero; coseno; top-k estable con umbral."],
["pipeline.py","Dependencias explícitas, JSON Schema, validación en código y un reintento correctivo."],
["controles.py","Citas ausentes o inventadas; abstención; exclusión de documentos confidenciales y no vigentes; saneo."],
["asistente.py","Recuperar, filtrar, abstenerse, generar, verificar y cerrar con trazabilidad."],
["pii.py","Enmascaramiento por intervalos de PII y bloques confidenciales."]],[105,390])
h2("Las cinco fases del método responder")
par("Primero se buscan hasta cuatro fragmentos. Si los controles están activos, se descartan documentos no permitidos y el sistema se abstiene si el mejor puntaje no alcanza el umbral. Después se carga el prompt correspondiente y se genera texto o JSON. Las fuentes se contrastan con los documentos o fragmentos realmente recuperados. Finalmente se sanea la respuesta y se registra latencia, costo y recuperación.")
par("Las citas aceptan el ID documental o del fragmento, con prefijo doc: opcional. Una fuente ajena genera un error con las palabras no recuperada. Si hubo recuperación y no hay cita, se marca el incumplimiento.")
h2("Validación local")
par(f"Resultado de unittest: {resumen['pruebas']} pruebas, {resumen['fallos']} fallos, {resumen['errores']} errores y {resumen['omitidas']} omisiones. Se incluyen casos de norma cero, búsqueda ordenada, citas falsas, umbral inclusivo, reintento, PII, rutas fuera del directorio, código limpio y comentarios adversariales.")
par("La verificación de parches usa ast.parse. El código de entrada y los fragmentos de corrección se analizan sintácticamente; no se importan, aplican ni ejecutan.")
code(r"$env:PYTHONPATH = 'src'"+"\n"+r".\.venv\Scripts\python.exe -m unittest discover -s tests"+" `\n  -p test_revisor_unittest.py -v")
par("Evidencia: bitacora/laboratorio3/pruebas_unittest.txt y resumen_validacion.json. La ejecución oficial de pytest está en bitacora/validacion_oficial/, con JUnit XML, comando, directorio, fechas y hashes.",small=True)

pagina()
h("2 Comparación de la guía común")
par("Pregunta usada: ¿Puedo desplegar el 30? En el modo normal el sistema se abstuvo: los puntajes hash quedaron por debajo de 0.35. Sin RAG la simulación indicó ausencia de contexto. Sin controles devolvió el título de un documento obsoleto, sin elaborar una respuesta normativa. Este resultado muestra el comportamiento del andamio y sus límites, no una respuesta válida sobre despliegues.")
par("Se ejecutaron 16 casos públicos, dos repeticiones y cuatro configuraciones: 128 ejecuciones. Se usó contrato_guia.yaml, que conserva el contrato del ZIP docente.")
tabla(["Config.","Prompt","RAG","Controles","Exactitud","Citas","Abst. ok"],[
[c,"v1" if c=="A" else "v2","Sí" if c in "CD" else "No","Sí" if c=="D" else "No",
f"{guia[c]['metricas']['exactitud']:.2f}",f"{guia[c]['metricas']['citas_correctas']:.2f}",
f"{guia[c]['metricas']['abstencion_correcta']:.2f}"] for c in "ABCD"],[47,52,43,61,75,65,152])
tabla(["Config.","Alucinación","Fuga","Consistencia","p95 ms","US$/resp."],[
[c,f"{guia[c]['metricas']['alucinacion']:.2f}",f"{guia[c]['metricas']['fuga_pii']:.2f}",
f"{guia[c]['metricas']['consistencia']:.2f}",f"{guia[c]['metricas']['latencia_p95_ms']:.1f}","0.00000"]
for c in "ABCD"],[47,85,55,108,85,115])
h2("Interpretación e intervalos")
par("Ninguna configuración cumplió el contrato del caso común. La diferencia D - A fue +0.125 de exactitud; su intervalo bootstrap del 95 % fue [-0.125, 0.375]. Incluye cero, por lo que no permite afirmar una mejora. Los intervalos remuestrean casos pareados, manteniendo juntas sus repeticiones.")
par("La consistencia compara el contenido de respuesta, fuentes y abstención, sin latencia ni costo. La consistencia de un simulador determinista no prueba estabilidad de un LLM. El costo cero corresponde al proveedor fake y los tiempos son locales.")
par("Evidencia: bitacora/laboratorio3/guia_ABCD/av1_A.json a av1_D.json, guia_ABCD.txt, s3_rag_eval.txt y comparacion_guia.json.",small=True)

pagina()
h("3 Conexión con el revisor de código")
par("El equipo usa detectar, explicar, parche y dictamen. Tu etapa es parche. La siguiente tabla describe esta copia de referencia; no sustituye su Avance 1.")
tabla(["Etapa","Entrada y propósito","Validación"],[
["1 reglas","Señales AST y políticas recuperadas.","Regla existente, línea real y cobertura de señales."],
["2 explicar","Reglas y hallazgos de la etapa anterior.","Conservar evidencia y severidad; evitar hallazgos nuevos."],
["3 parche","Reglas y explicaciones.","Fragmento Python no vacío y sintácticamente válido."],
["4 verificar","Artefacto y parches propuestos.","Esquema, regla, línea, cobertura y sintaxis."]],[72,238,185])
par("El preanálisis detecta patrones conservadores de SEC-01 a SEC-10. El buscador combina similitud vectorial y coincidencia de identificador para políticas ya identificadas. Un puntaje 1.0 de ID exacto no se presenta como similitud coseno. En código limpio, el resultado es sin hallazgos. No se revela sec-11 ni se obedecen órdenes incluidas en comentarios.")
par("Se prepararon 20 casos: 12 normales, 4 fuera de dominio, 2 límite y 2 adversariales. Se conservaron aparte los diez casos públicos originales. La evaluación de referencia usó tres repeticiones por caso: 240 ejecuciones entre A y D.")
tabla(["Config.","Exactitud","Citas","Abst. ok","FP limpio","Resultado"],[
[c,f"{variante[c]['metricas']['exactitud']:.2f}",f"{variante[c]['metricas']['citas_correctas']:.2f}",
f"{variante[c]['metricas']['abstencion_correcta']:.2f}",variante[c]["metricas"]["falsos_positivos_limpio"],
"Simulación"] for c in "ABCD"],[47,85,70,85,90,118])
par("El simulador arma sus salidas a partir de las señales AST; no consulta los resultados esperados. Por eso su exactitud de 1.00 comprueba cableado y no calidad generativa. No se observó mejora de exactitud A-D: todos los intervalos fueron [0, 0]. Los validadores de A2 permanecen activos en las cuatro configuraciones.")
h2("Meta que cambiaría en el contrato")
par("Para esta variante exigiría cero falsos positivos en el código limpio y una cita por regla reportada. Una alerta falsa retrasa revisiones válidas y una regla sin fuente no puede justificarse. Se agregó falsos_positivos_limpio_max: 0 al evaluador; además se propuso citas_correctas_min: 0.95, manteniendo fuga_pii_max: 0.0.")
par("Evidencia: bitacora/simulacion/, evals/v2-revisor.jsonl, contrato_calidad.yaml y tests/test_revisor_unittest.py.",small=True)

pagina()
h("4 Reproducción y cierre")
h2("Ejecutar el laboratorio en esta carpeta")
code(r"$env:PYTHONPATH = 'src'"+"\n"+r"$env:LLM_PROVIDER = 'fake'"+"\n"+r"$env:EMB_PROVIDER = 'hash'"+"\n"+r"$env:PYTHONIOENCODING = 'utf-8'"+"\n"+r".\.venv\Scripts\python.exe guia\validar_laboratorio3.py")
par("El ZIP excluye el entorno virtual, credenciales y cachés. En otra computadora se debe crear .venv e instalar requirements.txt y el paquete editable, siguiendo LEEME_LABORATORIO3.md.")
h2("Comprobaciones oficiales ejecutadas")
code(r".\.venv\Scripts\python.exe -m pip install -r requirements.txt"+"\n"+r".\.venv\Scripts\python.exe -m pip install -e ."+"\n"+r".\.venv\Scripts\python.exe -m pytest tests/test_av1_controles.py -q"+"\n"+r".\.venv\Scripts\python.exe -m pytest -q")
par("El intento con pip no obtuvo pytest. Se recuperaron fuentes oficiales y licencias para ejecutar pytest 8.4.2. Resultado: 3/3 de controles y 48 aprobadas, 6 omitidas en la suite local. Las omisiones corresponden a cinco funciones futuras A4 y la API S4 por falta de FastAPI. A1/A2/AV1 del equipo dio 11/11 en una instantánea parcial fija.")
h2("Medición con un proveedor real")
par("La llave se configura únicamente en .env. Después se seleccionan LLM_PROVIDER=gemini y EMB_PROVIDER=gemini, se confirma el modelo del curso y se calibra el umbral con ejemplos de desarrollo separados. El 0.20 de hash es un valor de desarrollo; el 0.35 de Gemini es provisional y no está calibrado. El diagnóstico vectorial hash obtuvo acierto@1=0.70 y acierto@3=0.80 en diez consultas sobre reglas, sin demostrar comprensión semántica.")
par("Primero se recomienda una repetición para comprobar el flujo y después tres para la evidencia final. La variante puede realizar hasta cuatro llamadas por ejecución, además de reintentos. Los precios del andamio son ilustrativos; no se reportaron cargos reales.")
h2("Conclusión")
par("El motor individual quedó implementado y sus comportamientos esenciales se verificaron localmente. La simulación muestra la abstención por contexto insuficiente y permite inspeccionar el efecto de desactivar controles. El checkpoint de controles con pytest quedó aprobado. La calibración real del caso guía propuso 0.6386 con ocho validaciones correctas. La evaluación permanece parcial por cuota; ese tamaño de muestra no garantiza generalización. El analizador estático no cubre todas las vulnerabilidades y los parches propuestos requieren revisión funcional.")
par("La integración se realiza sobre el Avance 1 existente del equipo. La etapa A2 confirmada para Cesar es parche. Los commits, la etiqueta y la coevaluación deben corresponder al trabajo real de sus integrantes. Registro de asistencia: ai_log_laboratorio3.md.",small=True)

pagina()
h("5 Registro de ejecución y calibración")
h2("Dónde se ejecutaron las pruebas")
par("Windows, Python 3.14.7. Directorio de la copia del laboratorio:")
par(str(RAIZ),small=True)
par("La instantánea parcial del equipo se fijó al commit 6c1835b1a556240382c3d678ecec6bf0af6f5948. Allí se ejecutaron solo A1, A2 y controles AV1. Las 48 aprobadas corresponden a esta copia del laboratorio, no a toda la suite del repositorio ni a GitHub Actions.")
par("Cada grupo tiene comando, directorio, hora UTC de inicio y fin, código de salida y hashes en bitacora/validacion_oficial/ultima_ejecucion.json y su ejecucion.json. Los archivos .txt y JUnit .xml guardan resultados sin resumir.")
code(r"$env:PYTHONPATH = 'herramientas_pruebas;src'"+"\n"+r"$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'"+"\n"+r".\.venv\Scripts\python.exe guia\ejecutar_pruebas_oficiales.py")
par("El soporte incluye fuentes de pytest 8.4.2, pluggy 1.6.0, iniconfig 2.1.0 y módulos de Pygments 2.19.2, con licencias. No se cambió la lógica de pytest; se generó la metadata de versión a partir de las etiquetas oficiales. La copia del equipo se conserva fuera del paquete.")
h2("Acceso y continuación de Gemini")
par("Al ejecutar desde PowerShell del alumno, Google respondió HTTP 200. El modelo seleccionado fue gemini-3.1-flash-lite y los embeddings gemini-embedding-001. La calibración produjo 0.6386449460, con 4/4 positivos y 4/4 negativos correctos en validación. La evaluación se interrumpió por HTTP 429 tras guardar 15 respuestas de A; faltan 177 de 192.")
par("calibrar_umbral.py separa ocho consultas de desarrollo y ocho de validación. Selecciona el corte con mayor exactitud balanceada en desarrollo y lo contrasta con validación. La demostración hash propuso 0.2587 pero obtuvo 0.50 en validación; no se aplicó ese valor ni se presenta como válido para Gemini.")
code(r".\.venv\Scripts\python.exe guia\calibrar_umbral.py"+"\n"+r"$modelo = 'MODELO_AUTORIZADO'"+"\n"+r"$cal = 'bitacora/calibracion_gemini.json'"+"\n"+r"python guia/evaluar_guia_gemini.py --modelo $modelo --calibracion $cal --rep 1")
par("Configurar GEMINI_API_KEY solo en el entorno local o .env. La evaluación rechaza calibraciones hash. Usar primero una repetición y después tres para la evidencia final. Este proceso calibra el caso guía y no modifica el motor ni las mediciones existentes del equipo.")
par("Ejecutar guia/completar_gemini.py desde PowerShell normal realiza acceso, selección entre modelos disponibles, calibración y evaluación. Guarda cada respuesta y permite reanudar si se interrumpe, sin mezclar cambios de código o modelo. Se añadió una pausa de seis segundos y registro completo de cuotas, con reintentos acotados y parada ante cuota diaria. Se verificó que la firma y las 15 respuestas previas se conservan. Las pausas planificadas ocurren fuera de la latencia de responder; los reintentos internos permanecen dentro.",small=True)

def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont("ArialLab",8)
    canvas.drawString(50,30,"FinNorte · Laboratorio 3 · Evidencia de ejecución local")
    canvas.drawRightString(A4[0]-50,30,str(doc.page))
    canvas.restoreState()
archivo=SALIDA/"Laboratorio3_Revisor_Codigo.pdf"
doc=SimpleDocTemplate(str(archivo),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=44,bottomMargin=48,
    title="Laboratorio 3 Motor con recuperación y controles",author="")
doc.build(historia,onFirstPage=footer,onLaterPages=footer)
(SALIDA/"Laboratorio3_Revisor_Codigo.md").write_text("\n\n".join(md),encoding="utf8")
print(archivo)
