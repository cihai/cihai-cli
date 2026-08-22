# Contributing

Thanks for looking. Bug reports with a reproduction — the character or term
you looked up, the command, and what came back — are the most useful
contribution right now. cihai-cli's output currently travels over `logging`
rather than a dedicated stdout channel (see
[WRITING.md](WRITING.md#cli-help-text-and-error-messages)); giving it a
stable, scriptable contract is tracked in
[#341](https://github.com/cihai/cihai-cli/issues/341) and is a good place to
start a design discussion before writing code.

How this project writes prose — README, `CHANGES`, release notes, commit
messages, CLI help text, logging, docstrings, and source comments — is set
out separately in [WRITING.md](WRITING.md). Read that before changing any of
it. The constraints every change is held to, and the map of what is where,
are in [AGENTS.md](../AGENTS.md).

## Getting set up

```console
$ uv sync --all-extras --dev
```

This installs the `dev` dependency group: `cihai` and `PyYAML` (runtime),
`pytest` plus `pytest-rerunfailures`, `pytest-mock`, and `pytest-watcher`
(testing), `ruff` and `mypy` plus type stubs (lint), `coverage` and
`pytest-cov` (coverage), and the `gp-sphinx` documentation stack (docs).

## The gates

Format:

```console
$ uv run ruff format .
```

Lint:

```console
$ uv run ruff check . --fix --show-fixes
```

Type-check:

```console
$ uv run mypy .
```

Test:

```console
$ uv run pytest
```

Documentation is a gate, not a courtesy. Examples in docstrings and under
`src/cihai_cli/` and `docs/` are executed by `pytest`; the doctest flags live
in `pyproject.toml`, so there is no separate doctest step and a green
`pytest` is the proof. `README.md` is not part of that mechanism — see
[WRITING.md](WRITING.md#documented-examples-that-run). `docs/index.md` carries
a second, independent check: `tests/test_docs_examples.py` runs the literal
`cihai` commands shown there and compares the output.

CI (`.github/workflows/tests.yml`) runs `ruff check .`, `ruff format . --check`,
`mypy .`, and `pytest --cov=./ --cov-report=xml` on every push and pull
request, against Python 3.14. That is the order of record; every gate it runs
has to pass before a change is done.

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption. Fix a regression rather than disabling or
skipping its test.

### Imports and typing

- Standard library: namespace imports (`import pathlib`, not `from pathlib
  import Path`). Third-party packages may use `from x import Y`.
- Typing: `import typing as t`, access via `t.NamedTuple`, `t.Iterator`, and
  so on.
- Every file starts with `from __future__ import annotations` — `ruff`'s
  `isort` config (`required-imports`) enforces it.
- `mypy` runs with `strict = true` against `src/` and `tests/`
  (`[tool.mypy]` in `pyproject.toml`), targeting Python 3.10.

## Tests

The suite never downloads the live UNIHAN dataset. `tests/conftest.py`
builds a `Unihan.zip` from `tests/fixtures` for each test that needs one
(`zip_file`, `zip_path`, `unihan_options`), and points a fresh SQLite
database at `tmpdb_file`. Use those fixtures, plus `tmp_path` and
`monkeypatch`, rather than hand-rolled temp files or `unittest.mock` — prefer
real `cihai`/`unihan_etl` integration through the fixtures over mocking the
library.

`addopts` in `pyproject.toml` sets `--reruns=0`, so `pytest-rerunfailures` is
installed but inert by default; a flaky test is a bug, not a candidate for a
rerun flag.

Assert on log output through `caplog.records`, not `caplog.text` string
matching — see the testing-logs guidance in
[WRITING.md's Logging section](WRITING.md#logging).

Watch mode: `uv run ptw .` (`just start` runs the suite once, then watches).
`just watch-test` uses `entr(1)` instead, when installed.

## Documentation

```console
$ just build-docs
```

builds the Sphinx site (Furo-based, via `gp-sphinx`) to `docs/_build/html`.
`just start-docs` runs `sphinx-autobuild` with livereload; `just design-docs`
additionally watches static assets for CSS/JS work.

Nothing under `docs/` is generated output to avoid hand-editing, with one
exception: `docs/cli/*.md` and `docs/api.md` wrap `.. argparse::` and
`.. automodule::` directives, so the command reference itself comes from
`src/cihai_cli/cli.py` at build time — edit the source, not the rendered
argument tables (see
[Reference pages](WRITING.md#reference-pages)). A `{ref}` that does not
resolve fails the build; build the docs before committing a documentation
change.

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag pushes,
because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

Releases publish to PyPI via OIDC trusted publishing, triggered by a
`v<version>` git tag:

1. Update `CHANGES` with the release notes.
2. Bump the version in `src/cihai_cli/__about__.py`.
3. Commit as `Tag v<version>` and push.
4. The release owner creates and pushes the `v<version>` tag.
5. CI (`.github/workflows/tests.yml`, the `release` job) builds and publishes
   to PyPI automatically.

## Pull requests

One subject per pull request. Unrelated cleanup found along the way belongs
in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Update the documentation when a change affects the public interface — the
CLI's flags or output, configuration keys, or an exported Python symbol.

Commit format is in [WRITING.md](WRITING.md#commits). You may merge once you
have sign-off from one other developer; without merge permission, ask a
maintainer to merge for you.

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal
  attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always
  assume good intentions.
- Behaviour which can be reasonably considered harassment will not be tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. Report it through
GitHub's private vulnerability reporting on this repository's Security tab
(`https://github.com/cihai/cihai-cli/security/advisories/new`), which is
enabled for this repository.
