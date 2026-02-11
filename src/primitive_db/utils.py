import json
import os

from src.primitive_db.constants import DATA_DIR


def load_metadata(filepath: str) -> dict:
    """Загружает метаданные базы данных из файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: dict) -> None:
    """Сохраняет метаданные базы данных в файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_table_data(table_name: str) -> list:
    """Загружает данные таблицы из JSON-файла."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name: str, data: list) -> None:
    """Сохраняет данные таблицы в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
