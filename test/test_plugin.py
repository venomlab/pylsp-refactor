from unittest.mock import ANY

from pylsp_refactor import plugin
from test.conftest import *


def test_code_action(config, workspace, document, code_action_context):
    selection = {
        "start": {
            "line": 6,
            "character": 5,
        },
        "end": {
            "line": 6,
            "character": 5,
        },
    }

    response = plugin.pylsp_code_actions(
        config=config,
        workspace=workspace,
        document=document,
        range=selection,
        context=code_action_context,
    )

    expected = [
        {
            "title": "Introduce variable",
            "kind": "refactor.introduce",
            "command": {
                "command": "pylsp_refactor.refactor.introduce.variable",
                "arguments": [document.uri, selection],
            },
        },
    ]

    assert response == expected

    command = response[0]["command"]["command"]
    arguments = response[0]["command"]["arguments"]

    response = plugin.pylsp_execute_command(
        config=config,
        workspace=workspace,
        command=command,
        arguments=arguments,
    )

    workspace._endpoint.request.assert_called_once_with(
        "workspace/applyEdit",
        {
            "edit": {
                "changes": {
                    document.uri: [
                        {
                            "range": {
                                "start": {"line": 6, "character": 4},
                                "end": {"line": 6, "character": 9},
                            },
                            "newText": "foo_result = foo()",
                        },
                    ],
                },
            },
        },
    )
