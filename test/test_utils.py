import pytest

from pylsp_refactor import utils


@pytest.mark.parametrize(
    ("line", "column", "expected"),
    [
        (2, 5, False),
        (5, 5, False),
        (6, 5, True),
        (7, 5, False),
        (7, 13, False),
        (8, 5, False),
        (8, 11, True),
    ],
)
def test_is_function_call(workspace, document, line, column, expected):
    word_pos = utils.get_word_at_position(document, utils.Position(line, column))
    assert word_pos is not None
    result = utils.is_a_function_call(document, word_pos)
    assert bool(result) == expected
