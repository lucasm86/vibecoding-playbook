# Categorías permitidas

Lista cerrada. Cada ficha en `entries/<categoria>/` debe usar exactamente una de
estas categorías (coincide con el nombre de la subcarpeta y con el campo
`categoria` del YAML). El script `scripts/build_catalog_index.py` rechaza
cualquier valor fuera de esta lista.

- `scraping`
- `automatizacion-navegador`
- `pdf-documentos`
- `ocr`
- `llm-agentes`
- `backend-apis`
- `frontend-ui`
- `datos-etl`
- `auth-seguridad`
- `testing`
- `devops-ci`
- `integraciones-mensajeria`
- `utilidades`

## Agregar una categoría nueva

Esta lista es deliberadamente corta y estable. Antes de agregar una categoría:

1. Confirmá que ninguna categoría existente encaja, ni siquiera de forma
   aproximada.
2. Agregala acá primero, en orden alfabético no es necesario pero sí que quede
   explicada en una línea si el nombre no es autoevidente.
3. Recién después creá `entries/<categoria-nueva>/`.

No crees categorías de una sola entrada "por las dudas"; si dudás, usá
`utilidades` y reclasificá cuando aparezca una segunda entrada similar.
