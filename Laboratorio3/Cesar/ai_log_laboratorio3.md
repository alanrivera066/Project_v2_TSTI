# Registro de uso de IA
| Fecha | Uso | Aceptado | Modificado o revisado | Validación |
|---|---|---|---|---|
| 2026-11-22 | Asistencia de ChatGPT para implementar A1, A2 y guía del Lab 3 desde el ZIP docente | Código base de normalización, coseno, flujo, citas y abstención | Comparación con docstrings, casos del curso y límites de entrada | bitacora/laboratorio3/pruebas_unittest.txt |
| 2026-11-22 | Integración de referencia de la variante v2-revisor | Preanálisis AST, prompts y JSON Schema | Filtro confidencial, líneas válidas, recuperación por ID y control de parches | tests/test_revisor_unittest.py y ejemplo_revisor.json |
| 2026-11-22 | Diseño de 20 casos y contrato propuesto | Mezcla 12 normales, 4 fuera, 2 límite y 2 adversariales | Conservación de los casos públicos originales y separación de fake frente a medición real | evals/v2-revisor.jsonl y bitacora/simulacion/ |
| 2026-11-22 | Redacción de informe de evidencia | Explicación de fases, tabla y límites de medición | Nombres y etapa en blanco por instrucción; no atribuir resultados a Gemini ni afirmar pytest aprobado | entrega/Laboratorio3_Revisor_Codigo.pdf |

El código fue producido con asistencia de IA y requiere revisión por los integrantes antes de integrarlo a su Avance 1 ya existente. No se inventaron autores de commits, roles individuales, corridas reales ni una decisión de fusión entre buscadores de compañeros.

## Actualización de pruebas y datos
Se confirmó Cesar Eduardo Valdez Pinto y parche/rev_parche según el repositorio aportado. Se ejecutó pytest real: 3 controles; suite local 47 aprobadas y 6 omitidas; 11 tests A1/A2/AV1 de una instantánea parcial fija del equipo. Registro: bitacora/validacion_oficial/. Se preparó calibración desarrollo/validación y evaluación Gemini, pendiente de llave y sin llamadas. La demostración hash falló en validación y no se aplicó su corte.

## Configuración autorizada y bloqueo de red
Se cargó la llave desde el archivo local indicado por el usuario, sin mostrarla. El acceso al listado de modelos falló por DNS antes de validar la llave. Se preparó completar_gemini.py con registros y reanudación, y se añadió una prueba de privacidad de errores del proveedor. La suite actual dio 48 aprobadas y 6 omitidas; controles 3/3 y copia parcial del equipo 11/11. No se declararon resultados reales de Gemini.

## Cuota y conservación de evidencias
El usuario ejecutó el proceso real fuera del entorno restringido: Google 200, calibración 0.6386449460, desarrollo 8/8 y validación 8/8. La evaluación se detuvo por 429 después de 15 respuestas. Se comprobó la firma, se mantuvieron los 15 archivos y se añadió control de ritmo/registro de cuota fuera del código medido. Tres pruebas de la nueva política pasaron. La evaluación sigue parcial, sin afirmar si el límite era por minuto o diario porque el error original estaba truncado.

## Cierre real: 24 de noviembre de 2026 (registros UTC del 25)
El usuario completó las 192 ejecuciones reales de la guía común desde PowerShell normal. Se verificaron modelo, umbral, firma y preservación de las 15 respuestas anteriores. Se repitieron pruebas oficiales: 3 controles; suite local 51 aprobadas y 6 omitidas; copia parcial del equipo 11 aprobadas.

En la revisión se detectó que la consistencia del evaluador preparado inicialmente exigía igualdad literal, diferente de la estabilidad del acierto booleano del andamio docente. Se cargó el archivo docente original del ZIP, conservado con SHA-256, y se recalcularon offline las mismas respuestas; cero nuevas llamadas y cero respuestas modificadas. Los dos criterios se publican y se preserva resumen.json. D alcanza 93.75 % de exactitud y cumple las ocho metas con el criterio docente; la consistencia literal es 31.25 % y c10 falla en las tres repeticiones. No se cambió el umbral con datos finales.

Se actualizó el informe a seis páginas y se revisaron sus seis páginas renderizadas. El paquete documenta límites, fallos y reproducción; las simulaciones siguen separadas. La integración se prepara como propuesta aislada en el repositorio existente, sin atribuir commits históricos al alumno ni afirmar entrega a Canvas.

La propuesta de integración no llegó a publicarse: GitHub rechazó la creación del primer blob con HTTP 403, Resource not accessible by integration. Se registró el bloqueo y no se creó rama, commit ni PR. El paquete final y sus evidencias quedan completos de forma local.

## Revisión editorial del informe — 24 de noviembre de 2026
A petición del alumno, se revisaron 26 párrafos para usar primera persona y una redacción académica natural. Se quitaron del PDF las notas sobre el entorno del asistente, el bloqueo de publicación y las aclaraciones administrativas de autoría, coevaluación o Canvas. Se conservaron los resultados, los alcances de las pruebas, el error c10, los dos criterios de consistencia y las limitaciones estadísticas. Se revisaron las seis páginas renderizadas; no se generaron nuevas respuestas Gemini ni se modificaron los insumos medidos. El registro de asistencia y las evidencias permanecen en sus archivos correspondientes.
