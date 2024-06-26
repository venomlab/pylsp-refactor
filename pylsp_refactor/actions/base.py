import abc
from typing import Any

from pylsp.workspace import Document, Workspace

from pylsp_refactor.utils import Range


class CodeAction(abc.ABC):
    kind: str
    command: str
    title: str

    def __init__(
        self,
        config: dict[str, Any],
        workspace: Workspace,
        document: Document,
        range: Range,
    ) -> None:
        self._config = config
        self._workspace = workspace
        self._document = document
        self._range = range

    def generate_code_actions(self) -> list[dict[str, Any]]:
        if not self._should_propose_action():
            return []
        return [
            {
                "title": self.title,
                "kind": self.kind,
                "command": {
                    "command": self.command,
                    "arguments": [self._document.uri, self._range.to_range()],
                },
            },
        ]

    @abc.abstractmethod
    def apply(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _should_propose_action(self) -> bool:
        raise NotImplementedError
