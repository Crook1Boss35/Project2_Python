## Управление таблицами

База данных управляется через консольные команды.

### Доступные команды

- `create_table <имя_таблицы> <столбец:тип> ...` — создать таблицу  
  Поддерживаемые типы: `int`, `str`, `bool`.  
  Столбец `ID:int` добавляется автоматически.

- `list_tables` — показать список всех таблиц

- `drop_table <имя_таблицы>` — удалить таблицу

- `help` — показать справку

- `exit` — выйти из программы

### Пример использования

```text
>>> create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>> list_tables
- users

>>> drop_table users
Таблица "users" успешно удалена.```

## Demo

[![asciinema demo](https://asciinema.org/a/pgzktxpPgOP5fufv.svg)](https://asciinema.org/a/pgzktxpPgOP5fufv)

CRUD-операции (Part2)

На этом этапе реализованы операции Create, Read, Update, Delete для работы с данными внутри таблиц.

Данные каждой таблицы хранятся в отдельном JSON-файле в директории data/.

Доступные команды

insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
Добавить запись (ID генерируется автоматически).

select from <имя_таблицы>
Вывести все записи таблицы.

select from <имя_таблицы> where <столбец> = <значение>
Вывести записи по условию.

update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение>
Обновить записи по условию.

delete from <имя_таблицы> where <столбец> = <значение>
Удалить записи по условию.

info <имя_таблицы>
Показать информацию о таблице (схема + количество записей).

help — справка

exit — выход

>>> create_table users name:str age:int is_active:bool

>>> insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

>>> select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei |  28 |    True   |
+----+--------+-----+-----------+

>>> update users set age = 29 where name = "Sergei"
Записи успешно обновлены.

>>> delete from users where ID = 1
Запись с ID=1 успешно удалена.

>>> info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0

## Demo2 CRUD
[![asciinema demo](https://asciinema.org/a/HPVOygMveoUGz93O.svg)](https://asciinema.org/a/HPVOygMveoUGz93O)
