## Developing

Clone the repository:

```shell
git clone https://github.com/venomlab/pylsp-refactor
```

Then inside the `pylsp-refactor` directory install deps and initialize dev env via `poetry`:

```shell
poetry install
```

### Enabling logging

To enable logging in pylsp:

```shell
pylsp -v --log-file /tmp/pylsp.log
```

### Enabling tcp mode

Normally, editors communicate with language servers through standard
input/output. Optionally, you can run pylsp in tcp mode if you want to be able
to use the standard input/output, for example so you can use IPython or pudb,
using the --tcp flag:

```shell
pylsp -v --log-file /tmp/pylsp.log --tcp --port 7090
```

Consult your lsp client documentation on how to connect to tcp-mode language
server, but if it doesn't support connecting to a language server via TCP, then
usually can configure `netcat`/`nc` to be your "language server" that will
proxy requests to a tcp-mode language server:

```shell
nc localhost 7090
```

### Testing

Run `pytest` to run plugin tests.
