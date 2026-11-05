# Comparación parcial · Gemini 3.1 Flash-Lite

Estado: PENDIENTE DE MEDIR. Hay 163/240 ejecuciones: A=60, B=60, C=43 y D=0. Faltan 77.
La API rechazó más llamadas con HTTP 429: límite diario de 500 por proyecto y modelo. La respuesta completa está en av1_cuota_agotada.json.
El proveedor indicó reinicio aproximado el 6 de noviembre de 2026 a las 02:00 de Ciudad de México.

| Configuración completa | Ejecuciones | Exactitud | Consistencia | Citas correctas | Alucinación | Fuga PII | Abstención correcta | Latencia p95 (ms) | Costo medio estimado (USD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 60 | 0.6000 | 0.9000 | 0.3500 | 0.0000 | 0.0500 | 0.8000 | 73083.6 | 0.001040 |
| B | 60 | 0.7000 | 0.9000 | 0.5667 | 0.2667 | 0.0500 | 0.8000 | 47378.0 | 0.001170 |

Fuentes: av1_A.json y av1_B.json. Cada uno contiene los 20 casos y sus tres repeticiones. C está incompleta y D no se ha medido; no se publican cifras finales ni intervalos A/B/C/D para ellas.
A y B no cumplen todo el contrato. Las metas no se cambiaron. El costo se estima con tokens reales a tarifa Standard de pago 0.25/1.50 USD por millón; excluye embeddings y llamadas sin reporte de tokens. No es una factura.
Las 62 respuestas de Gemini 3.5 y la comparación histórica del 2 de noviembre están separadas y no se reutilizaron.
Los 67 archivos de la firma corresponden al commit f8de85e0b93812f3bfd85c8749542c9ac50c3d49. La validación y procedencia están en av1_verificacion_parcial.txt y av1_procedencia.json.
Kevin sigue PENDIENTE.
