from unittest.mock import ANY

from pylsp_refactor import plugin


def test_code_action_on_b64encode(config, workspace, document, code_action_context):
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
                "command": "pylsp_refactor.refactor.introduce_variable_under_cursor",
                "arguments": [document.uri, ANY, ("b64encode", "function")],
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
                                "start": {"line": 6, "character": 0},
                                "end": {"line": 6, "character": 27},
                            },
                            "newText": '    new_variable = base64.b64encode("asd")',
                        },
                    ],
                },
            },
        },
    )


def test_code_action_on_get_foo(config, workspace, document, code_action_context):
    selection = {
        "start": {
            "line": 7,
            "character": 5,
        },
        "end": {
            "line": 7,
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
                "command": "pylsp_refactor.refactor.introduce_variable_under_cursor",
                "arguments": [document.uri, ANY, ("get_foo", "function")],
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
                                "start": {"line": 7, "character": 0},
                                "end": {"line": 7, "character": 13},
                            },
                            "newText": "    foo = get_foo()",
                        },
                    ],
                },
            },
        },
    )


def test_code_action_on_dict_return_get_foo(config, workspace, document, code_action_context):
    selection = {
        "start": {
            "line": 11,
            "character": 5,
        },
        "end": {
            "line": 11,
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
                "command": "pylsp_refactor.refactor.introduce_variable_under_cursor",
                "arguments": [document.uri, ANY, ("get_foo", "function")],
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
                                "start": {"line": 10, "character": 0},
                                "end": {"line": 11, "character": 25},
                            },
                            "newText": '    foo = get_foo()\n    return {\n        "asd": foo,',
                        },
                    ],
                },
            },
        },
    )


def test_code_action_on_class_construct(config, workspace, document, code_action_context):
    selection = {
        "start": {
            "line": 18,
            "character": 5,
        },
        "end": {
            "line": 18,
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
                "command": "pylsp_refactor.refactor.introduce_variable_under_cursor",
                "arguments": [document.uri, ANY, ("FooBar", "class")],
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
                                "start": {"line": 18, "character": 0},
                                "end": {"line": 18, "character": 12},
                            },
                            "newText": "    foo_bar = FooBar()",
                        },
                    ],
                },
            },
        },
    )
