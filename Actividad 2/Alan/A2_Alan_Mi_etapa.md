# Mi etapa del flujo de FinNorte

**Borrador asistido por IA: la persona debe leerlo, ejecutar su etapa y ajustarlo con sus palabras antes de entregar**

Alan · Equipo 2 · v2-revisor

## 1 Mi etapa

Mi etapa asignada es explicar, con id rev_explicar. Recibe hallazgos de detectar y código y entrega los mismos hallazgos más explicacion. Mi responsabilidad es revisar y defender esta parte de la revisión de código. La preparación asistida no acredita todavía mi ejecución o autoría individual. Etapa 4: PENDIENTE · Kevin.

## 2 Mi prompt v1

En prompts/rev_explicar.v1.md identifico un rol, restricciones, datos de entrada, formato JSON y manejo de información faltante. Un ejemplo literal es: «Mantén exactamente id, regla y línea de cada uno.». La tarea se divide en etapas; el formato permite comprobar resultados antes de continuar. Si falta información, se pide reconocer el límite y evitar inventar datos.

## 3 Mi validación en código

Mi parte usa reglas.py y la validación de esquema de pipeline.py. Comprueba identidad de los hallazgos, descripción original, referencia a regla y línea, y ciertos identificadores completos. Es código porque debe rechazar el incumplimiento aunque el modelo ignore una instrucción.

Caso guardado: En la comparación real v3/v4, una repetición v3 no cumplió la nueva referencia de línea. Fuente: bitacora/lab2_cierre/casos/alan_trazabilidad__v3__r1.json. Se trata de un requisito ampliado, no de un fallo del contrato anterior.

Error guardado: «La explicación de H1 no identifica la línea 9; el texto debe ser trazable por sí solo».

## 4 Evidencia de ejecución

Extracto del caso real bitacora/lab2_cierre/casos/alan_trazabilidad__v4__r1.json:

```text
prompt: rev_explicar.v4
modelo: gemini-3.5-flash-lite
fecha UTC: 2026-11-01T05:58:25.929964+00:00
etapa: explicar; valida: True; intentos: 1
```

Mi fila en bitacora/av1_a2_matriz.md: explicar | rev_explicar.v4 | 3 hallazgos | válida True | 1 intento(s). La matriz se generó a partir de JSON históricos y no representa nuevas ejecuciones.

## 5 Consistencia

Las tres repeticiones v4 cumplieron el requisito de trazabilidad. Esto no exige texto idéntico ni acredita cobertura universal. Fuente: bitacora/lab2_cierre/metricas.json. No atribuyo estas ejecuciones guardadas a una prueba personal que aún no he realizado.

## 6 Mi mejora y el antes y después

Regla y línea explícitas: 6/9 explicaciones en v3 y 9/9 en v4; casos válidos al primer intento: 2/3 y 3/3. Son tres repeticiones de reportes.py por versión con las mismas entradas previas.

La rúbrica llama a la mejora «v2». Aquí explico la evolución con los números reales de archivo: v1/v2 históricos, revisión v3 y, cuando corresponde, cierre v4. No renombro versiones medidas. En el Avance 1 se añade contexto con detectar v4, explicar v5 y parche v5; sus resultados nuevos A/B/C/D, ya completos, están en bitacora/av1_cierre. Miden el motor conjunto; el antes y después individual sigue siendo el histórico.

## 7 Mis commits y uso de IA

PENDIENTE: lo agrega la persona después de subir con su cuenta.

Este borrador y la integración se prepararon con asistencia de ChatGPT mediante Codex. Debo completar mi uso real de IA en ai_log.md y explicar qué acepté, cambié y validé personalmente.
