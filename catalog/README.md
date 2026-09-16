# Catálogo de repositorios

> Referencia curada de repositorios de GitHub que el agente **Architect**
> consulta antes de proponer construir un componente desde cero o salir a
> buscar en internet. Convive con el resto de este playbook; no lo reemplaza.

## Qué es

Una colección de fichas (`entries/<categoria>/<owner>__<repo>.yaml`), una por
repositorio evaluado, con metadatos verificables (licencia, actividad,
estrellas) y, sobre todo, **criterio propio**: por qué nos sirve, cuándo usarlo,
cuándo no, y qué riesgo legal o de licencia implica.

No es una lista de "repos copados". Cada entrada existe porque alguien la
evaluó con el schema completo — especialmente el campo `por_que_nos_sirve`,
que es obligatorio y es la razón de ser del catálogo.

## Estructura

```text
catalog/
├── README.md          ← este archivo
├── SCHEMA.md           ← definición de cada campo, tipos, enums, obligatoriedad
├── CATEGORIES.md        ← lista cerrada de categorías permitidas
├── TEMPLATE.yaml         ← ficha vacía para copiar
├── entries/
│   └── <categoria>/
│       └── <owner>__<repo>.yaml
└── index.json          ← GENERADO por scripts/build_catalog_index.py, nunca a mano
```

## Cómo lo usa el Architect

Ver la sección correspondiente en [`../agents/ARCHITECT.md`](../agents/ARCHITECT.md).
En resumen: antes de diseñar un componente desde cero, lee `catalog/index.json`,
abre las fichas relevantes, y justifica en el diseño por qué usa o descarta
cada una citando `usar_cuando` / `no_usar_cuando`.

## Cómo agregar una entrada

1. Confirmá la categoría en [`CATEGORIES.md`](CATEGORIES.md). Si no encaja
   ninguna, leé la sección de esa lista sobre cómo agregar una nueva.
2. Copiá [`TEMPLATE.yaml`](TEMPLATE.yaml) a
   `entries/<categoria>/<owner>__<repo>.yaml` (owner y repo en minúsculas,
   separados por doble guion bajo).
3. Completá todos los campos obligatorios. Los metadatos verificables
   (`licencia_spdx`, `archivado`, `ultimo_push`, `estrellas`,
   `lenguaje_principal`) salen de la API de GitHub, nunca a ojo:

   ```bash
   gh api repos/<owner>/<repo> --jq '{license: .license.spdx_id, archived: .archived, pushed_at: .pushed_at, stars: .stargazers_count, language: .language}'
   ```

   Poné la fecha del día en `verificado_el`.
4. Completá el criterio (`por_que_nos_sirve`, `usar_cuando`, `no_usar_cuando`,
   etc.) con honestidad — es la parte que un buscador de GitHub no te da.
5. Clasificá la licencia siguiendo la tabla normativa en
   [`SCHEMA.md`](SCHEMA.md#regla-de-clasificación-de-licencias).
6. Corré el script de validación/build antes de commitear:

   ```bash
   python scripts/build_catalog_index.py
   ```

   Si hay errores (campo faltante, categoría inválida, id duplicado, id que no
   coincide con el nombre de archivo), el script los lista y termina con
   código de salida distinto de cero sin tocar `index.json`.
7. Commiteá la ficha nueva y el `index.json` regenerado juntos.

## Mantenimiento

- Re-verificá una ficha (actualizá `verificado_el` y los metadatos de GitHub)
  cuando la vayas a usar y hayan pasado más de 6 meses desde la última
  verificación, o cuando notes que el repo cambió de estado (archivado,
  licencia, etc.).
- Nunca edites `index.json` a mano — se pisa en el próximo build.
- Si un repo se archiva o queda abandonado, actualizá `archivado` / `madurez`
  en su ficha en vez de borrarla: la entrada sigue siendo información útil
  (como señal de alerta) aunque ya no se recomiende usarla.
