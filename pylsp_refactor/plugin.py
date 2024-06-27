import logging
from typing import Any

from pylsp import hookimpl
from pylsp.workspace import Document, Workspace

from pylsp_refactor import utils
from pylsp_refactor.actions import code_actions

logger = logging.getLogger(__name__)


@hookimpl
def pylsp_settings() -> dict[str, dict[str, dict[str, bool]]]:
    logger.info("Initializing pylsp_refactor")

    # Disable default plugins that conflicts with our plugin
    return {
        "plugins": {
            "pylsp_refactor": {"enabled": True},
        },
    }


@hookimpl
def pylsp_commands(config, workspace) -> list[str]:
    return code_actions.commands(config)


@hookimpl
def pylsp_code_actions(
    config: dict[str, Any],
    workspace: Workspace,
    document: Document,
    range: dict[str, Any],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)
    range_ = utils.parse_range(range)
    response = []
    response.extend(code_actions.collect_code_actions(config, workspace, document, range_))
    return response


@hookimpl
def pylsp_execute_command(
    config: dict[str, Any],
    workspace: Workspace,
    command: str,
    arguments: tuple[str, dict[str, Any], ...],
) -> None:
    logger.info("workspace/executeCommand: %s %s", command, arguments)
    if command in code_actions.commands(config):
        doc_uri = arguments[0]
        range = arguments[1]
        document: Document = workspace.get_document(doc_uri)
        range_ = utils.parse_range(range)
        code_actions.apply(config, workspace, document, range_, command, arguments)
