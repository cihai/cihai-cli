import pathlib

import pytest

import yaml
from click.testing import CliRunner

from cihai_cli import cli


def test_cli(test_config_file):
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    result = runner.invoke(cli.cli, "-c", test_config_file)
    result = runner.invoke(cli.cli, "info")
    assert result.exit_code == 2
    # result = runner.invoke(cli, ['info', '好'])
    # assert result.exit_code == 0


def test_cli_reflects_after_bootstrap(
    tmp_path: pathlib.Path, tmpdb_file, unihan_options
):
    config = {
        "database": {"url": f"sqlite:///{tmpdb_file}s"},
        "unihan_options": unihan_options,
    }
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        yaml.dump(config, default_flow_style=False), encoding="utf-8"
    )
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["-c", str(config_file), "info", "㐀"])
    assert "Bootstrapping Unihan database" in result.output
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ["-c", str(config_file)], "info")


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_cli_version(flag):
    runner = CliRunner()
    result = runner.invoke(cli.cli, [flag])
    assert "cihai-cli" in result.output
    assert "cihai" in result.output
    assert "unihan-etl" in result.output
