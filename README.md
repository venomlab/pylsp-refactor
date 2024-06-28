# pylsp-refactor

Refactoring tools for Python LSP Server

This is a plugin for [Python LSP Server](https://github.com/python-lsp/python-lsp-server).

## Installation

To use this plugin, you need to install this plugin in the same virtualenv as python-lsp-server itself.

```bash
pip install pylsp-refactor
```

Then run `python-lsp-server` as usual, the plugin will be auto-discovered by
`python-lsp-server` if you've installed it to the right environment. Refer to
`python-lsp-server` and your IDE/text editor documentation on how to setup
`python-lsp-server`.

## Configuration

- `pylsp.plugins.pylsp_refactor.enabled` is `true` by default, you can change it to false to disable plugin completely

## Features

This plugin adds the following features to `pylsp`:

Code Action:

- introduce variable

## Usage

### Introduce variable

When CodeAction is triggered and the cursor is on a line where function call or class instantiation is presented.
Makes a new variable from a function call or class instantiation and tries to guess a name for it if possible.

Additionally, it moves newly created variable out of block if it's happening
somewhere inside dict initialization or class instantiation

## Developing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) from
[python-lsp/cookiecutter-pylsp-plugin](https://github.com/python-lsp/cookiecutter-pylsp-plugin)
project template.
