# Comparación A/B/C/D · Gemini 3.1 Flash-Lite

Fuente: av1_A.json, av1_B.json, av1_C.json, av1_D.json y av1_resumen.json de esta carpeta.
240 ejecuciones reales: 20 casos × 3 repeticiones × 4 configuraciones. Las 62 respuestas anteriores de Gemini 3.5 no se reutilizaron.

| Configuración | Ejecuciones | Exactitud | Consistencia | Citas correctas | Alucinación | Fuga PII | Abstención correcta | Latencia p95 (ms) | Costo medio estimado (USD) | Errores de sistema | Contrato |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 60 | 0.6000 | 0.9000 | 0.3500 | 0.0000 | 0.0500 | 0.8000 | 73083.6 | 0.001040 | 0 | No cumple |
| B | 60 | 0.7000 | 0.9000 | 0.5667 | 0.2667 | 0.0500 | 0.8000 | 47378.0 | 0.001170 | 0 | No cumple |
| C | 60 | 0.7500 | 0.9500 | 0.9500 | 0.0000 | 0.0500 | 0.8000 | 91010.8 | 0.001744 | 0 | No cumple |
| D | 60 | 0.9500 | 0.9500 | 0.9500 | 0.0000 | 0.0000 | 0.9500 | 66173.0 | 0.001570 | 0 | No cumple |

A: prompts 1/1/1. B: 4/5/5. C: B con Mini-RAG. D: C con controles de negocio, dominio, citas y saneo. Esquema y reintento están activos en las cuatro; el filtrado mínimo de sec-11 también se aplica en C.

La consistencia compara los pares (regla, línea) de hallazgos y parches, la abstención y el error entre las tres repeticiones. Esa firma deja fuera la redacción y el contenido del código corregido. La exactitud usa las comprobaciones de los 20 casos; no equivale a precisión exhaustiva del revisor.

El costo medio corresponde a ejecuciones completadas. Se estima con tokens reales y tarifa Standard de pago (0.25/1.50 USD por millón de entrada/salida); excluye embeddings, intentos de ejecuciones interrumpidas y llamadas sin reporte de tokens. No representa una factura. La latencia incluye pausas y reintentos de cada ejecución conservada.

Las metas se mantienen aunque no se alcancen. Kevin sigue PENDIENTE.

## Diferencias pareadas por caso

| Comparación | Diferencia de exactitud | Intervalo 95 % |
|---|---:|---|
| B-A | 0.1000 | [0.0000, 0.2500] |
| C-B | 0.0500 | [0.0000, 0.1500] |
| D-C | 0.2000 | [0.0000, 0.4000] |
| D-A | 0.3500 | [0.1000, 0.6000] |

Intervalos bootstrap de 5,000 remuestreos pareados de los 20 casos; semilla 7. Las tres repeticiones se promedian por caso.
