from typing import Any

from pylsp_refactor import utils

from .base import CodeAction


class IntroduceVariableUnderCursor(CodeAction):
    title = "Introduce variable"
    kind = "refactor.introduce"
    command = "pylsp_refactor.refactor.introduce_variable_under_cursor"

    def apply(self, arguments: tuple[str, dict[str, int], Any]) -> None:
        callee_name, callee_type = arguments[2]
        callee_name_snake = utils.camel_to_snake(callee_name)
        if callee_type == "class":
            variable_name = callee_name_snake
            if variable_name == callee_name:
                variable_name += "_obj"
        elif callee_name_snake.startswith("get_") and len(callee_name) > 4:
            variable_name = callee_name[4:]
        elif callee_name_snake.startswith("find_") and len(callee_name) > 5:
            variable_name = callee_name[5:]
        else:
            variable_name = "new_variable"
        script = utils.get_script(self._document)
        jedi_line, jedi_column = self._range.start.to_jedi()
        refactoring = script.extract_variable(
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
        obj_call = utils.find_call_at_line(self._document, self._range.start.line)
        if obj_call is None:
            return []
        return [
            {
                "title": self.title,
                "kind": self.kind,
                "command": {
                    "command": self.command,
                    "arguments": [
                        self._document.uri,
                        obj_call.to_range(),
                        (
                            obj_call.name,
                            obj_call.type_,
                        ),
                    ],
                },
            },
        ]
