"""Informe final generado a partir de salidas reales y del recálculo docente original."""
from informe_estilo import *
import xml.etree.ElementTree as ET
BASE="bitacora/proceso_gemini/20261125T002950Z"
real=leer(BASE+"/evaluacion/resumen.json")
docente=leer(BASE+"/evaluacion/analisis_docente/resumen_docente.json")
cal=leer(BASE+"/calibracion.json")
filas={r["config"]:r for r in docente["tabla"]}
D=filas["D"]
ultimo=leer("bitacora/validacion_oficial/ultima_ejecucion.json")
pruebas={}
for grupo in ("controles_lab3","suite_local","equipo_a1_a2_av1"):
    cs=ET.parse(Path(ultimo["directorio"])/(grupo+".xml")).findall(".//testcase")
    pruebas[grupo]=dict(aprobadas=sum(not any(c.find(k) is not None for k in ("failure","error","skipped")) for c in cs),
        omitidas=sum(c.find("skipped") is not None for c in cs))
pct=lambda n:f"{100*n:.2f} %"
titulo("Laboratorio 3\nMotor con recuperación y controles")
par("LSCA2318 · Universidad Tecmilenio · Entrega individual")
par("Alumno: Cesar Eduardo Valdez Pinto")
par('Variante del equipo: v2-revisor · Mi etapa A2: parche / rev_parche')
par("Repositorio: https://github.com/alanrivera066/Project_v2_TSTI")
par('Fecha: 24 de noviembre de 2026')
h2("Resultado del laboratorio")
par('En este laboratorio evalué un motor con recuperación de información y controles de respuesta. Comparé cuatro configuraciones mediante 16 casos y tres repeticiones por caso, para un total de 192 ejecuciones. Utilicé gemini-3.1-flash-lite para generar las respuestas y gemini-embedding-001 para los embeddings. Después de reanudar comprobé las respuestas, el umbral y la firma del código.')
tabla(["Medida de D","Resultado"],[
["Exactitud",pct(D["exactitud"])+" · 45 de 48 ejecuciones correctas"],
["Citas esperadas y abstención correcta",pct(D["citas_correctas"])+" en cada medida"],
["Citas inventadas y fuga PII detectadas","0 en los casos evaluados"],
["Latencia p95",f'{D["latencia_p95_ms"]/1000:.3f} segundos'],
["Metas del contrato docente",str(sum(x["cumple"] for x in D["contrato"]))+" de 8, usando su definición original"]],[220,275])
h2("Alcance de mi trabajo")
par('La guía común corresponde a mi entrega individual. Dentro del equipo trabajamos con la variante 2, revisor de código, y mi etapa es parche. En este documento presento la implementación del laboratorio, las pruebas, la calibración del umbral y la comparación de resultados. Mantuve el código y las mediciones del Avance 1 que ya tenía el equipo.')
par('Para distinguir las mediciones, separé las pruebas de código, las simulaciones fake/hash y la evaluación real. Los resultados simulados del revisor sirven para comprobar su funcionamiento y se presentan por separado de las mediciones reales de la guía común.')
par('Fuentes de la práctica: manual paso a paso, guía del alumno, presentación Lab 03, ZIP del curso, avance1/equipo.md y registros de bitacora/.',small=True)

pagina()
h("1 Implementación y pruebas")
tabla(["Componente","Comportamiento implementado"],[
["Buscador A1","Normaliza filas, calcula coseno y devuelve top-k ordenado con umbral."],
["Flujo A2","Resuelve dependencias, valida JSON Schema y reglas en código; reintenta con el error."],
["Controles","Comprueba citas; se abstiene por contexto insuficiente; excluye documentos confidenciales y no vigentes."],
["Asistente","Recuperar, filtrar y abstener, generar con contexto, verificar y sanear; registrar costo y latencia."],
["Saneo","Enmascara PII y bloques confidenciales; elimina URLs o imágenes externas no permitidas."]],[100,395])
par('Para comprobar las fuentes utilicé verificar_citas, que acepta identificadores documentales, de fragmentos y el prefijo doc:. Esta función rechaza fuentes ajenas e identifica citas ausentes. Con debe_abstenerse comprobé que hubiera contexto y que el mejor puntaje alcanzara el umbral. Guardé la información de recuperación, respuesta y tiempo para revisar cada caso.')
h2("Pruebas ejecutadas sin red")
tabla(["Grupo","Aprobadas","Omitidas"],[
["Controles oficiales del laboratorio",pruebas["controles_lab3"]["aprobadas"],0],
["Suite completa de esta copia local",pruebas["suite_local"]["aprobadas"],pruebas["suite_local"]["omitidas"]],
["A1/A2/AV1 de la copia parcial del equipo",pruebas["equipo_a1_a2_av1"]["aprobadas"],0]],[295,100,100])
par('Utilicé pytest 8.4.2. Las seis pruebas omitidas corresponden a cinco funciones futuras de A4 y al módulo API S4, que requiere FastAPI. Las tres pruebas de controles del laboratorio aprobaron. Guardé la versión, los comandos, las rutas, la salida y los resultados en formato JUnit XML.')
par('Para revisar A1/A2/AV1 tomé una copia parcial del equipo en el commit 6c1835b1a556240382c3d678ecec6bf0af6f5948. El alcance de esas once pruebas es ese subconjunto. Para los fragmentos de parche comprobé la sintaxis con ast.parse, sin aplicar ni ejecutar el código analizado.')
par("Evidencia: bitacora/validacion_oficial/ultima_ejecucion.json y la carpeta a la que apunta. El soporte de pruebas y sus licencias están en herramientas_pruebas/.",small=True)

pagina()
h("2 Calibración del umbral")
par('Configuré la conexión con Gemini en el archivo local .env y comprobé el acceso mediante una respuesta HTTP 200. Para calibrar utilicé el corpus común, gemini-embedding-001, k=4 y el mismo filtro documental del motor. Separé ocho consultas de desarrollo y ocho de validación de los 16 casos de la evaluación final.')
tabla(["Conjunto","Positivos correctos","Negativos correctos","Exactitud balanceada"],[
["Desarrollo","4 / 4","4 / 4",pct(cal["desarrollo"]["exactitud_balanceada"])],
["Validación","4 / 4","4 / 4",pct(cal["validacion"]["exactitud_balanceada"])]],[95,130,130,140])
h2("Criterio y valor elegido")
par(f'Elegí el umbral {cal["umbral_propuesto"]:.10f}. Para obtenerlo comparé cortes entre los puntajes del conjunto de desarrollo y seleccioné el de mayor exactitud balanceada. En los empates prioricé la abstención ante consultas fuera de dominio. Después comprobé el valor con el conjunto de validación, sin utilizar los 16 casos finales para ajustarlo.')
par('El resultado de 8/8 en cada conjunto es favorable, aunque la muestra es pequeña. En la evaluación final apareció una abstención innecesaria en c10. Conservé ese error y mantuve el umbral elegido, para evaluar el sistema con casos independientes de la calibración.')
h2("Reanudación y cuota")
par('Durante la primera ejecución obtuve quince respuestas y después recibí un error HTTP 429. El mensaje guardado no permite distinguir el tipo exacto de cuota. Al reanudar mantuve el modelo, los prompts, el corpus, los datos y las respuestas anteriores. Añadí una pausa de seis segundos entre ejecuciones y un registro más completo de los errores de cuota.')
par('La pausa ocurre antes de procesar cada respuesta y queda fuera de su latencia. Los reintentos internos del proveedor sí forman parte del tiempo registrado. Guardé por separado la información de la reanudación para poder reconstruir la ejecución.')
par("Calibración: "+BASE+"/calibracion.json. Reanudación y firma: "+BASE+"/evaluacion/. Las credenciales se excluyen del informe, de los archivos públicos y del ZIP.",small=True)

pagina()
h("3 Comparación de las configuraciones")
par('En A utilicé el prompt v1 sin contexto ni controles; en B cambié al prompt v2 sin contexto; en C añadí recuperación y en D incorporé los controles. Cada configuración produjo 48 resultados. Las 192 salidas completadas no registraron errores de sistema.')
tabla(["Config.","Exactitud","Citas","Abstención","Fuga PII","Consistencia"],[
[c,pct(filas[c]["exactitud"]),pct(filas[c]["citas_correctas"]),pct(filas[c]["abstencion_correcta"]),
pct(filas[c]["fuga_pii"]),pct(filas[c]["consistencia"])] for c in "ABCD"],[48,90,85,95,82,95])
tabla(["Config.","Citas inventadas","p95 segundos","USD estimado","Metas"],[
[c,pct(filas[c]["alucinacion"]),f'{filas[c]["latencia_p95_ms"]/1000:.3f}',
f'{filas[c]["costo_promedio_usd"]:.6f}',str(sum(x["cumple"] for x in filas[c]["contrato"]))+" / 8"]
for c in "ABCD"],[48,130,110,110,97])
par('Al comparar C con D observé que la recuperación por sí sola permitió exponer contenido restringido en seis de las 48 respuestas de C. Con los controles de D no detecté esa fuga. Las métricas de fuga y citas inventadas se limitan a los patrones y casos de esta evaluación.')
par('Para estimar el costo utilicé la tarifa ilustrativa incluida en el proyecto: USD 0.30 por millón de tokens de entrada y USD 2.50 por millón de salida. El valor no corresponde a una factura y excluye embeddings y llamadas fallidas que no aparecen en las respuestas completadas.')
par('En esta tabla utilicé la definición original de consistencia del curso: mantener el mismo acierto o fallo por caso entre repeticiones. En la siguiente sección comparo ese criterio con la igualdad literal de las respuestas.')
par("Fuentes: resumen.json y guia_A.json a guia_D.json de la ejecución real; analisis_docente/resumen_docente.json para el criterio original del contrato.",small=True)

pagina()
h("4 Análisis de los resultados")
tabla(["Comparación","Cambio en exactitud","IC 95 % por caso"],[
[k,f'{100*v["diferencia"]:+.2f} puntos',f'[{100*v["ic95"][0]:+.2f}, {100*v["ic95"][1]:+.2f}]']
for k,v in real["intervalos"].items()],[105,180,210])
par('En C - B y D - A los intervalos quedan por encima de cero. En D - C el intervalo incluye cero, por lo que no puedo concluir una mejora de exactitud al añadir controles con esta muestra. Sí observé una reducción de la fuga detectada, de 6/48 en C a 0/48 en D.')
h2("Diferencia entre criterios de consistencia")
par('El cálculo inicial comprobaba que coincidieran exactamente el texto, las fuentes y la abstención. Al contrastarlo con el evaluador original del curso identifiqué una diferencia: ese evaluador mide si el acierto booleano se mantiene entre repeticiones. Para aplicar el mismo criterio del contrato recalculé las 192 salidas guardadas con el archivo original. No generé respuestas nuevas ni modifiqué las existentes.')
tabla(["Config.","Criterio docente","Igualdad literal previa"],[
[c,pct(filas[c]["consistencia"]),pct(filas[c]["consistencia_literal_previa"])] for c in "ABCD"],[95,200,200])
par('En c01 y c06 las respuestas fueron correctas en las tres repeticiones, aunque cambió su redacción. En c10 ocurrió lo contrario: D se abstuvo en las tres ocasiones, no respondió Idempotency-Key y no citó ing-07. Por eso interpreto la consistencia como estabilidad del resultado, que también puede incluir un error repetido.')
par('D cumple las ocho metas con el criterio original del contrato, pero conserva el fallo de c10. Como mejora posterior considero ampliar los casos de calibración y reforzar la recuperación de preguntas técnicas, manteniendo una evaluación final independiente.')
par('Conservé ambos cálculos: resumen.json contiene la comparación literal; analisis_docente/resumen_docente.json, el criterio original. El archivo del evaluador en referencias/ y su SHA-256 permiten comprobar el recálculo.',small=True)

pagina()
h("5 Evidencia y reproducción")
h2("Entorno de ejecución")
par('Ejecuté la evaluación Gemini desde PowerShell en Windows, con Python 3.14.7, en el siguiente directorio:',small=True)
par(RAIZ.as_posix(),small=True)
par('El registro de acceso comenzó el 25 de noviembre de 2026 a las 00:29:50 UTC y el proceso terminó a las 00:56:47 UTC. Ambos horarios corresponden al 24 de noviembre en Ciudad de México. El análisis posterior utilizó los archivos guardados, sin llamadas nuevas a Gemini.')
h2("Archivos que respaldan la entrega")
tabla(["Archivo o carpeta","Qué comprueba"],[
["estado.json","El proceso terminó y señala las rutas de salida."],
["calibracion.json","Consultas de desarrollo/validación y umbral elegido."],
["evaluacion/A a D","Las 192 salidas por caso y repetición."],
["firma.json y reanudacion_*.json","Mismos insumos; conservación de las quince respuestas anteriores."],
["evaluacion/analisis_docente/","Recálculo original docente y comparación de consistencia."],
["bitacora/validacion_oficial/","Comandos, directorios, versiones, hashes, texto y JUnit de pytest."]],[190,305])
code(r"$env:PYTHONPATH = 'herramientas_pruebas;src'"+"\n"+r"$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'"+"\n"+r".\.venv\Scripts\python.exe guia\ejecutar_pruebas_oficiales.py"+"\n"+r".\.venv\Scripts\python.exe guia\analizar_con_criterio_docente.py")
par('El segundo comando procesa las respuestas existentes. Para consultar los resultados no hace falta repetir Gemini. Incluí en el ZIP el código, las pruebas, los registros y las licencias. En otro equipo es necesario crear el entorno virtual e instalar las dependencias de requirements.txt.')
h2("Conclusión")
par('Con esta práctica comprobé cómo cambian las respuestas al añadir recuperación y controles. La configuración D alcanzó 93.75 % de exactitud y cumplió las ocho metas del contrato con su criterio original. El caso c10 y el tamaño de la muestra muestran que todavía hay margen de mejora. Dejé los resultados y los comandos documentados para poder revisar y repetir la evaluación.')


def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont("ArialLab",8)
    canvas.drawString(50,30,"FinNorte · Laboratorio 3 · Cesar Eduardo Valdez Pinto")
    canvas.drawRightString(A4[0]-50,30,str(doc.page))
    canvas.restoreState()
archivo=SALIDA/"Laboratorio3_Revisor_Codigo.pdf"
SimpleDocTemplate(str(archivo),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=44,bottomMargin=48,
    title="Laboratorio 3 Motor con recuperación y controles",author="Cesar Eduardo Valdez Pinto").build(
        historia,onFirstPage=footer,onLaterPages=footer)
(SALIDA/"Laboratorio3_Revisor_Codigo.md").write_text("\n\n".join(md),encoding="utf8")
print(archivo)
