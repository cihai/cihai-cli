import contextlib
import pathlib
import typing as t

import pytest
import yaml
from cihai_cli.cli import cli

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict as UnihanOptions


def test_cli(
    test_config_file: pathlib.Path,
    tmp_path: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
    monkeypatch: pytest.MonkeyPatch,
    tmpdb_file: pathlib.Path,
    unihan_options: "UnihanOptions",
) -> None:
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
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    flag: str,
) -> None:
    try:
        cli([flag])
    except SystemExit:
        result = capsys.readouterr()
        output = "".join(list(result.out))
        assert "cihai-cli" in output
        assert "cihai" in output
        assert "unihan-etl" in output
