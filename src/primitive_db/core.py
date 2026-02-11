SUPPORTED_TYPES = {"int", "str", "bool"}


def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict:
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed: list[tuple[str, str]] = []

    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        name, type_name = col.split(":", 1)

        if type_name not in SUPPORTED_TYPES:
            print(f"Некорректное значение: {type_name}. Попробуйте снова.")
            return metadata

        parsed.append((name, type_name))

    # Автоматически добавляем ID:int в начало
    full_columns = [("ID", "int")] + parsed
    metadata[table_name] = full_columns

    cols_str = ", ".join([f"{n}:{t}" for n, t in full_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata
