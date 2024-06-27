import re

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
WHITESPACE_RE = re.compile(r"\s")
FUNC_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z_0-9]*)\s*\(")  # ")"
OPEN_PARENTHESI_RE = re.compile(r"\s*\(")  # ")"
