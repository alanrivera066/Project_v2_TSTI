# Comparación A/B/C/D de cuatro etapas

240 ejecuciones reales: 20 casos × 3 repeticiones × 4 configuraciones. Se conserva aparte la medición anterior de tres etapas.
A: 1/1/1/1; B: 4/5/5/2; C: B + RAG; D: C + controles de negocio, citas, dominio y saneo. Esquema y reintento activos en las cuatro.

| Configuración | Exactitud | Citas | Alucinación | Fuga PII | Abstención correcta | Consistencia | p95 ms | Costo medio USD | Metas cumplidas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 0.6500 | 0.3500 | 0.0000 | 0.0000 | 0.8000 | 0.9500 | 49354.2 | 0.001696 | 4/8 |
| B | 0.7000 | 0.5667 | 0.2833 | 0.0000 | 0.8000 | 0.9000 | 38478.4 | 0.001861 | 3/8 |
| C | 0.8000 | 0.9500 | 0.0000 | 0.0000 | 0.8000 | 1.0000 | 39528.1 | 0.002506 | 6/8 |
| D | 0.9500 | 0.9500 | 0.0000 | 0.0000 | 0.9500 | 0.9500 | 59517.3 | 0.002321 | 7/8 |

La consistencia compara abstención, errores y reglas/líneas de hallazgos y parches; incluye además estado, total y reglas/líneas del dictamen. No exige igualdad literal de explicaciones, parches o resumen.
La exactitud comprueba las expectativas definidas, no toda vulnerabilidad posible. Las citas se califican aparte; un caso sin fuentes exigidas puede aprobarlas. Alucinación cuenta errores de citas marcadas como no recuperadas: cero no acredita ausencia general de invenciones. La comprobación registra errores en las cuatro configuraciones; solo D bloquea la entrega por ellos.
Los fallos de validación se conservan. Los fallos de proveedor detienen y permiten reanudar; no se cuentan como respuestas medidas.
El costo es estimado, no una factura. La latencia incluye pausas por límite de llamadas, red, servicio y reintentos de cada ejecución retenida.

| Comparación | Diferencia | Intervalo 95 % |
|---|---:|---|
| B-A | 0.0500 | [-0.1000, 0.2000] |
| C-B | 0.1000 | [0.0000, 0.2500] |
| D-C | 0.1500 | [-0.0500, 0.3500] |
| D-A | 0.3000 | [0.0500, 0.5500] |

Bootstrap pareado por caso, 5,000 remuestreos, semilla 7; media de tres repeticiones por caso. Las metas originales se mantienen.
