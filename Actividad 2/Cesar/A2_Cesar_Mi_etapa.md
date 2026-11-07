# Mi etapa del flujo de FinNorte

Cesar · Equipo 2 · v2-revisor

## 1 Mi etapa

Mi etapa asignada es parche, con id rev_parche. Recibe hallazgos explicados y archivo original y entrega parches con id, regla, linea y cambio; codigo_corregido. Mi responsabilidad es revisar y defender esta parte de la revisión de código.

## 2 Mi prompt v1

En prompts/rev_parche.v1.md identifico un rol, restricciones, datos de entrada, formato JSON y manejo de información faltante. Un ejemplo literal es: «El programa compilará tu propuesta sin ejecutarla.». La tarea se divide en etapas; el formato permite comprobar resultados antes de continuar. Si falta información, se pide reconocer el límite y evitar inventar datos.

## 3 Mi validación en código

Mi parte usa reglas.py y la validación de esquema de pipeline.py. Comprueba un parche por hallazgo, identidad, compilación y conservación exacta del archivo limpio. Es código porque debe rechazar el incumplimiento aunque el modelo ignore una instrucción.

Caso guardado: En limites.py histórico v1, el modelo modificó un archivo sin hallazgos y el validador lo rechazó tras dos intentos. Fuente: bitacora/a2_trazabilidad_v1.json. En otra prueba, el esquema rechazó descripcion como campo extra.

Referencia del error: Sin hallazgos se debe conservar exactamente el código original.

## 4 Evidencia de ejecución

Extracto del caso real bitacora/lab2_cierre/casos/cesar_ejemplo__v4__r1.json:

```text
prompt: rev_parche.v4
modelo: gemini-3.5-flash-lite
fecha UTC: 2026-11-01T06:00:32.243590+00:00
etapa: parche; valida: True; intentos: 1
```

Mi fila en bitacora/av1_a2_matriz.md: parche | rev_parche.v4 | 5 parches | válida True | 1 intento(s). La matriz se generó a partir de JSON históricos y no representa nuevas ejecuciones.

## 5 Consistencia

Las tres repeticiones v4 fueron válidas al primer intento. Los archivos propuestos pueden variar; compilar no demuestra equivalencia funcional. 

## 6 Mi mejora y el antes y después

Salidas válidas al primer intento: 2/3 en v3 y 3/3 en v4. La v4 añadió un ejemplo no vacío y prohibió campos extra. Fuente: bitacora/lab2_cierre/metricas.json.

La rúbrica llama a la mejora «v2». Aquí explico la evolución con los números reales de archivo: v1/v2 históricos, revisión v3 y, cuando corresponde, cierre v4. En el Avance 1 se añade contexto con detectar v4, explicar v5 y parche v5; sus resultados nuevos A/B/C/D, ya completos, están en bitacora/av1_cierre. Miden el motor conjunto; el antes y después individual sigue siendo el histórico.

## 7 Mis commits y uso de IA

Mi documento de la Actividad 2 se incorporó al repositorio del equipo mediante el commit [1378a62: Actividad 2](https://github.com/alanrivera066/Project_v2_TSTI/commit/1378a6249e5244af62d754c1d10230faabf57052), registrado con mi cuenta de GitHub, **MajesDo63**. Este commit agrega el documento de mi etapa y sus archivos de apoyo.

Utilicé ChatGPT para comprender el Laboratorio 2, la Actividad 2 y mi responsabilidad en la etapa de parches. También solicité apoyo de Codex para analizar el prompt, el esquema, el validador y las evidencias guardadas. Con asistencia se contrastaron las versiones del prompt y se comprobaron casos como la conservación de un archivo sin hallazgos y el rechazo de código con sintaxis incorrecta.

Los resultados de las ejecuciones y las comparaciones entre versiones se encuentran en las bitácoras del proyecto.
