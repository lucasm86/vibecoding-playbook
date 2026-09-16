#!/usr/bin/env python3
"""Valida las fichas de catalog/entries/ y genera catalog/index.json.

Uso:
    python scripts/build_catalog_index.py

Dependencia unica: PyYAML.
    pip install pyyaml

Recorre catalog/entries/**/*.yaml, valida que cada ficha tenga los campos
obligatorios, una categoria permitida (catalog/CATEGORIES.md) y que su `id`
coincida con el nombre de archivo. Detecta ids duplicados. Si encuentra
errores, los lista todos y termina con codigo de salida distinto de cero sin
escribir catalog/index.json. Si todo esta bien, escribe catalog/index.json
ordenado por categoria e id.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Falta PyYAML. Instalalo con: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
ENTRIES_DIR = CATALOG_DIR / "entries"
CATEGORIES_FILE = CATALOG_DIR / "CATEGORIES.md"
INDEX_FILE = CATALOG_DIR / "index.json"

REQUIRED_FIELDS = [
    "id",
    "url",
    "nombre",
    "categoria",
    "tags",
    "licencia_spdx",
    "archivado",
    "ultimo_push",
    "estrellas",
    "lenguaje_principal",
    "verificado_el",
    "proposito",
    "capacidades",
    "stack_y_dependencias",
    "forma_de_uso",
    "madurez",
    "por_que_nos_sirve",
    "usar_cuando",
    "no_usar_cuando",
    "alternativas",
    "probado_por_nosotros",
    "proyectos_donde_se_uso",
    "compatibilidad_licencia",
    "apto_producto_propietario",
    "riesgo_legal",
    "notas",
]

VALID_FORMA_DE_USO = {"libreria", "cli", "servicio", "api", "referencia-de-codigo"}
VALID_MADUREZ = {"experimental", "estable", "abandonado"}
VALID_COMPATIBILIDAD_LICENCIA = {
    "permisiva",
    "copyleft-debil",
    "copyleft-fuerte",
    "sin-licencia",
    "desconocida",
}
VALID_APTO_PRODUCTO_PROPIETARIO = {"si", "con-condiciones", "no", "a-revisar"}

# Campos que pueden ser null explicito ademas de su tipo normal.
NULLABLE_FIELDS = {"licencia_spdx", "riesgo_legal"}

INDEX_FIELDS = [
    "id",
    "url",
    "categoria",
    "tags",
    "proposito",
    "forma_de_uso",
    "madurez",
    "licencia_spdx",
    "apto_producto_propietario",
    "archivado",
    "probado_por_nosotros",
]


def load_categories() -> set[str]:
    if not CATEGORIES_FILE.exists():
        return set()
    categories = set()
    for line in CATEGORIES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- `") and line.endswith("`"):
            categories.add(line[3:-1])
    return categories


def expected_id_from_filename(path: Path) -> str | None:
    stem = path.stem
    if "__" not in stem:
        return None
    owner, _, repo = stem.partition("__")
    if not owner or not repo:
        return None
    return f"{owner}/{repo}"


def validate_entry(path: Path, data: dict, valid_categories: set[str]) -> list[str]:
    errors = []
    rel = path.relative_to(REPO_ROOT)

    if not isinstance(data, dict):
        return [f"{rel}: el contenido no es un mapeo YAML valido"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{rel}: falta el campo obligatorio '{field}'")

    if errors:
        # Sin todos los campos, seguir validando puede generar KeyError ruidoso.
        return errors

    entry_id = data.get("id")
    if not isinstance(entry_id, str) or "/" not in entry_id:
        errors.append(f"{rel}: 'id' debe tener forma 'owner/repo' (encontrado: {entry_id!r})")
    else:
        expected_id = expected_id_from_filename(path)
        if expected_id is None:
            errors.append(
                f"{rel}: el nombre de archivo debe ser '<owner>__<repo>.yaml'"
            )
        elif entry_id.lower() != expected_id.lower():
            errors.append(
                f"{rel}: 'id' ({entry_id!r}) no coincide con el nombre de archivo "
                f"(esperado {expected_id!r})"
            )

    categoria = data.get("categoria")
    if categoria not in valid_categories:
        errors.append(
            f"{rel}: categoria '{categoria}' no esta en catalog/CATEGORIES.md"
        )
    else:
        parent_dir = path.parent.name
        if parent_dir != categoria:
            errors.append(
                f"{rel}: la carpeta contenedora ('{parent_dir}') no coincide con "
                f"'categoria' ('{categoria}')"
            )

    forma_de_uso = data.get("forma_de_uso")
    if forma_de_uso not in VALID_FORMA_DE_USO:
        errors.append(
            f"{rel}: forma_de_uso '{forma_de_uso}' invalido "
            f"(valores permitidos: {sorted(VALID_FORMA_DE_USO)})"
        )

    madurez = data.get("madurez")
    if madurez not in VALID_MADUREZ:
        errors.append(
            f"{rel}: madurez '{madurez}' invalido "
            f"(valores permitidos: {sorted(VALID_MADUREZ)})"
        )

    compat = data.get("compatibilidad_licencia")
    if compat not in VALID_COMPATIBILIDAD_LICENCIA:
        errors.append(
            f"{rel}: compatibilidad_licencia '{compat}' invalido "
            f"(valores permitidos: {sorted(VALID_COMPATIBILIDAD_LICENCIA)})"
        )

    apto = data.get("apto_producto_propietario")
    if apto not in VALID_APTO_PRODUCTO_PROPIETARIO:
        errors.append(
            f"{rel}: apto_producto_propietario '{apto}' invalido "
            f"(valores permitidos: {sorted(VALID_APTO_PRODUCTO_PROPIETARIO)})"
        )

    for field in ("tags", "capacidades", "usar_cuando", "no_usar_cuando", "alternativas", "proyectos_donde_se_uso"):
        if not isinstance(data.get(field), list):
            errors.append(f"{rel}: '{field}' debe ser una lista")

    for field in ("archivado", "probado_por_nosotros"):
        if not isinstance(data.get(field), bool):
            errors.append(f"{rel}: '{field}' debe ser booleano (true/false)")

    for field in NULLABLE_FIELDS:
        value = data.get(field)
        if value is not None and not isinstance(value, str):
            errors.append(f"{rel}: '{field}' debe ser string o null")

    if not isinstance(data.get("por_que_nos_sirve"), str) or not data["por_que_nos_sirve"].strip():
        errors.append(f"{rel}: 'por_que_nos_sirve' es obligatorio y no puede estar vacio")

    return errors


def main() -> int:
    if not ENTRIES_DIR.exists():
        print(f"No existe {ENTRIES_DIR}", file=sys.stderr)
        return 2

    valid_categories = load_categories()
    yaml_files = sorted(ENTRIES_DIR.rglob("*.yaml"))

    all_errors: list[str] = []
    entries: list[dict] = []
    seen_ids: dict[str, Path] = {}

    for path in yaml_files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            all_errors.append(f"{path.relative_to(REPO_ROOT)}: YAML invalido ({exc})")
            continue

        errors = validate_entry(path, data, valid_categories)
        if errors:
            all_errors.extend(errors)
            continue

        entry_id = data["id"]
        if entry_id in seen_ids:
            all_errors.append(
                f"id duplicado '{entry_id}': {seen_ids[entry_id].relative_to(REPO_ROOT)} "
                f"y {path.relative_to(REPO_ROOT)}"
            )
            continue
        seen_ids[entry_id] = path

        rel_path = path.relative_to(REPO_ROOT).as_posix()
        entries.append({**{k: data[k] for k in INDEX_FIELDS}, "ficha": rel_path})

    if all_errors:
        print(f"Se encontraron {len(all_errors)} error(es):\n", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    entries.sort(key=lambda e: (e["categoria"], e["id"]))

    INDEX_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"OK: {len(entries)} ficha(s) validada(s). Escrito {INDEX_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
