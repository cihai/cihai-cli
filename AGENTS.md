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

## Documentation Standards

### Code Blocks in Documentation

When writing documentation (README, CHANGES, docs/), follow these rules for code blocks:

**One command per code block.** This makes commands individually copyable.

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
