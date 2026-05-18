from __future__ import annotations


NORMALIZATIONS: tuple[tuple[str, str], ...] = (
    ("一るい", "1るい"),
    ("二るい", "2るい"),
    ("三るい", "3るい"),
    ("一・", "1・"),
    ("二・", "2・"),
    ("三・", "3・"),
    ("一つ", "ひとつ"),
    ("一アウト", "1アウト"),
    ("二アウト", "2アウト"),
)


def kids_text(text: str) -> str:
    readable = text
    for source, target in NORMALIZATIONS:
        readable = readable.replace(source, target)
    return readable
