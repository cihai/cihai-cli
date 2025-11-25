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
make test           # or: uv run pytest
uv run pytest tests/test_cli.py           # single file
uv run pytest tests/test_cli.py::test_info_command  # single test

make start          # run tests then watch with pytest-watcher
uv run ptw .        # standalone watcher (doctests enabled by default)
```

### Linting & Types
```bash
make ruff           # uv run ruff check .
make ruff_format    # uv run ruff format .
uv run ruff check . --fix --show-fixes

make mypy           # strict type checking
```

### Documentation
```bash
make build_docs     # build Sphinx HTML in docs/_build
make start_docs     # autobuild + livereload
make design_docs    # update CSS/JS assets
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
- Watch mode: `uv run ptw .` (used in `make start`).
- Coverage via `pytest-cov`; configuration in `pyproject.toml`.
- Prefer fixtures over mocks (`server`, `session`, etc. when available); use `tmp_path` over `tempfile`, `monkeypatch` over `unittest.mock`.

## Coding Standards
- `from __future__ import annotations` required; enforced by ruff.
- Namespace imports for stdlib/typing (`import typing as t`).
- Docstrings follow NumPy style (see `tool.ruff.lint.pydocstyle`).
- Python target version: 3.10 (`tool.ruff.target-version`).
- Keep CLI output human-friendly YAML; avoid breaking existing flags/args.
- Doctests: keep concise, narrative Examples blocks; move complex flows to `tests/examples/`.

## Debugging Tips
- Lean on `pytest -k <pattern> -vv` for focused failures.
- For CLI behavior, run `uv run cihai info 好` or `uv run cihai reverse library`.
- If Unihan DB is missing, CLI bootstraps automatically; avoid altering that flow unless required.
- Stuck in loops? Pause, minimize to a minimal repro, document exact errors, and restate the hypothesis before another attempt.

## Commit Standards
- Format: `Component/File(commit-type[scope]): short imperative subject`.
- Body: `why:` and `what:` bullet list; keep lines ≤72 chars, one topic per commit.
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `py(deps)` / `py(deps[dev])`.
- Mark breaking changes with `BREAKING:` and include related issue refs when relevant.

## Notes & Docs Authoring
- For `notes/**/*.md`, keep content concise and well-structured (headings, bullets, code fences).
- Use clear link text `[Title](mdc:URL)` and avoid redundancy; follow llms.txt style when possible.

## References
- Project docs: https://cihai-cli.git-pull.com
- Library docs: https://cihai.git-pull.com
- Unihan dataset: https://www.unicode.org/charts/unihan.html
- Shared tooling: https://github.com/gp-libs/gp-libs
