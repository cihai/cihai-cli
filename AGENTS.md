# AGENTS.md

Guidance for AI agents (Cursor, Claude Code, Copilot, etc.) working in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests must pass (unit, doctest, lint, type checks) before declaring work complete.
- Do not describe code as "working" if any test fails.
- Fix regressions rather than disabling or skipping tests unless explicitly approved.

## Project Overview

gp-libs is the shared tooling stack used across the git-pull ecosystem. This repository, `cihai-cli`, is a command-line interface built on top of the `cihai` library to explore the Unihan (CJK) character database. Key abilities:
- Lookup CJK characters with `cihai info <char>` and YAML-formatted output.
- Reverse search definitions with `cihai reverse <term>`.
- Bootstraps and queries the Unihan dataset via `cihai` / `unihan-etl`.
- Provides a small, typed argparse-based CLI (`src/cihai_cli/cli.py`) exposed as the `cihai` entry point.

## Development Environment

This project uses:
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency and task execution
- [ruff](https://github.com/astral-sh/ruff) for linting/formatting
- [mypy](https://github.com/python/mypy) with strict settings
- [pytest](https://docs.pytest.org/) (+ doctests) for testing
- [gp-libs](https://github.com/gp-libs/gp-libs) for shared docs/testing helpers
- Sphinx (Furo) for documentation

## Common Commands

### Setup
```bash
# Install dependencies (editable)
uv pip install --editable .
uv pip sync

# Install with dev extras
uv pip install --editable . -G dev
```

### Tests
```bash
just test           # or: uv run pytest
uv run pytest tests/test_cli.py           # single file
uv run pytest tests/test_cli.py::test_info_command  # single test

just start          # run tests then watch with pytest-watcher
uv run ptw .        # standalone watcher (doctests enabled by default)
```

### Linting & Types
```bash
just ruff           # uv run ruff check .
just ruff-format    # uv run ruff format .
uv run ruff check . --fix --show-fixes

just mypy           # strict type checking
```

### Documentation
```bash
just build-docs     # build Sphinx HTML in docs/_build
just start-docs     # autobuild + livereload
just design-docs    # update CSS/JS assets
```

### Workflow (recommended)
1) `uv run ruff format .`
2) `uv run pytest`
3) `uv run ruff check . --fix --show-fixes`
4) `uv run mypy`
5) `uv run pytest` (verify clean)

## Code Architecture (quick map)
- `src/cihai_cli/cli.py`: argparse entrypoint, implements `info` and `reverse` commands, logging setup.
- `src/cihai_cli/__about__.py`: package metadata (`__version__`).
- Tests: `tests/` (unit) plus doctests in `src/` and `docs/`.
- Docs: `docs/` Sphinx project (Furo theme).

## Testing Strategy
- Pytest with doctests enabled (`addopts` in `pyproject.toml`).
- Prefer real `cihai` / `unihan_etl` integration over heavy mocking; reuse fixtures where present.
- Watch mode: `uv run ptw .` (used in `just start`).
- Coverage via `pytest-cov`; configuration in `pyproject.toml`.
- Prefer fixtures over mocks (`server`, `session`, etc. when available); use `tmp_path` over `tempfile`, `monkeypatch` over `unittest.mock`.

## Coding Standards
- `from __future__ import annotations` required; enforced by ruff.
- Namespace imports for stdlib/typing (`import typing as t`); third-party packages may use `from X import Y`.
- Docstrings follow NumPy style (see `tool.ruff.lint.pydocstyle`).
- Python target version: 3.10 (`tool.ruff.target-version`).
- Keep CLI output human-friendly YAML; avoid breaking existing flags/args.
- Doctests: keep concise, narrative Examples blocks; move complex flows to `tests/examples/`.

## Logging Standards

These rules guide future logging changes; existing code may not yet conform.

### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `unihan_field` | `str` | UNIHAN field name |
| `unihan_source_file` | `str` | source data file path |
| `unihan_record_count` | `int` | records processed |
| `cihai_command` | `str` | CLI command name |

**Heavy/optional keys** (DEBUG only, potentially large):

| Key | Type | Context |
|-----|------|---------|
| `unihan_stdout` | `list[str]` | subprocess stdout lines (truncate or cap; `%(unihan_stdout)s` produces repr) |
| `unihan_stderr` | `list[str]` | subprocess stderr lines (same caveats) |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

### Key naming rules

- `snake_case`, not dotted; `unihan_` prefix
- Prefer stable scalars; avoid ad-hoc objects
- Heavy keys (`unihan_stdout`, `unihan_stderr`) are DEBUG-only; consider companion `unihan_stdout_len` fields or hard truncation (e.g. `stdout[:100]`)

### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

### LoggerAdapter for persistent context

For objects with stable identity (Dataset, Reader, Exporter), use `LoggerAdapter` to avoid repeating the same `extra` on every call. Lead with the portable pattern (override `process()` to merge); `merge_extra=True` simplifies this on Python 3.13+.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics, data I/O | Field parsing, record transformation steps |
| `INFO` | Data lifecycle, user-visible operations | Download completed, export finished, database bootstrapped |
| `WARNING` | Recoverable issues, deprecation, user-actionable config | Missing optional field, deprecated data format |
| `ERROR` | Failures that stop an operation | Download failed, parse error, database write failed |

Config discovery noise belongs in `DEBUG`; only surprising/user-actionable config issues → `WARNING`.

### Message style

- Lowercase, past tense for events: `"download completed"`, `"parse error"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="cihai_cli.cli")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "unihan_field")]`
- Assert on schema: `record.unihan_record_count == 100` not `"100 records" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

## Documentation Standards

### Code Blocks in Documentation

When writing documentation (README, CHANGES, docs/), follow these rules for code blocks:

**One command per code block.** This makes commands individually copyable. For sequential commands, either use separate code blocks or chain them with `&&` or `;` and `\` continuations (keeping it one logical command).

**Put explanations outside the code block**, not as comments inside.

Good:

Run the tests:

```console
$ uv run pytest
```

Run with coverage:

```console
$ uv run pytest --cov
```

Bad:

```console
# Run the tests
$ uv run pytest

# Run with coverage
$ uv run pytest --cov
```

### Shell Command Formatting

These rules apply to shell commands in documentation (README, CHANGES, docs/), **not** to Python doctests.

**Use `console` language tag with `$ ` prefix.** This distinguishes interactive commands from scripts and enables prompt-aware copy in many terminals.

Good:

```console
$ uv run pytest
```

Bad:

```bash
uv run pytest
```

**Split long commands with `\` for readability.** Each flag or flag+value pair gets its own continuation line, indented. Positional parameters go on the final line.

Good:

```console
$ pipx install \
    --suffix=@next \
    --pip-args '\--pre' \
    --force \
    'cihai-cli'
```

Bad:

```console
$ pipx install --suffix=@next --pip-args '\--pre' --force 'cihai-cli'
```

## Debugging Tips
- Lean on `pytest -k <pattern> -vv` for focused failures.
- For CLI behavior, run `uv run cihai info 好` or `uv run cihai reverse library`.
- If Unihan DB is missing, CLI bootstraps automatically; avoid altering that flow unless required.
- Stuck in loops? Pause, minimize to a minimal repro, document exact errors, and restate the hypothesis before another attempt.

## Git Commit Standards

Commit subjects: `Scope(type[detail]): concise description`

Body template:
```
why: Reason or impact.
what:
- Key technical changes
- Single topic only
```

Guidelines:
- Subject ≤50 chars; body lines ≤72 chars; imperative mood.
- One topic per commit; separate subject and body with a blank line.
- Mark breaking changes with `BREAKING:` and include related issue refs when relevant.

Common commit types:
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

## Notes & Docs Authoring
- For `notes/**/*.md`, keep content concise and well-structured (headings, bullets, code fences).
- Use clear link text `[Title](mdc:URL)` and avoid redundancy; follow llms.txt style when possible.

## References
- Project docs: https://cihai-cli.git-pull.com
- Library docs: https://cihai.git-pull.com
- Unihan dataset: https://www.unicode.org/charts/unihan.html
- Shared tooling: https://github.com/gp-libs/gp-libs
