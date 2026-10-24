"""CLI tests for cihai-cli."""

from __future__ import annotations

import argparse
import contextlib
import sys
import typing as t

import pytest
import yaml

from cihai_cli._colors import ColorMode, Colors
from cihai_cli._formatter import create_formatter
from cihai_cli.cli import cli

if t.TYPE_CHECKING:
    import pathlib

    from cihai.types import UntypedDict as UnihanOptions


def test_cli(
    test_config_file: pathlib.Path,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test basic cihai usage."""
    monkeypatch.chdir(tmp_path)

    with contextlib.suppress(SystemExit):
        cli()

    with contextlib.suppress(SystemExit):
        cli(["-c", str(test_config_file)])

    with contextlib.suppress(SystemExit):
        cli(["info"])

    with contextlib.suppress(SystemExit):
        cli(["reverse"])


def test_cli_reflects_after_bootstrap(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmpdb_file: pathlib.Path,
    unihan_options: UnihanOptions,
) -> None:
    """High-level, integrative CLI-based test."""
    config = {
        "database": {"url": f"sqlite:///{tmpdb_file}s"},
        "unihan_options": {
            "source": str(unihan_options["source"]),
            "work_dir": str(unihan_options["work_dir"]),
            "zip_path": str(unihan_options["zip_path"]),
        },
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        yaml.dump(config, default_flow_style=False),
        encoding="utf-8",
    )

    try:
        cli(["-c", str(config_file), "info", "㐀"])
    except SystemExit:
        output = "".join(list(caplog.messages) + list(capsys.readouterr().out))
        assert "Bootstrapping Unihan database" in output

    caplog.clear()

    try:
        cli(["-c", str(config_file), "info"])
    except SystemExit:
        output = "".join(list(capsys.readouterr().err))
        assert "cihai info" in output


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_cli_version(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    flag: str,
) -> None:
    """Returns cihai-cli version."""
    try:
        cli([flag])
    except SystemExit:
        output = "".join(list(caplog.messages) + list(capsys.readouterr().out))
        assert "cihai-cli" in output
        assert "cihai" in output
        assert "unihan-etl" in output


def test_cli_help_contains_examples(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify main help output includes example commands."""
    with contextlib.suppress(SystemExit):
        cli(["--help"])

    output = capsys.readouterr().out
    assert "info examples:" in output
    assert "cihai info 好" in output
    assert "reverse examples:" in output
    assert "cihai reverse" in output


def test_cli_info_help_contains_examples(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify info subcommand help includes example commands."""
    with contextlib.suppress(SystemExit):
        cli(["info", "--help"])

    output = capsys.readouterr().out
    assert "examples:" in output
    assert "cihai info 好" in output
    assert "cihai info --all" in output


def test_cli_reverse_help_contains_examples(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify reverse subcommand help includes example commands."""
    with contextlib.suppress(SystemExit):
        cli(["reverse", "--help"])

    output = capsys.readouterr().out
    assert "examples:" in output
    assert "cihai reverse" in output


def test_help_example_color_follows_argparse(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """From Python 3.14 argparse decides example color; below, cihai's theme.

    argparse 3.14+ colors help itself, so examples share its on/off decision
    and palette with the usage line. The bound theme asks for color here and
    ``NO_COLOR`` refuses it, so the examples show which side decided.
    """
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    formatter_class = create_formatter(Colors(ColorMode.ALWAYS))
    monkeypatch.setenv("NO_COLOR", "1")
    parser = argparse.ArgumentParser(
        prog="cihai",
        description="info examples:\n  cihai info 好",
        formatter_class=formatter_class,
    )

    example = next(line for line in parser.format_help().splitlines() if "好" in line)

    assert ("\033[" in example) is (sys.version_info < (3, 14))
