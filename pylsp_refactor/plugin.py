import logging
from typing import Any

from pylsp import hookimpl
from pylsp.config.config import Config
from pylsp.workspace import Document, Workspace

from pylsp_refactor import utils

logger = logging.getLogger(__name__)


@hookimpl
def pylsp_settings() -> dict[str, dict[str, dict[str, bool]]]:
    logger.info("Initializing pylsp_refactor")

    # Disable default plugins that conflicts with our plugin
    return {
        "plugins": {
            # "autopep8_format": {"enabled": False},
            # "definition": {"enabled": False},
            # "flake8_lint": {"enabled": False},
            # "folding": {"enabled": False},
            # "highlight": {"enabled": False},
            # "hover": {"enabled": False},
            # "jedi_completion": {"enabled": False},
            # "jedi_rename": {"enabled": False},
            # "mccabe_lint": {"enabled": False},
            # "preload_imports": {"enabled": False},
            # "pycodestyle_lint": {"enabled": False},
            # "pydocstyle_lint": {"enabled": False},
            # "pyflakes_lint": {"enabled": False},
            # "pylint_lint": {"enabled": False},
            # "references": {"enabled": False},
            # "rope_completion": {"enabled": False},
            # "rope_rename": {"enabled": False},
            # "signature": {"enabled": False},
            # "symbols": {"enabled": False},
            # "yapf_format": {"enabled": False},
            "pylsp_refactor": {"enabled": True},
        },
    }


@hookimpl
def pylsp_commands(config, workspace) -> list[str]:
    return [
        "pylsp_refactor.refactor.introduce.variable",
    ]


@hookimpl
def pylsp_code_actions(
    config: Config,
    workspace: Workspace,
    document: Document,
    range: dict[str, Any],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    logger.info("textDocument/codeAction: %s %s %s", document, range, context)
    start, end = utils.parse_range(range)
    if start != end:
        return []
    if utils.is_any_def(document, start.line):
        return []
    if utils.is_empty_line(document, start.line):
        return []
    return [
        {
            "title": "Introduce variable",
            "kind": "refactor.introduce",
            "command": {
                "command": "pylsp_refactor.refactor.introduce.variable",
                "arguments": [document.uri, range],
            },
        },
    ]


@hookimpl
def pylsp_execute_command(config: Config, workspace: Workspace, command, arguments):
    logger.info("workspace/executeCommand: %s %s", command, arguments)

    if command == "pylsp_refactor.refactor.introduce.variable":
        doc_uri, range = arguments
        document: Document = workspace.get_document(doc_uri)
        start, end = utils.parse_range(range)
        new_var_name = "new_variable"
        if start == end:
            word = utils.get_word_at_position(document, start)
            if word and utils.is_a_function_call(document, word):
                new_var_name = f"{word.text}_result"
        existing_text = utils.get_line_indented_range(document, start.line)
        new_text = f"{new_var_name} = {existing_text.text}"
        new_range = existing_text.to_range()
        workspace_edit = {
            "changes": {
                doc_uri: [
                    {
                        "range": new_range,
                        "newText": new_text,
                    },
                ],
            },
        }

        logger.info("applying workspace edit: %s %s", command, workspace_edit)
        workspace.apply_edit(workspace_edit)
