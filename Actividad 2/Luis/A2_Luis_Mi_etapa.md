# Mi etapa del flujo de FinNorte

**Borrador asistido por IA: la persona debe leerlo, ejecutar su etapa y ajustarlo con sus palabras antes de entregar**

Luis · Equipo 2 · v2-revisor

## 1 Mi etapa

Mi etapa asignada es detectar, con id rev_detectar. Recibe código numerado y señales estáticas y entrega hallazgos con id, regla, linea y descripcion. Mi responsabilidad es revisar y defender esta parte de la revisión de código. La preparación asistida no acredita todavía mi ejecución o autoría individual. Etapa 4: PENDIENTE · Kevin.

## 2 Mi prompt v1

En prompts/rev_detectar.v1.md identifico un rol, restricciones, datos de entrada, formato JSON y manejo de información faltante. Un ejemplo literal es: «No inventes vulnerabilidades ni números de línea.». La tarea se divide en etapas; el formato permite comprobar resultados antes de continuar. Si falta información, se pide reconocer el límite y evitar inventar datos.

## 3 Mi validación en código

Mi parte usa reglas.py y la validación de esquema de pipeline.py. Comprueba líneas existentes, reglas SEC permitidas, duplicados y cobertura de registros sensibles reconocibles. Es código porque debe rechazar el incumplimiento aunque el modelo ignore una instrucción.

Caso guardado: La respuesta histórica v1 de transferencias.py omitía el registro. El error se obtuvo al revalidarla con el contrato ampliado; no fue un rechazo en vivo de aquella ejecución. Fuente: bitacora/lab2_revision/revalidacion_historica.json.

Referencia del error: Falta SEC-03: registro con dato sensible sin enmascarar en línea 12.

## 4 Evidencia de ejecución

Extracto del caso real bitacora/lab2_revision/casos/flujo_v3__transferencias__1.json:

```text
prompt: rev_detectar.v3
modelo: gemini-3.5-flash-lite
fecha UTC: 2026-11-01T05:38:27.305216+00:00
etapa: detectar; valida: True; intentos: 1
```

Mi fila en bitacora/av1_a2_matriz.md: detectar | rev_detectar.v3 | 5 hallazgos | válida True | 1 intento(s). La matriz se generó a partir de JSON históricos y no representa nuevas ejecuciones.

## 5 Consistencia

El reporte de consistencia conserva una firma estructural en las tres repeticiones v3; el texto varía. Fuente: bitacora/lab2_revision/consistencia_por_etapa.json. No atribuyo estas ejecuciones guardadas a una prueba personal que aún no he realizado.

## 6 Mi mejora y el antes y después

Cuatro hallazgos históricos frente a cinco en la revisión v3; las tres repeticiones de v3 mantuvieron cinco. Cambiaron prompt y preprocesamiento. El historial también usa otro modelo: esta diferencia es descriptiva, no una comparación causal del prompt.

La mejora académica «v2» se identifica aquí con las versiones reales, sin renombrarlas. El Avance 1 conecta contexto con detectar v4; su evaluación nueva A/B/C/D, ya completa, está en bitacora/av1_cierre. Es una medición conjunta del motor y no reemplaza el antes y después histórico de mi etapa.

## 7 Mis commits y uso de IA

PENDIENTE: lo agrega la persona después de subir con su cuenta.

Este borrador y la integración se prepararon con asistencia de ChatGPT mediante Codex. Debo completar mi uso real de IA en ai_log.md y explicar qué acepté, cambié y validé personalmente.
