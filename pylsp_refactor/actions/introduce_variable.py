from pylsp_refactor import utils

from .base import CodeAction


class IntroduceVariable(CodeAction):
    title = "Introduce variable"
    kind = "refactor.introduce"
    command = "pylsp_refactor.refactor.introduce.variable"

    def apply(self) -> None:
        new_var_name = "new_variable"
        if self._range.start == self._range.end:
            word = utils.get_word_at_position(self._document, self._range.start)
            if word and utils.is_a_function_call(self._document, word):
                new_var_name = f"{word.text}_result"
        existing_text = utils.get_line_indented_range(self._document, self._range.start.line)
        new_text = f"{new_var_name} = {existing_text.text}"
        new_range = existing_text.to_range()
        workspace_edit = {
            "changes": {
                self._document.uri: [
                    {
                        "range": new_range,
                        "newText": new_text,
                    },
                ],
            },
        }
        self._workspace.apply_edit(workspace_edit)

    def _should_propose_action(self) -> bool:
        if self._range.start != self._range.end:
            return False
        if utils.is_any_def(self._document, self._range.start.line):
            return False
        if utils.is_empty_line(self._document, self._range.start.line):
            return False
        return True
