from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def handle_db_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """Обрабатывает типовые ошибки БД."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        def fallback() -> Any:
            if args and isinstance(args[0], (dict, list)):
                return args[0]
            return None

        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
            return fallback()
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
            return fallback()
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return fallback()
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return fallback()

    return wrapper


def confirm_action(
    action_name: str,) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Запрашивает подтверждение перед опасной операцией."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()
            if answer != "y":
                print("Операция отменена.")
                if args and isinstance(args[0], (dict, list)):
                    return args[0]
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """Замеряет время выполнения функции и печатает результат."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper


def create_cacher() -> Callable[[Any, Callable[[], Any]], Any]:
    """Создаёт замыкание для кэширования результатов запросов."""
    cache: dict[Any, Any] = {}

    def cache_result(key: Any, value_func: Callable[[], Any]) -> Any:
        if key in cache:
            return cache[key]
        value = value_func()
        cache[key] = value
        return value

    setattr(cache_result, "clear", cache.clear)

    return cache_result

