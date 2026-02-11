import shlex

from prettytable import PrettyTable

from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    select,
    update,
)
from src.primitive_db.parser import parse_set, parse_values, parse_where
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

META_FILE = "db_meta.json"

def print_help() -> None:
    print("\n***Операции с данными***\n")
    print("Функции:")
    print(
        '<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - '
        "создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> - "
        "прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> - "
        "удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run() -> None:
    print("\n***База данных***")
    print_help()

    while True:
        metadata = load_metadata(META_FILE)

        user_input = input(">>>Введите команду: ").strip()
        if user_input == "":
            continue

        args = shlex.split(user_input, posix=False)
        command = args[0]

        if command == "exit":
            break

        if command == "help":
            print_help()
            continue

        if command == "list_tables":
            if not metadata:
                continue
            for name in sorted(metadata.keys()):
                print(f"- {name}")
            continue

        if command == "create_table":
            if len(args) < 3:
                print("Некорректное значение: недостаточно аргументов. Попробуйте еще.")
                continue

            table_name = args[1]
            columns = args[2:]
            new_metadata = create_table(metadata, table_name, columns)

            if new_metadata is not metadata or table_name in new_metadata:
                save_metadata(META_FILE, new_metadata)
            continue

        if command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: недостаточно аргументов. Попробуйте еще.")
                continue

            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)

            save_metadata(META_FILE, new_metadata)
            continue

        if command == "insert":
            if len(args) < 5 or args[1] != "into":
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

            table_name = args[2]

            if args[3] != "values":
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

            values_part = " ".join(args[4:])

            try:
                values = parse_values(values_part)
            except ValueError as e:
                print(e)
                continue

            table_data = load_table_data(table_name)
            new_data = insert(metadata, table_name, values, table_data)
            save_table_data(table_name, new_data)
            continue

        if command == "select":
            if len(args) < 3 or args[1] != "from":
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

            table_name = args[2]

            table_data = load_table_data(table_name)

            where_clause = None

            if len(args) > 3:
                if len(args) < 6 or args[3] != "where":
                    print(f"Функции {command} нет. Попробуйте снова.")
                    continue

                where_expr = " ".join(args[4:])
                try:
                    where_clause = parse_where(where_expr)
                except ValueError as e:
                    print(e)
                    continue

            result = select(table_data, where_clause)

            if not result:
                continue

            columns = metadata.get(table_name)
            if not columns:
                continue

            table = PrettyTable()
            table.field_names = [col[0] for col in columns]

            for row in result:
                table.add_row([row.get(col[0]) for col in columns])

            print(table)
            continue

        if command == "update":
            if len(args) < 8:
                print("Некорректное значение: недостаточно аргументов. Попробуйте еще.")
                continue

            table_name = args[1]

            if args[2] != "set":
                print("Некорректное значение: set. Попробуйте снова.")
                continue

            if "where" not in args:
                print("Некорректное значение: where. Попробуйте снова.")
                continue

            where_index = args.index("where")

            set_expr = " ".join(args[3:where_index])
            where_expr = " ".join(args[where_index + 1 :])

            try:
                set_clause = parse_set(set_expr)
                where_clause = parse_where(where_expr)
            except ValueError as e:
                print(e)
                continue

            table_data = load_table_data(table_name)
            new_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, new_data)
            continue

        if command == "delete":
            if len(args) < 6 or args[1] != "from":
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

            table_name = args[2]

            if args[3] != "where":
                print(f"Функции {command} нет. Попробуйте снова.")
                continue

            where_expr = " ".join(args[4:])

            try:
                where_clause = parse_where(where_expr)
            except ValueError as e:
                print(e)
                continue

            table_data = load_table_data(table_name)
            new_data = delete(table_data, where_clause)
            save_table_data(table_name, new_data)
            continue

        if command == "info":
            if len(args) != 2:
                print("Некорректное значение: недостаточно аргументов. Попробуйте еще.")
                continue

            table_name = args[1]
            table_data = load_table_data(table_name)
            info(metadata, table_name, table_data)
            continue


        print(f"Функции {command} нет. Попробуйте снова.")
