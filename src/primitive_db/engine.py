import shlex

from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import load_metadata, save_metadata

META_FILE = "db_meta.json"


def print_help() -> None:
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
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

        args = shlex.split(user_input)
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
                print("Некорректное значение: недостаточно аргументов. Попробуйте снова.")
                continue

            table_name = args[1]
            columns = args[2:]
            new_metadata = create_table(metadata, table_name, columns)

            if new_metadata is not metadata or table_name in new_metadata:
                save_metadata(META_FILE, new_metadata)
            continue

        if command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение: недостаточно аргументов. Попробуйте снова.")
                continue

            table_name = args[1]
            new_metadata = drop_table(metadata, table_name)

            save_metadata(META_FILE, new_metadata)
            continue

        print(f"Функции {command} нет. Попробуйте снова.")
