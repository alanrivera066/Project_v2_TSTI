# Laboratorio 3
Motor con recuperación y controles

LSCA2318 · Universidad Tecmilenio · Entrega individual

Alumno: Cesar Eduardo Valdez Pinto

Variante del equipo: v2-revisor · Mi etapa A2: parche / rev_parche

Repositorio: https://github.com/alanrivera066/Project_v2_TSTI

Fecha: 24 de noviembre de 2026

### Resultado del laboratorio

En este laboratorio evalué un motor con recuperación de información y controles de respuesta. Comparé cuatro configuraciones mediante 16 casos y tres repeticiones por caso, para un total de 192 ejecuciones. Utilicé gemini-3.1-flash-lite para generar las respuestas y gemini-embedding-001 para los embeddings. Después de reanudar comprobé las respuestas, el umbral y la firma del código.

| Medida de D | Resultado |
|---|---|

| Exactitud | 93.75 % · 45 de 48 ejecuciones correctas |

| Citas esperadas y abstención correcta | 93.75 % en cada medida |

| Citas inventadas y fuga PII detectadas | 0 en los casos evaluados |

| Latencia p95 | 3.720 segundos |

| Metas del contrato docente | 8 de 8, usando su definición original |

### Alcance de mi trabajo

La guía común corresponde a mi entrega individual. Dentro del equipo trabajamos con la variante 2, revisor de código, y mi etapa es parche. En este documento presento la implementación del laboratorio, las pruebas, la calibración del umbral y la comparación de resultados. Mantuve el código y las mediciones del Avance 1 que ya tenía el equipo.

Para distinguir las mediciones, separé las pruebas de código, las simulaciones fake/hash y la evaluación real. Los resultados simulados del revisor sirven para comprobar su funcionamiento y se presentan por separado de las mediciones reales de la guía común.

Fuentes de la práctica: manual paso a paso, guía del alumno, presentación Lab 03, ZIP del curso, avance1/equipo.md y registros de bitacora/.

## 1 Implementación y pruebas

| Componente | Comportamiento implementado |
|---|---|

| Buscador A1 | Normaliza filas, calcula coseno y devuelve top-k ordenado con umbral. |

| Flujo A2 | Resuelve dependencias, valida JSON Schema y reglas en código; reintenta con el error. |

| Controles | Comprueba citas; se abstiene por contexto insuficiente; excluye documentos confidenciales y no vigentes. |

| Asistente | Recuperar, filtrar y abstener, generar con contexto, verificar y sanear; registrar costo y latencia. |

| Saneo | Enmascara PII y bloques confidenciales; elimina URLs o imágenes externas no permitidas. |

Para comprobar las fuentes utilicé verificar_citas, que acepta identificadores documentales, de fragmentos y el prefijo doc:. Esta función rechaza fuentes ajenas e identifica citas ausentes. Con debe_abstenerse comprobé que hubiera contexto y que el mejor puntaje alcanzara el umbral. Guardé la información de recuperación, respuesta y tiempo para revisar cada caso.

### Pruebas ejecutadas sin red

| Grupo | Aprobadas | Omitidas |
|---|---|---|

| Controles oficiales del laboratorio | 3 | 0 |

| Suite completa de esta copia local | 51 | 6 |

| A1/A2/AV1 de la copia parcial del equipo | 11 | 0 |

Utilicé pytest 8.4.2. Las seis pruebas omitidas corresponden a cinco funciones futuras de A4 y al módulo API S4, que requiere FastAPI. Las tres pruebas de controles del laboratorio aprobaron. Guardé la versión, los comandos, las rutas, la salida y los resultados en formato JUnit XML.

Para revisar A1/A2/AV1 tomé una copia parcial del equipo en el commit 6c1835b1a556240382c3d678ecec6bf0af6f5948. El alcance de esas once pruebas es ese subconjunto. Para los fragmentos de parche comprobé la sintaxis con ast.parse, sin aplicar ni ejecutar el código analizado.

Evidencia: bitacora/validacion_oficial/ultima_ejecucion.json y la carpeta a la que apunta. El soporte de pruebas y sus licencias están en herramientas_pruebas/.

## 2 Calibración del umbral

Configuré la conexión con Gemini en el archivo local .env y comprobé el acceso mediante una respuesta HTTP 200. Para calibrar utilicé el corpus común, gemini-embedding-001, k=4 y el mismo filtro documental del motor. Separé ocho consultas de desarrollo y ocho de validación de los 16 casos de la evaluación final.

| Conjunto | Positivos correctos | Negativos correctos | Exactitud balanceada |
|---|---|---|---|

| Desarrollo | 4 / 4 | 4 / 4 | 100.00 % |

| Validación | 4 / 4 | 4 / 4 | 100.00 % |

### Criterio y valor elegido

Elegí el umbral 0.6386449460. Para obtenerlo comparé cortes entre los puntajes del conjunto de desarrollo y seleccioné el de mayor exactitud balanceada. En los empates prioricé la abstención ante consultas fuera de dominio. Después comprobé el valor con el conjunto de validación, sin utilizar los 16 casos finales para ajustarlo.

El resultado de 8/8 en cada conjunto es favorable, aunque la muestra es pequeña. En la evaluación final apareció una abstención innecesaria en c10. Conservé ese error y mantuve el umbral elegido, para evaluar el sistema con casos independientes de la calibración.

### Reanudación y cuota

Durante la primera ejecución obtuve quince respuestas y después recibí un error HTTP 429. El mensaje guardado no permite distinguir el tipo exacto de cuota. Al reanudar mantuve el modelo, los prompts, el corpus, los datos y las respuestas anteriores. Añadí una pausa de seis segundos entre ejecuciones y un registro más completo de los errores de cuota.

La pausa ocurre antes de procesar cada respuesta y queda fuera de su latencia. Los reintentos internos del proveedor sí forman parte del tiempo registrado. Guardé por separado la información de la reanudación para poder reconstruir la ejecución.

Calibración: bitacora/proceso_gemini/20261125T002950Z/calibracion.json. Reanudación y firma: bitacora/proceso_gemini/20261125T002950Z/evaluacion/. Las credenciales se excluyen del informe, de los archivos públicos y del ZIP.

## 3 Comparación de las configuraciones

En A utilicé el prompt v1 sin contexto ni controles; en B cambié al prompt v2 sin contexto; en C añadí recuperación y en D incorporé los controles. Cada configuración produjo 48 resultados. Las 192 salidas completadas no registraron errores de sistema.

| Config. | Exactitud | Citas | Abstención | Fuga PII | Consistencia |
|---|---|---|---|---|---|

| A | 52.08 % | 25.00 % | 81.25 % | 6.25 % | 75.00 % |

| B | 18.75 % | 25.00 % | 18.75 % | 0.00 % | 100.00 % |

| C | 87.50 % | 100.00 % | 93.75 % | 12.50 % | 100.00 % |

| D | 93.75 % | 93.75 % | 93.75 % | 0.00 % | 100.00 % |

| Config. | Citas inventadas | p95 segundos | USD estimado | Metas |
|---|---|---|---|---|

| A | 0.00 % | 12.699 | 0.001586 | 2 / 8 |

| B | 0.00 % | 3.586 | 0.000222 | 5 / 8 |

| C | 0.00 % | 4.702 | 0.000473 | 7 / 8 |

| D | 0.00 % | 3.720 | 0.000400 | 8 / 8 |

Al comparar C con D observé que la recuperación por sí sola permitió exponer contenido restringido en seis de las 48 respuestas de C. Con los controles de D no detecté esa fuga. Las métricas de fuga y citas inventadas se limitan a los patrones y casos de esta evaluación.

Para estimar el costo utilicé la tarifa ilustrativa incluida en el proyecto: USD 0.30 por millón de tokens de entrada y USD 2.50 por millón de salida. El valor no corresponde a una factura y excluye embeddings y llamadas fallidas que no aparecen en las respuestas completadas.

En esta tabla utilicé la definición original de consistencia del curso: mantener el mismo acierto o fallo por caso entre repeticiones. En la siguiente sección comparo ese criterio con la igualdad literal de las respuestas.

Fuentes: resumen.json y guia_A.json a guia_D.json de la ejecución real; analisis_docente/resumen_docente.json para el criterio original del contrato.

## 4 Análisis de los resultados

| Comparación | Cambio en exactitud | IC 95 % por caso |
|---|---|---|

| B-A | -33.33 puntos | [-68.75, +4.17] |

| C-B | +68.75 puntos | [+37.50, +93.75] |

| D-C | +6.25 puntos | [-12.50, +25.00] |

| D-A | +41.67 puntos | [+20.83, +62.50] |

En C - B y D - A los intervalos quedan por encima de cero. En D - C el intervalo incluye cero, por lo que no puedo concluir una mejora de exactitud al añadir controles con esta muestra. Sí observé una reducción de la fuga detectada, de 6/48 en C a 0/48 en D.

### Diferencia entre criterios de consistencia

El cálculo inicial comprobaba que coincidieran exactamente el texto, las fuentes y la abstención. Al contrastarlo con el evaluador original del curso identifiqué una diferencia: ese evaluador mide si el acierto booleano se mantiene entre repeticiones. Para aplicar el mismo criterio del contrato recalculé las 192 salidas guardadas con el archivo original. No generé respuestas nuevas ni modifiqué las existentes.

| Config. | Criterio docente | Igualdad literal previa |
|---|---|---|

| A | 75.00 % | 0.00 % |

| B | 100.00 % | 31.25 % |

| C | 100.00 % | 18.75 % |

| D | 100.00 % | 31.25 % |

En c01 y c06 las respuestas fueron correctas en las tres repeticiones, aunque cambió su redacción. En c10 ocurrió lo contrario: D se abstuvo en las tres ocasiones, no respondió Idempotency-Key y no citó ing-07. Por eso interpreto la consistencia como estabilidad del resultado, que también puede incluir un error repetido.

D cumple las ocho metas con el criterio original del contrato, pero conserva el fallo de c10. Como mejora posterior considero ampliar los casos de calibración y reforzar la recuperación de preguntas técnicas, manteniendo una evaluación final independiente.

Conservé ambos cálculos: resumen.json contiene la comparación literal; analisis_docente/resumen_docente.json, el criterio original. El archivo del evaluador en referencias/ y su SHA-256 permiten comprobar el recálculo.

## 5 Evidencia y reproducción

### Entorno de ejecución

Ejecuté la evaluación Gemini desde PowerShell en Windows, con Python 3.14.7, en el siguiente directorio:

C:/Users/cesar/OneDrive/Documentos/ChatGPT/Estudiar/laboratorio3_finnorte/finnorte-ia-alumno

El registro de acceso comenzó el 25 de noviembre de 2026 a las 00:29:50 UTC y el proceso terminó a las 00:56:47 UTC. Ambos horarios corresponden al 24 de noviembre en Ciudad de México. El análisis posterior utilizó los archivos guardados, sin llamadas nuevas a Gemini.

### Archivos que respaldan la entrega

| Archivo o carpeta | Qué comprueba |
|---|---|

| estado.json | El proceso terminó y señala las rutas de salida. |

| calibracion.json | Consultas de desarrollo/validación y umbral elegido. |

| evaluacion/A a D | Las 192 salidas por caso y repetición. |

| firma.json y reanudacion_*.json | Mismos insumos; conservación de las quince respuestas anteriores. |

| evaluacion/analisis_docente/ | Recálculo original docente y comparación de consistencia. |

| bitacora/validacion_oficial/ | Comandos, directorios, versiones, hashes, texto y JUnit de pytest. |

~~~powershell
$env:PYTHONPATH = 'herramientas_pruebas;src'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe guia\ejecutar_pruebas_oficiales.py
.\.venv\Scripts\python.exe guia\analizar_con_criterio_docente.py
~~~

El segundo comando procesa las respuestas existentes. Para consultar los resultados no hace falta repetir Gemini. Incluí en el ZIP el código, las pruebas, los registros y las licencias. En otro equipo es necesario crear el entorno virtual e instalar las dependencias de requirements.txt.

### Conclusión

Con esta práctica comprobé cómo cambian las respuestas al añadir recuperación y controles. La configuración D alcanzó 93.75 % de exactitud y cumplió las ocho metas del contrato con su criterio original. El caso c10 y el tamaño de la muestra muestran que todavía hay margen de mejora. Dejé los resultados y los comandos documentados para poder revisar y repetir la evaluación.