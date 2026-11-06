# FinNorte · Equipo 2 · v2-revisor

Revisa código Python mediante detectar → explicar → parche → dictamen. El resultado es un reporte con los hallazgos, «sin hallazgos» o un aviso de revisión fallida. El documento técnico final está en `entregables/`.

## Cierre con cuatro etapas

La nueva comparación A/B/C/D completó **240/240 ejecuciones del motor de cuatro etapas**, con Gemini 3.1 Flash-Lite. Los prompts de Kevin y sus escritos se conservaron. A usa 1/1/1/1 y B/C/D, 4/5/5/2. El contrato mantiene sus metas.

| Configuración | Exactitud | Citas | Alucinación | Fuga PII | Abstención correcta | Consistencia | p95 ms | Costo medio USD | Metas cumplidas |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 0.6500 | 0.3500 | 0.0000 | 0.0000 | 0.8000 | 0.9500 | 49354.2 | 0.001696 | 4/8 |
| B | 0.7000 | 0.5667 | 0.2833 | 0.0000 | 0.8000 | 0.9000 | 38478.4 | 0.001861 | 3/8 |
| C | 0.8000 | 0.9500 | 0.0000 | 0.0000 | 0.8000 | 1.0000 | 39528.1 | 0.002506 | 6/8 |
| D | 0.9500 | 0.9500 | 0.0000 | 0.0000 | 0.9500 | 0.9500 | 59517.3 | 0.002321 | 7/8 |

Evidencia actual: `bitacora/av1_cuatro_etapas_20261105/`. Los fallos se conservan; completar la corrida no significa cumplir todas las metas. La consistencia incluye estado, total y reglas/líneas del dictamen, además de los campos anteriores; no exige igualdad literal del texto.

Para comprobar la comparación actual:

```text
python guia/verificar_evidencias.py
```

Para ejecutar otra comparación real, configura la llave en tu `.env` local y usa una carpeta nueva:

```text
python guia/av1_configuraciones.py --casos evals/v2-revisor.jsonl --rep 3 --cuatro-etapas --salida bitacora/av1_cuatro_nueva
```

Si se interrumpe, repite el mismo comando con `--continuar`, sin cambiar código, modelo, prompts, casos ni contrato. No se recuperan respuestas de tres etapas.

Laboratorio 2 completo: `bitacora/lab2_cuatro_etapas_20261105/a2_matriz.md`, `a2_matriz_v1.md`, trazabilidad y resumen. Se usaron las tres entradas oficiales y tres repeticiones adicionales de transferencias.py. Versión mejorada: 6/6 flujos completos; inicial: 4/6, con fallos reales guardados. Ambas repeticiones conservaron reglas y líneas; eso no acredita exactitud exhaustiva.

```text
python guia/a2_flujo_variante.py --salida bitacora/lab2_cuatro_nuevo
python guia/a2_flujo_variante.py --v1 --salida bitacora/lab2_cuatro_nuevo
```

La etiqueta `avance1-medicion-3-etapas` conserva `5939a14` y sus 240 respuestas históricas. `avance1` se reserva para la entrega integrada al cerrar el PR #7. Para verificar el antecedente sin cambiar tu rama:

```text
python guia/verificar_evidencias.py --carpeta bitacora/av1_gemini31_20261105 --revision avance1-medicion-3-etapas
```

El documento técnico presenta la medición de cuatro etapas en las secciones 8 a 11. La sección 11 y las referencias del anexo se actualizaron por solicitud del usuario el 6 de noviembre; el PDF conserva 12 páginas. Los registros personales de Luis, Alan y César siguen a cargo de sus autores. El profesor se agregará después por el equipo.

## Responsabilidades

| Persona | Parte asignada |
|---|---|
| Luis · Lolmastercraft | Detectar, buscador, Mini-RAG, fuentes, citas y abstención |
| Alan · alanrivera066 | Explicar, esquema y reintento, 20 casos de evaluación |
| César · MajesDo63 | Parche, reglas de negocio y contrato de calidad |
| Kevin · KevinAdmp | Dictamen, reporte final, seis casos, conclusiones e integración del documento final |

Dueños, entradas, salidas, fusión y decisiones fechadas: `avance1/equipo.md`. La preparación y las pruebas tienen asistencia de IA registrada en `ai_log.md`. Los usos personales quedan **PENDIENTES**, por instrucción del usuario; la asignación y la cuenta que publica no acreditan ejecución individual.

## Instalación y pruebas

Python 3.10 o posterior:

```text
python -m venv .venv
```

Windows: `.\.venv\Scripts\Activate.ps1`. Mac/Linux: `source .venv/bin/activate`.

```text
python -m pip install -r requirements.txt
python -m pip install -e .
python -m finnorte info
pytest -q
```

Las pruebas usan fake/hash, sin red: comprueban código, no calidad de un modelo real. Para Gemini, crea `.env` desde `.env.example` y configura la llave solo en ese archivo local, excluido de Git.

## Laboratorio 2

La guía común del profesor está en `guia/s2_flujo_cambios.py`: analizar → plan → checklist → nota. Sus prompts `cambio_*`, esquemas y pruebas originales `tests/test_a2_pipeline.py` están publicados. Este ejemplo de solicitudes de cambio es independiente de la etapa dictamen del revisor.

```text
python guia/s2_flujo_cambios.py --plan-version 1 --directorio bitacora/s2_nuevo_v1
python guia/s2_flujo_cambios.py --plan-version 2 --directorio bitacora/s2_nuevo_v2
```

Con Gemini configurado son llamadas reales; con `LLM_PROVIDER=fake` son demostraciones. Cada corrida escribe en una carpeta nueva y rechaza sobrescribir una anterior sin `--continuar`.

Las matrices históricas reales de la guía están en `bitacora/s2_trazabilidad_plan_v1.json`, `s2_trazabilidad_plan_v2.json` y sus registros de consistencia. Las matrices del revisor están en `bitacora/a2_matriz.md` y `a2_matriz_v1.md`, respaldadas por `a2_trazabilidad*.json` y las trazas de `bitacora/lab2_tres_etapas/`. Se conservan resultados y errores históricos de las tres etapas; se excluyó la cuarta etapa de esas copias. Procedencia y hashes: `bitacora/procedencia_importacion_20261105.json`.

`python guia/a2_flujo_variante.py --demo` comprueba las cuatro etapas con respuestas preparadas; no mide calidad de IA. Sin `--demo`, requiere un proveedor real y escribe nuevas evidencias en `bitacora/publicacion_lab2/flujo/`.

## Etapa dictamen

`rev_dictamen` recibe la salida de `explicar` y `parche` y entrega un reporte con los mismos hallazgos, su parche propuesto y un resumen. `validar_dictamen` ([dictamen.py](src/finnorte/dictamen.py)) rechaza lo que omita, invente o cambie datos recibidos, incluido texto del resumen que no provenga de ellos. El programa arma el reporte final. Si una etapa falla, muestra el aviso de revisión fallida sin datos parciales.

```text
python guia/a2_dictamen.py casos --version 2
python guia/a2_dictamen.py comparar --version 2
```

`casos` usa dos archivos limpios, tres con un problema y uno con dos (`evals/v2-revisor-dictamen.jsonl`). `comparar` usa tres entradas distintas y repite una tres veces. Agrega `--demo` para probar sin modelo real. Las evidencias no se sobrescriben.

| Medida con Gemini 3.1 Flash-Lite, 6 flujos | v1 | v2 |
|---|---:|---:|
| Dictamen válido al primer intento | 1/6 | 6/6 |
| Redacciones del resumen en 3 repeticiones | 3 | 1 |
| Reporte correcto para lo esperado | 6/6 | 6/6 |

Los seis casos con v2 dieron 6/6 reportes correctos. La v1 había pasado 12/12 con el primer validador; leer sus resúmenes mostró texto ajeno a los datos, y por eso se agregó la regla con la que se comparan ambas versiones. Detalle: `bitacora/dictamen/comparacion.md`. Son pocas ejecuciones y archivos pequeños: no demuestran el comportamiento con archivos grandes. El aviso de revisión fallida solo se ha comprobado en pruebas sin red; no ocurrió en estas ejecuciones reales.

## Antecedente de tres etapas y sus mediciones

Versiones del Lab 2: detectar v3, explicar v4, parche v4, dictamen v2. Perfil mejorado del Avance 1: v4/v5/v5. A usa v1/v1/v1; B, C y D usan el perfil mejorado. Los prompts medidos no se editaron. El esquema y reintento están activos en las cuatro configuraciones; D añade controles de negocio, dominio, citas y saneo. A/B/C/D midió tres etapas y conserva esa configuración: `incluir_dictamen` está apagado en el medidor.

Los 20 casos tienen 12 normales, 4 fuera de dominio y 4 límite/adversariales. r06 comprueba que el archivo limpio no tenga hallazgos ni parches, conserve su código y no se abstenga. r09 tiene su texto corregido en UTF-8.

| Evidencia | Qué demuestra |
|---|---|
| `bitacora/av1_cierre/` | Medición histórica completa del 2 de noviembre: 240 respuestas originales y trazas, con sus bytes conservados. Respalda antecedentes citados en A2; su firma no corresponde al código corregido. |
| `bitacora/av1_publicado_20261105/` | Intento anterior con Gemini 3.5: 62/240 respuestas del commit 8742796, conservadas como antecedente de otra firma. |
| `bitacora/av1_gemini31_20261105/` | Medición histórica completa de tres etapas: 240/240 ejecuciones con Gemini 3.1 Flash-Lite, 60 por configuración. Firma de 67 archivos verificada en 5939a14. |
| `bitacora/correccion_av1_pytest_antes.txt` | Pruebas de la copia antes de corregirla. |
| `bitacora/correccion_av1_pytest_despues.txt` | Pruebas ejecutadas después de corregirla; sin modelo real. |

La firma histórica incluye código del sistema, prompts y esquemas, corpus, archivos de entrada, casos, contrato y medidor. Para comprobar esas respuestas desde la rama actual:

```text
python guia/verificar_evidencias.py --carpeta bitacora/av1_gemini31_20261105 --revision avance1-medicion-3-etapas
```

Ese comando consulta la firma de la etiqueta histórica sin cambiar tu rama ni llamar al modelo. El verificador devuelve código 2 si la evidencia está incompleta. La medición nueva de cuatro etapas se verifica contra el código actual con el comando del inicio; usa también las instrucciones del inicio para una nueva corrida.

Mantener el mismo proveedor, modelo, embeddings, contrato y archivos. `--env RUTA_AL_ENV` permite leer una configuración sin copiar la llave al repositorio. Los fallos del proveedor se registran aparte y detienen la corrida. Las metas se conservan aunque alguna no se alcance.

## Actividad 2

Los borradores individuales están en `Actividad 2/Luis/`, `Actividad 2/Cesar/` y `Actividad 2/Alan/`. Sus comparaciones son históricas y sus fuentes de las tres etapas ahora están publicadas. Cada persona debe revisarlos y registrar su participación real. Las secciones técnicas actualizadas del Avance 1 están en [Word](entregables/Documento_Tecnico_Avance1.docx) y [PDF](entregables/Documento_Tecnico_Avance1.pdf), con 11 secciones, las conclusiones y la evidencia de Gemini 3.1. La página de Kevin está en `Actividad 2/Kevin/`, con sus evidencias en `bitacora/dictamen/`.

## Antecedente de Gemini 3.5 · 5 de noviembre

Ese intento terminó con A=60 y B=2; C y D quedaron sin medir en Gemini 3.5. Se guardaron 62/240 respuestas como antecedente. Gemini respondió repetidamente HTTP 503 UNAVAILABLE y tiempos de espera; después de varios reintentos sin progreso se detuvo la corrida. La comparación posterior de Gemini 3.1 sí completó las 240 ejecuciones, sin reutilizar estas respuestas ni las históricas de otra firma.

Esas 62 respuestas corresponden al código del commit `87427960918c2c87fdcc277a70757da13eb157cb`, con firma `1fd3da80456dbb8ade55a0cba3093ba0ac8af2478bbd9e74e48efdd1e69f0230`. Se conservan intactas como comparación parcial anterior. Su manifiesto permite comprobar los 67 archivos en ese commit. No deben verificarse contra el código posterior ni mezclarse con Gemini 3.1.

El PR [#1](https://github.com/alanrivera066/Project_v2_TSTI/pull/1) fue aprobado y fusionado por Alan. La etiqueta `avance1` se actualizó con Lolmastercraft al commit `3fc27aa5e4b6d4b1301bf310ff4d18ddbd322be3`, con la medición completa de 240 ejecuciones. GitHub Actions aprobó 56 pruebas en ese estado. Esa es la base de código y evidencia de la actualización documental; los usos personales de Luis, Alan y César conservan sus pendientes.

## Comparación histórica de tres etapas con Gemini 3.1

El usuario autorizó iniciar A/B/C/D desde cero con otro modelo porque Gemini 3.5 devolvió 503. Gemini 3.1 Flash-Lite respondió a una prueba real de disponibilidad; el buscador también respondió usando `gemini-embedding-001`. Ambas comprobaciones se guardan aparte de las 240 ejecuciones de evaluación.

Esa comparación mantuvo los prompts, casos, metas, embeddings y flujo de tres etapas. Solo cambian el modelo declarado y la estimación del costo por modelo: 0.25 USD de entrada y 1.50 USD de salida por millón de tokens de texto, a tarifa Standard de pago verificada el 5 de noviembre. Fuente: [precios de Google](https://aistudio.google.com/docs/pricing#gemini-3.1-flash-lite). Es una estimación con tokens reales; excluye embeddings y no representa una factura ni confirma cargos en una cuenta gratuita.

En la versión histórica de tres etapas, el verificador usaba por defecto `bitacora/av1_gemini31_20261105/`. En esta rama usa la comparación nueva de cuatro etapas; para la anterior indica carpeta y revisión como se explica al inicio. Las metas no se ajustan para hacer pasar resultados; la calidad se informa aunque no alcance el contrato.

### Interrupción anterior: 163/240

La corrida se interrumpió en A=60, B=60, C=43 y D=0. Gemini 3.1 devolvió HTTP 429 al alcanzar 500 llamadas diarias por proyecto/modelo. La respuesta completa está en `bitacora/av1_gemini31_20261105/av1_cuota_agotada.json`. El usuario proporcionó otra credencial autorizada y se continuaron las 77 ejecuciones restantes sin cambiar de modelo, embeddings, prompts, casos ni metas. El cambio de acceso se registra en `av1_cambio_credencial.json`; las dos llaves quedaron fuera de Git.

Los archivos `av1_comparacion_parcial.md`, `av1_estado_verificado.json` y `av1_interrupcion*.json` conservan ese corte y sus errores como antecedentes. El estado final se consulta en `av1_estado_medicion.json`, `av1_resumen.json` y el verificador.

### Resultado final: 240/240

Las cuatro configuraciones completaron 20 casos con tres repeticiones. La firma de los 67 archivos coincide con el código de la etiqueta `avance1-medicion-3-etapas` (5939a14). Fuente y tabla completa: `bitacora/av1_gemini31_20261105/av1_comparacion.md`; respuestas y métricas: `av1_A.json` a `av1_D.json` y `av1_resumen.json`.

| Configuración | Ejecuciones | Exactitud | Consistencia |
|---|---:|---:|---:|
| A | 60 | 0.60 | 0.90 |
| B | 60 | 0.70 | 0.90 |
| C | 60 | 0.75 | 0.95 |
| D | 60 | 0.95 | 0.95 |

D obtuvo fuga PII=0.00, citas correctas=0.95 y abstención correcta=0.95 en estos casos. Cumplió siete de las ocho metas; falló latencia p95: 66,173.0 ms frente a 12,000 ms. El contrato completo no se declara aprobado. La estimación de costo por ejecución completada fue 0.001570 USD para D; excluye embeddings, ejecuciones interrumpidas y solicitudes sin reporte de tokens, y no es una factura. El costo de todas las llamadas con tokens registrados figura aparte en `av1_integridad.json`.

Los intervalos pareados por caso están en `av1_resumen.json` y en la tabla completa. La prueba de reanudación conservó las 240 respuestas sin llamadas nuevas al modelo: `av1_qa_reanudacion.json`. La evidencia de pruebas locales y CI corresponde a 56 pruebas aprobadas, sin medir calidad de IA. La etapa dictamen se midió aparte y no forma parte de estas 240 ejecuciones.

Los dos comandos siguientes pertenecen al antecedente de tres etapas y se ejecutan solo sobre avance1-medicion-3-etapas:

```text
python guia/av1_reanudar_gemini31.py --env "RUTA_AL_ENV"
python guia/verificar_evidencias.py
```

El primer comando funciona en Windows, Mac y Linux. Fuerza el mismo modelo y embeddings, lee la llave del archivo elegido y conserva las respuestas existentes. No guarda la llave. El segundo certifica las 240 ejecuciones; si faltan datos termina con código 2. Cambiar solo la llave dentro del mismo proyecto no aumenta su cuota.
