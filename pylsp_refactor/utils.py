import logging
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jedi import Script
from jedi.api.classes import Name
from jedi.api.refactoring import Refactoring
from pylsp.workspace import Document, Workspace

from pylsp_refactor.regexes import FUNC_CALL_RE

logger = logging.getLogger(__name__)


@dataclass
class Position:
    line: int
    column: int

    @classmethod
    def from_range_item(cls, ri: dict[str, int]) -> "Position":
        return cls(line=ri["line"], column=ri["character"])

    def to_position(self) -> dict[str, int]:
        return {
            "line": self.line,
            "character": self.column,
        }

    def to_jedi(self) -> tuple[int, int]:
        return self.line + 1, self.column


@dataclass
class Range:
    start: Position
    end: Position

    def to_range(self) -> dict[str, dict[str, int]]:
        return {
            "start": self.start.to_position(),
            "end": self.end.to_position(),
        }


@dataclass
class TextPosition(Range):
    text: str


def parse_range(range: dict[str, dict[str, int]]) -> Range:
    return Range(start=Position.from_range_item(range["start"]), end=Position.from_range_item(range["end"]))


def get_script(document: Document) -> Script:
    return document.jedi_script(
        use_document_path=True,
    )


def find_function_call_at_line(document: Document, line_no: int) -> typing.Optional[TextPosition]:
    line: str = document.lines[line_no]
    match = FUNC_CALL_RE.search(line)
    if not match:
        return None
    start, end = match.span(1)
    jedi_line, jedi_column = Position(line_no, start).to_jedi()
    script = get_script(document)
    infers: list[Name] = script.infer(jedi_line, jedi_column)
    for infer in infers:
        logger.error("%s::%s", infer.line, jedi_line)
        if infer.type == "function" and (infer.module_path != Path(document.path) or infer.line != jedi_line):
            return TextPosition(Position(line_no, start), Position(line_no, end), infer.name)
    return None


def get_text_range_between_sources(original_source: str, new_source: str, original_line_no: int) -> TextPosition:
    original_lines = original_source.splitlines()
    new_lines = new_source.splitlines()

    diff_start_line = 0
    while diff_start_line < original_line_no and original_lines[diff_start_line] == new_lines[diff_start_line]:
        diff_start_line += 1
    start = Position(diff_start_line, 0)
    end = Position(original_line_no, len(original_lines[original_line_no]))
    if diff_start_line == original_line_no:
        text = new_lines[diff_start_line]
        return TextPosition(start, end, text)
    collect_lines = []
    difference_counter = diff_start_line
    while original_lines[diff_start_line] != new_lines[difference_counter] and difference_counter < len(new_lines):
        collect_lines.append(new_lines[difference_counter])
        difference_counter += 1
    while diff_start_line <= original_line_no:
        collect_lines.append(new_lines[difference_counter])
        diff_start_line += 1
        difference_counter += 1
    text = "\n".join(collect_lines)
    return TextPosition(start, end, text)


def is_a_class_def(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("class ")


def is_a_function_def(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("def ")


def is_a_return_statement(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("return ")
