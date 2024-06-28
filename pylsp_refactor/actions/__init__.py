import typing
from typing import Any

from pylsp.workspace import Document, Workspace

from pylsp_refactor.utils import Range

from .base import CodeAction
from .introduce_variable_under_cursor import IntroduceVariableUnderCursor


class CodeActionsCollection:
    def __init__(self, code_actions: typing.Optional[typing.List[typing.Type[CodeAction]]] = None) -> None:
        if code_actions is None:
            code_actions = []
        self._code_actions = code_actions

    def register(self, action: typing.Type[CodeAction]) -> None:
        self._code_actions.append(action)

    def collect_code_actions(
        self,
        config: dict[str, Any],
        workspace: Workspace,
        document: Document,
        range_: Range,
    ) -> list[dict[str, Any]]:
        actions = []
        for ca_type in self._code_actions:
            ca = ca_type(config, workspace, document, range_)
            actions.extend(ca.generate_code_actions())
        return actions

    def commands(self, config: Any) -> list[str]:  # noqa: ARG002
        commands: set[str] = {ca_type.command for ca_type in self._code_actions}
        commands.update(ca_type.command for ca_type in self._code_actions)
        return sorted(commands)

    def apply(
        self,
        config: dict[str, Any],
        workspace: Workspace,
        document: Document,
        range_: Range,
        command: str,
        arguments: tuple[str, dict[str, int], Any],
    ) -> None:
        for ca_type in self._code_actions:
            if ca_type.command == command:
                ca = ca_type(config, workspace, document, range_)
                ca.apply(arguments)


code_actions = CodeActionsCollection()
code_actions.register(IntroduceVariableUnderCursor)
