# Laboratorio 3 de FinNorte

Alumno: **Cesar Eduardo Valdez Pinto**. Guía común individual. Variante del equipo: **v2-revisor**. Etapa A2 que figura en el repositorio: **parche / rev_parche**. La variante 2 es revisión de código; no significa que cada integrante tenga la segunda etapa.

Repositorio del equipo: https://github.com/alanrivera066/Project_v2_TSTI

## Resultado final comprobado

La evaluación Gemini terminó. Se verificaron **192 salidas**: 16 casos, 3 repeticiones y 4 configuraciones. Modelo: gemini-3.1-flash-lite. Embeddings: gemini-embedding-001. Umbral: **0.6386449460169339**. Desarrollo y validación separados, 8 consultas en cada uno, con 8/8 correctas; la muestra es pequeña.

La configuración D obtuvo **93.75 % de exactitud (45/48)**, 93.75 % en citas esperadas, 93.75 % en abstención correcta, ninguna fuga detectada en esos casos y latencia p95 de 3.720 segundos. El caso c10 falló en sus tres repeticiones: abstención innecesaria. El umbral no se reajustó con los casos finales.

Con la definición original del evaluador docente, D cumple 8/8 metas. Ese criterio mide estabilidad del acierto booleano por caso; no exige textos idénticos. La implementación preparada inicialmente usó igualdad literal y su resultado original permanece en evaluacion/resumen.json. Se recalcularon las mismas 192 salidas, sin llamadas ni cambios de respuestas, con el evaluador original conservado en referencias/. La comparación literal de D es 31.25 %, frente a 100 % con el criterio docente. El informe explica ambas medidas y el fallo estable c10.

## Abrir la entrega y sus evidencias

- entrega/Laboratorio3_Revisor_Codigo.pdf: informe final de seis páginas.
- entrega/Laboratorio3_Revisor_Codigo.md: versión de texto del informe.
- bitacora/proceso_gemini/20261125T002950Z/: acceso, calibración, estado completo e integridad.
- En esa carpeta, evaluacion/A/ a D/: 192 respuestas originales.
- evaluacion/resumen.json y guia_A.json a guia_D.json: medición original, incluida consistencia literal.
- evaluacion/analisis_docente/: recálculo con criterio original docente y su procedencia.
- bitacora/validacion_oficial/: comandos, directorios, versiones, hashes, resultados y XML JUnit.
- bitacora/gemini_estado_actual.json: estado completo; gemini_estado_antes_cierre.json conserva el registro parcial anterior.
- ai_log_laboratorio3.md: asistencia, decisiones y antecedentes fechados. Las notas antiguas de ejecución parcial son históricas.

El usuario ejecutó Gemini desde PowerShell normal en Windows. Los registros conservan UTC: acceso 2026-11-25 00:29:50; cierre 00:56:47. La revisión posterior no hizo llamadas nuevas. Se conservaron por SHA-256 los insumos firmados y las quince respuestas previas a la interrupción 429. Se registra la pausa de seis segundos de la reanudación fuera de la latencia de respuesta.

## Código y alcance

- src/finnorte/retrieval.py: normalización, coseno y top-k con umbral.
- src/finnorte/pipeline.py: dependencias, JSON Schema, reglas y reintentos.
- src/finnorte/controles.py, asistente.py y pii.py: citas, abstención, filtros, saneo y enmascarado.
- src/finnorte/revisor.py, variante.py, prompts/revisor_* y evals/v2-revisor.jsonl: implementación de referencia del revisor.
- contrato_guia.yaml: contrato original de la guía común; contrato_calidad.yaml: propuesta para el revisor de referencia.

Esta carpeta documenta la guía común y una referencia de integración; conserva el Avance 1 que ya realizó el equipo. Las cuatro etapas de la referencia son reglas, explicar, parche y verificar. Los resultados fake/hash del revisor están separados y no se presentan como calidad generativa real. Los parches son sugerencias de fragmentos con sintaxis comprobada, sin aplicación automática ni prueba de equivalencia funcional.

## Pruebas y reproducción

Última ejecución: bitacora/validacion_oficial/20261125T010049Z. Controles oficiales: **3 aprobadas**. Suite local: **51 aprobadas y 6 omitidas**. Subconjunto A1/A2/AV1 de una instantánea parcial del equipo: **11 aprobadas**, commit 6c1835b1a556240382c3d678ecec6bf0af6f5948. Esas once pruebas no representan toda la suite del repositorio ni GitHub Actions.

Las seis omisiones corresponden a cinco funciones futuras de A4 y la API S4 por falta de FastAPI. Pytest 8.4.2 y su soporte proceden de fuentes oficiales, con licencias en herramientas_pruebas/.

Desde esta carpeta en PowerShell, con el entorno ya instalado:

```powershell
$env:PYTHONPATH = 'herramientas_pruebas;src'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe guia\ejecutar_pruebas_oficiales.py
.\.venv\Scripts\python.exe guia\analizar_con_criterio_docente.py
.\.venv\Scripts\python.exe guia\verificar_entrega_final.py
```

Para repetir también las once pruebas del equipo, agregar al primer comando --equipo-root RUTA_DE_LA_COPIA_LOCAL_DEL_REPOSITORIO. El ZIP no incluye esa instantánea parcial del equipo ni .venv. En una computadora nueva, crear el entorno e instalar requirements.txt y el proyecto con pip install -e .; las pruebas de código y el recálculo no requieren la llave de Gemini.

No es necesario volver a ejecutar Gemini para consultar la entrega. Para una nueva medición autorizada se requiere configurar GEMINI_API_KEY solo en .env y usar guia/completar_gemini.py; no mezclar ejecuciones con insumos distintos. El costo de los reportes usa la tarifa ilustrativa del andamio, no demuestra facturación y excluye embeddings y llamadas fallidas no reflejadas en las respuestas.

## Integración y entrega académica

Usar el repositorio existente del equipo. La propuesta se prepara en una rama con la carpeta Laboratorio3/Cesar/, el PDF, el ZIP y resúmenes de evidencia. El Avance 1 mantiene sus archivos. La contribución asistida debe revisarse por el alumno y el equipo; no se inventan commits, coevaluaciones ni una entrega a Canvas. La publicación académica y cualquier integración en main se revisan por separado.

Las credenciales y .env se excluyen del paquete y de los archivos públicos. El ZIP conserva código, prompts, casos, pruebas, licencias, informes y resultados originales. El informe final se genera con guia/generar_informe_final.py (requiere ReportLab y Arial de Windows).

Estado de GitHub al cierre: la creación del primer archivo fue rechazada con HTTP 403, Resource not accessible by integration. No se creó rama, commit ni PR. La entrega queda preparada localmente; falta habilitar el permiso de escritura o subirla desde una cuenta autorizada. Registro: bitacora/github_integracion.json.

El PDF y su versión Markdown se actualizaron con redacción en primera persona. Las métricas y los registros de ejecución se conservan. La información administrativa sobre GitHub permanece en bitacora/github_integracion.json.
