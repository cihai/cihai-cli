import pathlib

import pytest

import yaml

from cihai_cli.cli import cli


def test_cli(
    test_config_file: pathlib.Path,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.chdir(tmp_path)

    try:
        cli()
    except SystemExit:
        pass

    try:
        cli(["-c", test_config_file])
    except SystemExit:
        pass

    try:
        cli(["info"])
    except SystemExit:
        pass


def test_cli_reflects_after_bootstrap(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmpdb_file,
    unihan_options,
):
    config = {
        "database": {"url": f"sqlite:///{tmpdb_file}s"},
        "unihan_options": unihan_options,
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        yaml.dump(config, default_flow_style=False), encoding="utf-8"
    )

    try:
        cli(["-c", str(config_file), "info", "㐀"])
    except SystemExit:
        result = capsys.readouterr()
        output = "".join(list(result.out))
        assert "Bootstrapping Unihan database" in output

    try:
        cli(["-c", str(config_file), "info"])
    except SystemExit:
        result = capsys.readouterr()
        output = "".join(list(result.out))
        assert "Bootstrapping" in output


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_cli_version(
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    flag: str,
):
    try:
        result = cli([flag])
    except SystemExit:
        result = capsys.readouterr()
        output = "".join(list(result.out))
        assert "cihai-cli" in output
        assert "cihai" in output
        assert "unihan-etl" in output
