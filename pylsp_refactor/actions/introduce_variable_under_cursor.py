from typing import Any

from jedi.api.refactoring import Refactoring

from pylsp_refactor import utils

from .base import CodeAction


class IntroduceVariableUnderCursor(CodeAction):
    title = "Introduce variable"
    kind = "refactor.introduce"
    command = "pylsp_refactor.refactor.introduce_variable_under_cursor"

    def apply(self, arguments: tuple[str, dict[str, int], ...]) -> None:
        func_name: str = arguments[2].lower()
        if func_name.startswith("get_") and len(func_name) > 4:
            variable_name = func_name[4:]
        elif func_name.startswith("get") and len(func_name) > 3:
            variable_name = func_name[3:]
        elif func_name.startswith("find_") and len(func_name) > 5:
            variable_name = func_name[5:]
        elif func_name.startswith("find") and len(func_name) > 4:
            variable_name = func_name[4:]
        else:
            variable_name = "new_variable"
        script = utils.get_script(self._document)
        jedi_line, jedi_column = self._range.start.to_jedi()
        refactoring: Refactoring = script.extract_variable(
            jedi_line,
            jedi_column,
            new_name=variable_name,
        )
        changed_files = refactoring.get_changed_files()
        changes: dict[str, list[dict[str, Any]]] = {}
        for file, changed_file in changed_files.items():
            if file.as_uri() == self._document.uri:
                if self._document.uri not in changes:
                    changes[self._document.uri] = []
                new_source: str = changed_file.get_new_code()
                range_ = utils.get_text_range_between_sources(self._document.source, new_source, self._range.start.line)
                changes[self._document.uri].append({
                    "range": range_.to_range(),
                    "newText": range_.text,
                })

        workspace_edit = {"changes": changes}
        self._workspace.apply_edit(workspace_edit)

    def generate_code_actions(self) -> list[dict[str, Any]]:
        if self._range.start != self._range.end:
            return []
        if utils.is_a_return_statement(self._document, self._range.start.line):
            return []
        func_call = utils.find_function_call_at_line(self._document, self._range.start.line)
        if func_call is None:
            return []
        return [
            {
                "title": self.title,
                "kind": self.kind,
                "command": {
                    "command": self.command,
                    "arguments": [self._document.uri, func_call.to_range(), func_call.text],
                },
            },
        ]
