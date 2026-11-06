# Actividad 2 Mi etapa

Luis Alfonso Juárez Amaro | Equipo 2 | v2-revisor

Comenzamos a trabajar en el proyecto el 29 de octubre de 2026.

## 1. Mi etapa y cómo ayuda al proyecto

Mi etapa es detectar problemas de seguridad y su identificador es rev_detectar. Básicamente, recibe un archivo de Python con sus líneas numeradas y entrega una lista de hallazgos. Cada hallazgo incluye un identificador, una regla SEC, la línea donde aparece y una descripción.

Esta parte ayuda a que las siguientes etapas tengan un punto de partida. Por ejemplo, si aparece una credencial escrita directamente en el código, detectar debe señalarla para que después Alan explique el problema y César proponga una corrección. Si el archivo está limpio, debe entregar la lista vacía.

En el Avance 1, mi parte también comprende el buscador de reglas y los controles de citas y abstención. El buscador permite proporcionar contexto a las etapas, evitando incluir el documento confidencial sec-11.

## 2. Mi prompt inicial

Mi primera versión está en prompts/rev_detectar.v1.md. El prompt establece el rol de revisor de seguridad, las reglas permitidas y el formato JSON que debe devolver.

Una instrucción de mi archivo es: “No inventes vulnerabilidades ni números de línea”. También indica que los comentarios del código se deben tratar como datos, porque podrían contener instrucciones que intenten cambiar la revisión.

Las técnicas que identifico son la asignación de un rol, las restricciones explícitas y la salida estructurada. Por ejemplo, un hallazgo puede indicar SEC-01, línea 3, por una credencial escrita en el código. Lo importante es que el resultado se pueda comprobar antes de pasar a la siguiente etapa.

## 3. Mi validación en código

Para esta etapa se utiliza validar_detectar, en src/finnorte/reglas.py, además de la validación del esquema en pipeline.py. Se comprueba que la línea exista, que la regla esté permitida, que no se repita una misma regla y línea y que no se omitan ciertos registros sensibles que el programa puede reconocer.

Esto se revisa mediante código porque una instrucción en el prompt no garantiza que el modelo la cumpla. Si devuelve una línea que no existe, el programa debe rechazarla.

## 4. Evidencia de mi etapa

La trazabilidad nueva del Laboratorio 2 está en bitacora/lab2_cuatro_etapas_20261105/a2_trazabilidad.json. Un resumen del registro es:

| Campo | Dato |
| --- | --- |
| Proveedor y modelo | gemini / gemini-3.1-flash-lite |
| Fecha UTC del archivo | 2026-11-06T04:28:11.412938+00:00 |
| Prompt y entrada | rev_detectar.v3 / transferencias.py |
| Resultado | 5 hallazgos / Salida válida: true / Intentos: 1 |

Mi fila en a2_matriz.md, dentro de esa misma carpeta, corresponde a:

| Entrada | Etapa | Prompt | Resultado | Válida | Intentos |
| --- | --- | --- | --- | --- | --- |
| transferencias.py | detectar | rev_detectar.v3 | 5 hallazgos | Sí | 1 |

Estas evidencias permiten comprobar qué versión se utilizó y qué resultado entregó.

## 5. Consistencia en las tres repeticiones

En las tres repeticiones de transferencias.py, la versión mejorada mantuvo los mismos cinco pares de regla y línea: SEC-01 en la línea 3, SEC-02 en las líneas 8 y 11, SEC-03 en la línea 12 y SEC-07 en la línea 10.

Para mí, esto es importante porque una revisión no debería cambiar sus hallazgos sin motivo cuando recibe el mismo archivo. La coincidencia fue de reglas y líneas; eso no significa que toda la redacción fuera idéntica ni que se hayan encontrado todos los problemas posibles.

## 6. Mi mejora y el antes y después

La mejora histórica pasó de cuatro a cinco hallazgos en transferencias.py, al cubrir el registro sensible de la línea 12. La versión mejorada del Laboratorio 2 quedó como rev_detectar.v3. Se añadieron instrucciones sobre SEC-03 y señales calculadas por el programa para ayudar a localizar registros sensibles.

Ese cambio histórico incluye modificaciones de prompt, preprocesamiento y modelo, por lo que no puedo atribuir toda la diferencia únicamente al prompt.

En las pruebas nuevas con Gemini 3.1 Flash-Lite, ambas versiones terminaron detectando cinco hallazgos. La diferencia observada fue que v1 necesitó dos intentos y v3 necesitó uno en la ejecución inicial y las tres repeticiones de transferencias.py.

Para el Avance 1 se conserva otra versión, rev_detectar.v4, que incorpora el contexto recuperado por el buscador.

## 7. Referencias de mi parte en GitHub

Las contribuciones publicadas correspondientes a mi parte pueden consultarse en estos enlaces:

- [Detección de problemas de seguridad](https://github.com/alanrivera066/Project_v2_TSTI/commit/3f6a97aa0a5f439f1840ca456d2e1fd83fe0b5f2)

- [Búsqueda de reglas y controles de recuperación](https://github.com/alanrivera066/Project_v2_TSTI/commit/b0cd7757884f2f648c1f689cf2e28fc74e10466d)

- [PR #1 publicado con mi cuenta Lolmastercraft](https://github.com/alanrivera066/Project_v2_TSTI/pull/1)

Los enlaces permiten ubicar los cambios y sus evidencias. El apoyo de IA utilizado para preparar e integrar el trabajo se describe en mi registro.

# Mi registro personal de uso de IA

Luis Alfonso Juárez Amaro | Registro para ai_log.md y el anexo

## Herramienta utilizada

ChatGPT mediante Codex.

## ¿Para qué la utilicé?

Utilicé esta herramienta como apoyo para preparar la parte que me corresponde: la detección de problemas, la conexión del buscador de reglas y los controles de citas y abstención.

## ¿Qué acepté del apoyo recibido?

Acepté propuestas de código y ajustes de prompts que se incorporaron al proyecto con sus evidencias. También acepté utilizar las bitácoras para respaldar las cifras, en lugar de presentar resultados que no estuvieran medidos.

## ¿Qué cambié o pedí ajustar?

Fui precisando el alcance del trabajo y la distribución de las etapas. Pedí conservar los prompts anteriores, trabajar con versiones nuevas y mantener los registros personales pendientes hasta preparar su contenido.

## ¿Cómo se validó?

La validación se hizo mediante pruebas de código, ejecuciones reales con Gemini y revisión de las bitácoras, realizadas con asistencia de la herramienta. En la evidencia de mi etapa, detectar mantuvo los mismos cinco hallazgos en las tres repeticiones de transferencias.py.
