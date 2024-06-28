import re

FUNC_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z_0-9]*)\s*\(")  # ")"
