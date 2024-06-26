import typing
from dataclasses import dataclass

from pylsp.workspace import Document

from pylsp_refactor.regexes import OPEN_PARENTHESI_RE, WHITESPACE_RE, WORD_RE


@dataclass
class Position:
    line: int
    column: int

    @classmethod
    def from_range_item(cls, ri: dict[str, int]) -> "Position":
        return cls(line=ri["line"], column=ri["character"])


@dataclass
class Range:
    start: Position
    end: Position

    def to_range(self) -> dict[str, dict[str, int]]:
        return {
            "start": {
                "line": self.start.line,
                "character": self.start.column,
            },
            "end": {
                "line": self.end.line,
                "character": self.end.column + 1,
            },
        }


@dataclass
class TextPosition(Range):
    text: str


def parse_range(range: dict[str, dict[str, int]]) -> Range:
    return Range(start=Position.from_range_item(range["start"]), end=Position.from_range_item(range["end"]))


def is_a_class_def(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("class ")


def is_a_function_def(document: Document, line_no: int) -> bool:
    line: str = document.lines[line_no]
    return line.lstrip().startswith("def ")


def is_any_def(document: Document, line_no: int) -> bool:
    return is_a_function_def(document, line_no) or is_a_class_def(document, line_no)


def is_empty_line(document: Document, line_no: int) -> bool:
    return not document.lines[line_no].strip()


def is_a_function_call(
    document: Document,
    word_position: TextPosition,
) -> typing.Optional[TextPosition]:
    if is_a_function_def(document, word_position.start.line):
        return None
    line = document.lines[word_position.end.line]
    if OPEN_PARENTHESI_RE.match(line, word_position.end.column + 1) is None:
        return None
    return word_position


def get_word_at_position(document: Document, position: Position) -> typing.Optional[TextPosition]:
    line = document.lines[position.line]
    start = end = position.column
    while WORD_RE.fullmatch(line, start - 1, end) and start > 0:
        start -= 1
    while WORD_RE.fullmatch(line, start, end + 1) and end < len(line):
        end += 1
    word = line[start:end]
    if not WORD_RE.fullmatch(word):
        return None
    return TextPosition(
        text=word,
        start=Position(
            line=position.line,
            column=start,
        ),
        end=Position(
            line=position.line,
            column=end - 1,
        ),
    )


def get_line_indented_range(document: Document, line_no: int) -> TextPosition:
    line = document.lines[line_no]
    start = 0
    end = len(line.rstrip())
    while WHITESPACE_RE.match(line[start]):
        start += 1
    return TextPosition(
        text=line[start:end],
        start=Position(line=line_no, column=start),
        end=Position(line=line_no, column=end - 1),
    )
