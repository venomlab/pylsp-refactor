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
        range_: Range,
    ) -> None:
        self._config = config
        self._workspace = workspace
        self._document = document
        self._range = range_

    @abc.abstractmethod
    def generate_code_actions(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abc.abstractmethod
    def apply(self, arguments: tuple[str, dict[str, int], Any]) -> None:
        raise NotImplementedError
