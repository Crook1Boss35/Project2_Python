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

def insert(metadata: dict, table_name: str, values: list, table_data: list) -> list:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = metadata[table_name]

    expected_values_count = len(columns) - 1

    if len(values) != expected_values_count:
        print("Ошибка: Неверное количество значений.")
        return table_data

    new_record = {}

    if table_data:
        new_id = max(row["ID"] for row in table_data) + 1
    else:
        new_id = 1

    new_record["ID"] = new_id

    for (col_name, col_type), value in zip(columns[1:], values):
        if col_type == "int":
            if not isinstance(value, int):
                print(f'Ошибка: Столбец "{col_name}" должен быть int.')
                return table_data
        elif col_type == "str":
            if not isinstance(value, str):
                print(f'Ошибка: Столбец "{col_name}" должен быть str.')
                return table_data
        elif col_type == "bool":
            if not isinstance(value, bool):
                print(f'Ошибка: Столбец "{col_name}" должен быть bool.')
                return table_data

        new_record[col_name] = value

    table_data.append(new_record)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data

def select(table_data: list, where_clause: dict | None = None) -> list:
    if where_clause is None:
        return table_data

    if len(where_clause) != 1:
        return []

    (key, value), = where_clause.items()

    result = []
    for row in table_data:
        if key in row and row[key] == value:
            result.append(row)

    return result

def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    if len(where_clause) != 1:
        return table_data
    if len(set_clause) != 1:
        return table_data

    (where_key, where_value), = where_clause.items()
    (set_key, set_value), = set_clause.items()

    updated_count = 0

    for row in table_data:
        if where_key in row and row[where_key] == where_value:
            if set_key in row:
                row[set_key] = set_value
                updated_count += 1

    if updated_count == 0:
        print("Ошибка: Записи по условию не найдены.")
        return table_data

    if where_key == "ID":
        print(f"Запись с ID={where_value} успешно обновлена.")
    else:
        print("Записи успешно обновлены.")

    return table_data

def delete(table_data: list, where_clause: dict) -> list:
    if len(where_clause) != 1:
        return table_data

    (key, value), = where_clause.items()

    new_data = []
    deleted_ids = []

    for row in table_data:
        if key in row and row[key] == value:
            deleted_ids.append(row.get("ID"))
        else:
            new_data.append(row)

    if not deleted_ids:
        print("Ошибка: Записи по условию не найдены.")
        return table_data

    if key == "ID":
        print(f'Запись с ID={value} успешно удалена.')
    else:
        print("Записи успешно удалены.")

    return new_data

def info(metadata: dict, table_name: str, table_data: list) -> None:
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    columns_str = ", ".join(f"{name}:{typ}" for name, typ in columns)

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_str}")
    print(f"Количество записей: {len(table_data)}")
