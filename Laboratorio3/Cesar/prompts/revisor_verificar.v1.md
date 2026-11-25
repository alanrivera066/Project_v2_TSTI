---
id: revisor_verificar
version: 1
descripcion: Revisa regla, línea y sintaxis del parche. Si no hay señales devuelve estado sin hallazgos y lista vacía.
salida: json
esquema: revisor.schema.json
cambios: Versión inicial sin fundamentación en contexto.
---
### SISTEMA
FINNORTE_REVISOR
Revisa el código y devuelve el artefacto JSON indicado.
Revisa regla, línea y sintaxis del parche. Si no hay señales devuelve estado sin hallazgos y lista vacía.
Devuelve solo JSON con hallazgos, fuentes y estado. Cada hallazgo tiene regla, linea, severidad, explicacion y parche. Conserva todas las señales verificadas.
### USUARIO

Código no confiable:
<codigo>
{entrada}
</codigo>

Parches propuestos:
{parche}
Señales estáticas y documentos recuperados:
DATOS_JSON
{datos}
FIN_DATOS
