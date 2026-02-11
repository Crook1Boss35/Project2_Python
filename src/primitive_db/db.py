import json
from pathlib import Path


def new_db() -> dict:
    return {"tables": {}}


def create_table(db: dict, name: str) -> bool:
    tables = db["tables"]
    if name in tables:
        return False
    tables[name] = []
    return True


def list_tables(db: dict) -> list[str]:
    return sorted(db["tables"].keys())


def insert_row(db: dict, table: str, row: dict) -> bool:
    tables = db["tables"]
    if table not in tables:
        return False
    tables[table].append(row)
    return True


def select_rows(db: dict, table: str) -> list[dict] | None:
    tables = db["tables"]
    if table not in tables:
        return None
    return tables[table]


def load_db(path: Path) -> dict:
    if not path.exists():
        return new_db()
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
