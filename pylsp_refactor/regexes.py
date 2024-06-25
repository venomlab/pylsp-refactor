import re

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
OPEN_PARENTHESI_RE = re.compile(r"\s*\(")
WHITESPACE_RE = re.compile(r"\s")
