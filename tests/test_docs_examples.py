"""Documentation example tests."""

from __future__ import annotations

import contextlib
import logging
import pathlib
import shlex
import typing as t

import pytest
import yaml

from cihai_cli.cli import cli

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict as UnihanOptions


class DocsCommandCase(t.NamedTuple):
    """Documentation command test case."""

    test_id: str
    page: pathlib.Path
    command: str


DOCS_COMMAND_CASES = (
    DocsCommandCase(
        test_id="homepage-info",
        page=pathlib.Path("docs/index.md"),
        command="cihai info 好",
    ),
    DocsCommandCase(
        test_id="homepage-reverse",
        page=pathlib.Path("docs/index.md"),
        command="cihai reverse good",
    ),
)


def _write_config_file(
    tmp_path: pathlib.Path,
    tmpdb_file: pathlib.Path,
    unihan_options: UnihanOptions,
) -> pathlib.Path:
    config = {
        "database": {"url": f"sqlite:///{tmpdb_file}"},
        "unihan_options": {
            "source": str(unihan_options["source"]),
            "work_dir": str(unihan_options["work_dir"]),
            "zip_path": str(unihan_options["zip_path"]),
        },
    }
    config_file = tmp_path / "cihai-docs.yml"
    config_file.write_text(
        yaml.dump(config, default_flow_style=False),
        encoding="utf-8",
    )
    return config_file


def _extract_expected_output(case: DocsCommandCase) -> str:
    lines = case.page.read_text(encoding="utf-8").splitlines()
    command_line = f"$ {case.command}"
    try:
        command_index = lines.index(command_line)
    except ValueError as exc:
        msg = f"{command_line!r} is missing from {case.page}"
        raise AssertionError(msg) from exc

    fence_indices = [
        index
        for index in range(command_index + 1, len(lines))
        if lines[index].startswith("```")
    ]
    if len(fence_indices) < 2:
        msg = f"{case.command!r} in {case.page} needs a following output block"
        raise AssertionError(msg)

    start, end = fence_indices[0], fence_indices[1]
    return "\n".join(lines[start + 1 : end]).strip()


@pytest.mark.parametrize(
    "case",
    DOCS_COMMAND_CASES,
    ids=[case.test_id for case in DOCS_COMMAND_CASES],
)
def test_homepage_console_examples_match_cli_output(
    case: DocsCommandCase,
    tmp_path: pathlib.Path,
    tmpdb_file: pathlib.Path,
    unihan_options: UnihanOptions,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify docs/index.md console examples match real CLI output."""
    command_parts = shlex.split(case.command)
    assert command_parts[0] == "cihai"
    config_file = _write_config_file(
        tmp_path=tmp_path,
        tmpdb_file=tmpdb_file,
        unihan_options=unihan_options,
    )

    with caplog.at_level(logging.INFO), contextlib.suppress(SystemExit):
        cli(["-c", str(config_file), *command_parts[1:]])

    assert _extract_expected_output(case) in "\n".join(caplog.messages)


def test_quickstart_trunk_pipx_installs_cli_repo() -> None:
    """Keep the trunk pipx example pointed at cihai-cli."""
    quickstart = pathlib.Path("docs/quickstart.md").read_text(encoding="utf-8")

    assert "cihai-cli @ git+https://github.com/cihai/cihai-cli.git@master" in quickstart
    assert "cihai-cli @ git+https://github.com/cihai/cihai.git@master" not in quickstart


def test_sphinx_doctest_builder_is_enabled() -> None:
    """Keep the docs/justfile doctest recipe executable."""
    conf = pathlib.Path("docs/conf.py").read_text(encoding="utf-8")

    assert '"sphinx.ext.doctest"' in conf
