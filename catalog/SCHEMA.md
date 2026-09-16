# Schema de una ficha de catálogo

Cada archivo en `entries/<categoria>/<owner>__<repo>.yaml` es un objeto YAML
plano (sin anidamiento salvo listas) con las claves descritas abajo. Claves en
`snake_case`, sin tildes. `scripts/build_catalog_index.py` valida esta forma.

Convención de nombre de archivo: `<owner>__<repo>.yaml` (doble guion bajo),
todo en minúsculas, igual que aparecen en la URL de GitHub. Ejemplo: el
repositorio `https://github.com/Some-Org/CoolTool` se archiva como
`entries/utilidades/some-org__cooltool.yaml`.

## Obligatorio vs. opcional

Todos los campos listados abajo son **obligatorios** salvo que se indique lo
contrario. Un campo obligatorio sin valor conocido todavía se marca `null`
explícito (nunca se omite la clave), excepto donde el schema ya permite `null`
como valor válido (ver `licencia_spdx`, `riesgo_legal`).

## Identificación

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | string | `"<owner>/<repo>"` exacto, tal como en la URL de GitHub. Debe coincidir con el nombre de archivo (`<owner>__<repo>.yaml`, mismo owner/repo en minúsculas). |
| `url` | string | URL completa del repositorio en GitHub. |
| `nombre` | string | Nombre legible del proyecto (puede diferir del nombre del repo). |
| `categoria` | string | Una de las categorías listadas en `CATEGORIES.md`. |
| `tags` | list[string] | Lista corta (3-6) de términos en minúsculas, libres pero descriptivos. |

## Metadatos verificables

Se obtienen de la API de GitHub (`gh api repos/<owner>/<repo>` o equivalente),
**nunca a ojo ni por memoria**. Si un dato no está disponible, se documenta
como tal, no se inventa.

| Campo | Tipo | Descripción |
|---|---|---|
| `licencia_spdx` | string \| null | Identificador SPDX (`MIT`, `Apache-2.0`, `GPL-3.0`, etc.) según GitHub. `null` si el repo no declara licencia. |
| `archivado` | bool | Valor de `archived` en la API de GitHub. |
| `ultimo_push` | string (fecha ISO 8601) | Valor de `pushed_at`. |
| `estrellas` | int | Valor de `stargazers_count` al momento de verificar. |
| `lenguaje_principal` | string | Valor de `language` en la API de GitHub. |
| `verificado_el` | string (fecha ISO 8601, `AAAA-MM-DD`) | Fecha en que se consultó la API para llenar esta ficha o su última actualización. |

## Contenido técnico

| Campo | Tipo | Descripción |
|---|---|---|
| `proposito` | string | Una o dos oraciones: qué hace el repo, en lenguaje llano. |
| `capacidades` | list[string] | Funciones concretas y verificables (ej. `"extrae texto de PDFs escaneados con OCR"`), no frases de marketing (ej. no `"la mejor solución de OCR"`). |
| `stack_y_dependencias` | string | Lenguaje, runtime, dependencias fuertes o requisitos de infraestructura relevantes para integrarlo. |
| `forma_de_uso` | string (enum) | Una de: `libreria`, `cli`, `servicio`, `api`, `referencia-de-codigo`. |
| `madurez` | string (enum) | Una de: `experimental`, `estable`, `abandonado`. Ver criterio abajo. |

### Criterio de madurez

- **`estable`**: releases con versionado semántico o tags regulares, o adopción
  amplia (uso en producción documentado, estrellas + issues resueltos), y sin
  incompatibilidades rotas abiertas hace mucho tiempo.
- **`experimental`**: funciona pero cambia de API con frecuencia, tiene pocas
  releases, o el propio README lo marca como beta/WIP/pre-1.0.
- **`abandonado`**: `archivado: true`, o `ultimo_push` de más de ~18 meses sin
  actividad y sin fork mantenido activo, o el README indica explícitamente que
  el proyecto fue discontinuado.

## Criterio (la parte más importante)

| Campo | Tipo | Descripción |
|---|---|---|
| `por_que_nos_sirve` | string | **Obligatorio.** Qué aportamos nosotros concretamente al cargar esta ficha — no repetir el propósito del repo, sino el motivo por el que está en nuestro catálogo. |
| `usar_cuando` | list[string] | Situaciones concretas donde esta entrada es la elección correcta. |
| `no_usar_cuando` | list[string] | Situaciones donde, aunque parezca aplicable, no conviene usarla. |
| `alternativas` | list[string] | IDs (`owner/repo`) de otras entradas del catálogo, o URLs externas, que cubren un caso similar. Puede estar vacía. |
| `probado_por_nosotros` | bool | `true` si alguien del equipo lo usó en un proyecto real, no solo lo evaluó. |
| `proyectos_donde_se_uso` | list[string] | Nombres de proyectos internos donde se usó. Puede estar vacía. |

## Riesgos

| Campo | Tipo | Descripción |
|---|---|---|
| `compatibilidad_licencia` | string (enum) | Una de: `permisiva`, `copyleft-debil`, `copyleft-fuerte`, `sin-licencia`, `desconocida`. Ver regla de clasificación abajo. |
| `apto_producto_propietario` | string (enum) | Una de: `si`, `con-condiciones`, `no`, `a-revisar`. |
| `riesgo_legal` | string \| null | Nota breve sobre riesgos que no son de licencia: términos de uso de sitios de terceros (scraping), datos personales bajo la Ley 25.326, carga sobre servidores ajenos, uso de APIs con cuotas, etc. `null` si no aplica ninguno. |
| `notas` | string | Cualquier otra aclaración relevante. Puede ser una cadena vacía `""` si no hay nada que agregar. |

### Regla de clasificación de licencias

Esta tabla es normativa; no se decide caso por caso.

| `licencia_spdx` | `compatibilidad_licencia` | `apto_producto_propietario` |
|---|---|---|
| `MIT`, `BSD-2-Clause`, `BSD-3-Clause`, `Apache-2.0`, `ISC` | `permisiva` | `si` |
| `LGPL-2.1`, `LGPL-3.0`, `MPL-2.0` | `copyleft-debil` | `con-condiciones` |
| `GPL-2.0`, `GPL-3.0`, `AGPL-3.0` | `copyleft-fuerte` | `no` (si se incorpora código del repo al producto). La `AGPL` además obliga a liberar el código propio si el software se ofrece como servicio en red, aunque no se distribuya el binario. |
| `null` (sin licencia declarada) | `sin-licencia` | `no` por defecto — sin licencia explícita, la ley asume todos los derechos reservados por el autor. |
| Licencia no cubierta arriba o dudosa | `desconocida` | `a-revisar` |

`apto_producto_propietario` puede bajar de `si`/`con-condiciones` a `a-revisar`
si `riesgo_legal` documenta un problema no relacionado con la licencia (ej. el
repo depende de scraping de un sitio cuyos ToS lo prohíben).

## Ejemplo mínimo de tipos

```yaml
tags: ["pdf", "extraccion", "python"]
capacidades:
  - "extrae texto plano de PDFs con capa de texto"
alternativas: []
proyectos_donde_se_uso: []
riesgo_legal: null
notas: ""
```
