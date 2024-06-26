from typing import TYPE_CHECKING

import jedi
from jedi.api.classes import Name
from pylsp.workspace import Document

from pylsp_refactor.utils import Position

if TYPE_CHECKING:
    from jedi.api.classes import Signature
else:
    Signature = None


def get_script(document: Document) -> jedi.Script:
    return document.jedi_script(
        use_document_path=True,
    )


def get_jedi_line_and_column(position: Position) -> tuple[int, int]:
    return position.line + 1, position.column


def get_function_call_at_position(document: Document, position: Position):
    script = get_script(document)
    line, column = get_jedi_line_and_column(position)
    infers: list[Name] = script.infer(line, column)
    for infer in infers:
        if infer.type == "function" and infer.line != line:
            return infer.name
