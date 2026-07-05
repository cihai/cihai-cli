(architecture)=

# Architecture

cihai-cli is a thin command-line front end over {class}`cihai.core.Cihai`. Most
contributor work starts in {mod}`cihai_cli.cli`, then follows the command into
cihai's configuration, Unihan bootstrap, and query APIs.

## Runtime path

The entry point builds one parser with {func}`cihai_cli.cli.create_parser`.
That parser exposes {ref}`cihai info <cihai-info>` for direct character lookup
and {ref}`cihai reverse <cihai-reverse>` for definition search.

When a command runs, {func}`cihai_cli.cli.cli` loads configuration from
`--config` with {meth}`cihai.core.Cihai.from_file` or uses the default cihai
configuration. If the Unihan database is not bootstrapped, the CLI calls
cihai's {meth}`~cihai.core.Cihai.bootstrap` path with `unihan_options` from
configuration before running the query.

After bootstrap, {func}`cihai_cli.cli.command_info` calls
{meth}`cihai.data.unihan.dataset.Unihan.lookup_char` and
{func}`cihai_cli.cli.command_reverse` calls
{meth}`cihai.data.unihan.dataset.Unihan.reverse_char`. Both commands filter
output to human-facing fields unless `--all` asks for the full record.

## Documentation tests

The homepage examples are source-backed by `tests/test_docs_examples.py`. Those
tests build a temporary Unihan archive from `tests/fixtures`, run the documented
`cihai` commands against a temporary SQLite database, and compare the rendered
YAML block to real CLI output.

Use fixture-backed examples when a docs page promises command output. Console
blocks that install tools or show shell setup still build through Sphinx, but
they are not executable examples.
