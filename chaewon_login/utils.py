import re


def is_valid_hex_color(code: str) -> bool:
    return isinstance(code, str) and re.fullmatch(r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", code) is not None