import typing
from dataclasses import dataclass
from pathlib import Path

from jedi import Script
from pylsp.workspace import Document

from pylsp_refactor.regexes import CAMEL_TO_SNAKE_RE, FUNC_CALL_RE

if typing.TYPE_CHECKING:
    from jedi.api.classes import Name


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


@dataclass
class Call(Range):
    name: str
    type_: typing.Literal["function", "class"]


def parse_range(range_: dict[str, dict[str, int]]) -> Range:
    return Range(start=Position.from_range_item(range_["start"]), end=Position.from_range_item(range_["end"]))


def get_script(document: Document) -> Script:
    return document.jedi_script(
        use_document_path=True,
    )


def find_call_at_line(document: Document, line_no: int) -> typing.Optional[Call]:
    line: str = document.lines[line_no]
    match = FUNC_CALL_RE.search(line)
    if not match:
        return None
    start, end = match.span(1)
    jedi_line, jedi_column = Position(line_no, start).to_jedi()
    script = get_script(document)
    infers: list[Name] = script.infer(jedi_line, jedi_column)
    for infer in infers:
        if infer.type in ["function", "class"] and (
            infer.module_path != Path(document.path) or infer.line != jedi_line
        ):
            return Call(Position(line_no, start), Position(line_no, end), infer.name, infer.type)
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


def is_a_return_statement(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("return ")


def camel_to_snake(text: str) -> str:
    return CAMEL_TO_SNAKE_RE.sub("_", text).lower()
