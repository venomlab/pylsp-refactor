import typing

import pytest

from pylsp_refactor import jedi_utils, utils


@pytest.mark.parametrize(
    ("line", "column", "expected"),
    [
        (2, 5, None),
        (5, 5, None),
        (6, 5, "foo"),
        (7, 5, None),
        (7, 13, None),
        (8, 5, None),
        (8, 11, "foo"),
    ],
)
def test_is_function_call(workspace, document, line, column, expected):
    func: typing.Optional[str] = jedi_utils.get_function_call_at_position(document, utils.Position(line, column))
    if expected is None:
        assert func is None
    else:
        assert func == expected
