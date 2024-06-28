import logging
from typing import Any, no_type_check

from pylsp import hookimpl
from pylsp.workspace import Document, Workspace

from pylsp_refactor import utils
from pylsp_refactor.actions import code_actions

logger = logging.getLogger(__name__)


@no_type_check
@hookimpl
def pylsp_settings() -> dict[str, dict[str, dict[str, bool]]]:
    logger.info("Initializing pylsp_refactor")

    # Disable default plugins that conflicts with our plugin
    return {
        "plugins": {
            "pylsp_refactor": {"enabled": True},
        },
    }


@no_type_check
@hookimpl
def pylsp_commands(
    config: Any,
    workspace: Workspace,  # noqa: ARG001
) -> list[str]:
    return code_actions.commands(config)


@no_type_check
@hookimpl
def pylsp_code_actions(
    config: Any,
    workspace: Workspace,
    document: Document,
    range: dict[str, Any],  # noqa: A002
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)
    range_ = utils.parse_range(range)
    response = []
    response.extend(code_actions.collect_code_actions(config, workspace, document, range_))
    return response


@no_type_check
@hookimpl
def pylsp_execute_command(
    config: Any,
    workspace: Workspace,
    command: str,
    arguments: tuple[str, dict[str, Any], ...],
) -> None:
    logger.info("workspace/executeCommand: %s %s", command, arguments)
    if command in code_actions.commands(config):
        doc_uri = arguments[0]
        input_range = arguments[1]
        document = workspace.get_document(doc_uri)
        range_ = utils.parse_range(input_range)
        code_actions.apply(config, workspace, document, range_, command, arguments)
