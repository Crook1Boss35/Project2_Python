import ast
import re

"""Разбирают str/ values/ where/ set в список/ словарь."""

def parse_literal(raw: str):
    s = raw.strip()

    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False

    if ((s.startswith('"') and s.endswith('"'))
        or (s.startswith("'") and s.endswith("'"))):
        return s[1:-1]

    try:
        return int(s)
    except ValueError as exc:
        raise ValueError(f"Некорректное значение: {raw}. Попробуйте снова.") from exc

def parse_values(values_part: str) -> list:
    text = values_part.strip()
    if not (text.startswith("(") and text.endswith(")")):
        raise ValueError("Некорректное значение: values. Попробуйте снова.")

    normalized = re.sub(r"\btrue\b", "True", text, flags=re.IGNORECASE)
    normalized = re.sub(r"\bfalse\b", "False", normalized, flags=re.IGNORECASE)

    try:
        parsed = ast.literal_eval(normalized)
    except (ValueError, SyntaxError) as exc:
        raise ValueError("Некорректное значение: values. Попробуйте снова.") from exc

    if isinstance(parsed, tuple):
        return list(parsed)
    if isinstance(parsed, list):
        return parsed

    raise ValueError("Некорректное значение: values. Попробуйте снова.")

def parse_assignment(expr: str) -> tuple[str, object]:
    if "=" not in expr:
        raise ValueError(f"Некорректное значение: {expr}. Попробуйте снова.")

    left, right = expr.split("=", 1)
    key = left.strip()
    if not key:
        raise ValueError(f"Некорректное значение: {expr}. Попробуйте снова.")

    value = parse_literal(right.strip())
    return key, value


def parse_where(expr: str) -> dict:
    key, value = parse_assignment(expr)
    return {key: value}


def parse_set(expr: str) -> dict:
    key, value = parse_assignment(expr)
    return {key: value}
