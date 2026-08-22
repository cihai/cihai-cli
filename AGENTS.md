# AGENTS.md

cihai-cli is the command-line front end for the
[cihai](https://cihai.git-pull.com) CJK-language library: `cihai info <char>`
and `cihai reverse <term>` query the UNIHAN character database and print a
YAML record.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/cihai_cli/cli.py` | argparse entry point: `create_parser`, `cli`, `command_info`, `command_reverse` |
| `src/cihai_cli/_formatter.py` | Colorized `--help` formatter (`CihaiHelpFormatter`, `HelpTheme`) |
| `src/cihai_cli/_colors.py` | `NO_COLOR`/`FORCE_COLOR`-aware ANSI styling (`Colors`, `style`) |
| `src/cihai_cli/__about__.py` | Package metadata, `__version__` |
| `tests/` | pytest suite: `test_cli.py`, `test_docs_examples.py`, `test_install_widget.py`, `fixtures/` |
| `docs/` | Sphinx site (`gp-sphinx`/Furo): quickstart, generated CLI reference, project pages |
| `CHANGES` | Changelog, rendered at `docs/history.md` |
| `MIGRATION` | Deprecation/upgrade notes, rendered at `docs/migration.md` |
| `justfile`, `docs/justfile` | Task runner: test, lint, and docs-build recipes |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, release notes, commit messages,
  docstrings, and source comments:
  [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a single-use
  helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry
  for every change to the public API, CLI, configuration, or output.
- A passing gate is evidence only once it has been shown capable of failing.
  Pair a new test with a deliberate break that proves it bites.

cihai-cli is a thin front end over the `cihai` library; UNIHAN data comes
through `cihai`'s `unihan_etl` dependency. On first use, `cihai` bootstraps
the UNIHAN dataset automatically (downloads and builds a local database) —
avoid altering that flow unless the change specifically targets it. The YAML
record from `info`/`reverse` and status messages like "No records found" are
emitted through `logging`, not `print`, and default to stderr; see
[WRITING.md's CLI section](.github/WRITING.md#cli-help-text-and-error-messages)
before changing what a command prints or how a test captures it.

## References

- Docs: <https://cihai-cli.git-pull.com>
- `cihai` library docs: <https://cihai.git-pull.com>
- UNIHAN dataset: <https://www.unicode.org/charts/unihan.html>
- Issues: <https://github.com/cihai/cihai-cli/issues>
