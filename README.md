

Primitive DB
Консольная база данных на Python с поддержкой управления таблицами, CRUD-операций, декораторов, кэширования и логирования времени выполнения.
Проект хранит данные в JSON-файлах и использует декораторы и замыкания.

Установка
poetry install

Запуск
poetry run database

Управление таблицами
create_table <имя> <столбец:тип> ...
list_tables
drop_table <имя>
info <имя>
Поддерживаемые типы: int, str, bool

CRUD-операции
insert into <таблица> values (...)
select from <таблица>
select from <таблица> where <поле> = <значение>
update <таблица> set <поле> = <значение> where <поле> = <значение>
delete from <таблица> where <поле> = <значение>

Данные каждой таблицы хранятся в файле:
data/<table_name>.json

Декораторы:

handle_db_errors: обработка ошибок:
KeyError, ValueError, FileNotFoundError

confirm_action(action_name) применён к:
drop_table
delete

log_time: замеряет время выполнения функции. Применён к:
insert
select

create_cacher(): создаёт замыкание для кэширования результатов.
Используется для кэширования одинаковых запросов select.

Кэш автоматически очищается после:
insert, update, delete, drop_table

Прмиер работы:
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
update users set age = 29 where name = "Sergei"
delete from users where ID = 1
info users

## Demo
[![asciinema demo](https://asciinema.org/a/pgzktxpPgOP5fufv.svg)](https://asciinema.org/a/pgzktxpPgOP5fufv)
## Demo2 CRUD
[![asciinema demo](https://asciinema.org/a/HPVOygMveoUGz93O.svg)](https://asciinema.org/a/HPVOygMveoUGz93O)
## Demo3 Decoratory
[![asciinema demo](https://asciinema.org/a/EKcqiwPOw1rhta17.svg)](https://asciinema.org/a/EKcqiwPOw1rhta17)
