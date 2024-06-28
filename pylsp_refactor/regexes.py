import re

FUNC_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z_0-9]*)\s*\(")  # ")"
CAMEL_TO_SNAKE_RE = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
