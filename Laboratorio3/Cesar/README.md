# Laboratorio 3 — Cesar Eduardo Valdez Pinto

En este laboratorio conecté el buscador con el flujo, añadí controles y comparé cuatro configuraciones del motor. Este directorio contiene el código, las pruebas, el informe y los registros de la guía común.

Repositorio del equipo: https://github.com/alanrivera066/Project_v2_TSTI

Variante del equipo: v2-revisor. Mi etapa A2: parche / rev_parche.

## Informe y resultados

- [Informe del laboratorio en PDF](entrega/Laboratorio3_Revisor_Codigo.pdf).
- [Informe en Markdown](entrega/Laboratorio3_Revisor_Codigo.md).
- [Resumen original de la evaluación](bitacora/proceso_gemini/20261125T002950Z/evaluacion/resumen.json).
- [Resumen con el criterio de consistencia original del curso](bitacora/proceso_gemini/20261125T002950Z/evaluacion/analisis_docente/resumen_docente.json).
- [Calibración del umbral](bitacora/proceso_gemini/20261125T002950Z/calibracion.json).
- [Resultados de las pruebas de código](bitacora/validacion_oficial/resumen_resultados.json).

Completé 192 ejecuciones de la guía común: 16 casos, tres repeticiones y cuatro configuraciones. Utilicé gemini-3.1-flash-lite y gemini-embedding-001. El umbral elegido fue 0.6386449460169339, a partir de ocho consultas de desarrollo y otras ocho de validación, separadas de los casos finales.

La configuración D obtuvo 45/48 respuestas correctas (93.75 %), 93.75 % en citas y abstención correcta, cero fuga detectada en estos casos y una latencia p95 de 3.720 segundos. El caso c10 falló por abstención innecesaria en sus tres repeticiones; mantuve ese error y el umbral elegido.

Con el criterio original del curso, D cumple 8/8 metas. Ese criterio mide la estabilidad del acierto booleano: D tiene 100 %. El cálculo literal inicial, que compara texto, fuentes y abstención, da 31.25 %. Conservé ambos resultados y recalculé las mismas respuestas con el evaluador original, sin llamadas nuevas ni cambios en las salidas. El informe explica la diferencia y el fallo estable de c10. Los costos corresponden a la tarifa ilustrativa del proyecto, no a una factura.

## Qué contiene esta carpeta

| Carpeta o archivo | Contenido |
| --- | --- |
| src/finnorte/ | Buscador, flujo, asistente, controles e implementación de referencia del revisor. |
| prompts/ | Prompts versionados y esquemas. |
| corpus/ y evals/ | Corpus y casos de evaluación. |
| contrato_guia.yaml | Metas de la guía común. |
| contrato_calidad.yaml | Contrato propuesto para el revisor de referencia. |
| tests/ y herramientas_pruebas/ | Pruebas y soporte de pytest, con sus licencias. |
| guia/ | Scripts de ejecución, calibración, evaluación y recálculo. |
| bitacora/ | Respuestas originales, métricas, registros, firmas y resultados JUnit. |
| referencias/ | Evaluador original del curso y su procedencia. |
| entrega/ | Informe final en PDF y Markdown. |
| ai_log_laboratorio3.md | Registro de asistencia y cambios. |
| LEEME_LABORATORIO3.md | Explicación ampliada y antecedentes del trabajo. |

Las 192 mediciones reales corresponden a la guía común. Los 20 casos del revisor y sus simulaciones fake/hash se identifican por separado; no representan una nueva medición real de la variante del equipo.

## Pruebas

Controles oficiales: 3 aprobadas. Suite local: 51 aprobadas y 6 omitidas. Las omisiones corresponden a cinco funciones futuras de A4 y al módulo API S4 sin FastAPI. Un subconjunto A1/A2/AV1 de la copia parcial del equipo obtuvo 11 aprobadas, sobre el commit 6c1835b1a556240382c3d678ecec6bf0af6f5948. El paquete incluye su registro; no incluye esa copia parcial del equipo.

En PowerShell, primero ubicar la terminal dentro de Laboratorio3/Cesar/. En un equipo nuevo:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
$env:PYTHONPATH = 'herramientas_pruebas;src'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe guia\ejecutar_pruebas_oficiales.py
.\.venv\Scripts\python.exe guia\analizar_con_criterio_docente.py
```

Las pruebas de código y el recálculo usan los archivos existentes. No hace falta ejecutar Gemini de nuevo para consultar esta entrega.

## Ubicación en GitHub

Copiar la carpeta Laboratorio3 completa a la raíz de la copia local del repositorio. La ruta final es Laboratorio3/Cesar/README.md. Esta carpeta mantiene el laboratorio separado de los archivos del Avance 1. El informe de seis páginas documenta esta práctica; no sustituye el documento técnico completo del equipo.

Para subir todos los archivos en una sola operación, se puede utilizar GitHub Desktop: clonar o abrir el repositorio, copiar Laboratorio3, revisar los cambios, crear un commit y pulsar Push origin o Publish branch según la rama utilizada. La publicación requiere permiso de escritura en el repositorio.

El paquete excluye .env, la llave de API, el entorno virtual y los cachés. El código del Avance 1 existente mantiene su ubicación. En un repositorio nuevo, conservar esta misma estructura y añadir el enlace al proyecto del equipo.
