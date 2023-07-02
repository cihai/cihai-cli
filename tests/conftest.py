"""Pytest configuration."""

import pathlib
import typing as t
import zipfile

import pytest
import yaml

from cihai.data.unihan.constants import UNIHAN_FILES

if t.TYPE_CHECKING:
    from cihai.types import UntypedDict


@pytest.fixture(scope="session")
def project_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope="session")
def cache_path(project_path: pathlib.Path) -> pathlib.Path:
    return project_path / ".cihai_cache"


@pytest.fixture(scope="session", autouse=True)
def ensure_cache_path(cache_path: pathlib.Path) -> None:
    cache_path.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def tests_path(project_path: pathlib.Path) -> pathlib.Path:
    return project_path / "tests"


@pytest.fixture(scope="session")
def fixture_path(tests_path: pathlib.Path) -> pathlib.Path:
    """Return tests/fixtures/ directory."""
    return tests_path / "fixtures"


@pytest.fixture(scope="session")
def test_config_file_path(fixture_path: pathlib.Path) -> pathlib.Path:
    return fixture_path / "test_config.yml"


@pytest.fixture(scope="session")
def test_config_file(
    test_config_file_path: pathlib.Path,
    unihan_options: "UntypedDict",
) -> pathlib.Path:
    with test_config_file_path.open("w") as file:
        config = yaml.dump(
            {
                "database": {"url": "sqlite:///:memory:"},
                "unihan_options": {
                    "source": str(unihan_options["source"]),
                    "work_dir": str(unihan_options["work_dir"]),
                    "zip_path": str(unihan_options["zip_path"]),
                },
            },
            Dumper=yaml.SafeDumper,
            indent=True,
            default_flow_style=False,
            allow_unicode=True,
        )
        file.write(config)
    return test_config_file_path


@pytest.fixture(scope="session")
def zip_path(cache_path: pathlib.Path) -> pathlib.Path:
    return cache_path / "Unihan.zip"


@pytest.fixture(scope="session")
def zip_file(zip_path: pathlib.Path, fixture_path: pathlib.Path) -> zipfile.ZipFile:
    """Create and return ZipFile."""
    _files = []
    for f in UNIHAN_FILES:
        _files += [fixture_path / f]
    zf = zipfile.ZipFile(zip_path, "a")
    for _f in _files:
        if _f.name not in zf.namelist():
            zf.write(_f, _f.name)
    zf.close()
    return zf


@pytest.fixture(scope="session")
def unihan_options(
    zip_file: zipfile.ZipFile,
    zip_path: pathlib.Path,
    cache_path: pathlib.Path,
) -> "UntypedDict":
    return {
        "source": zip_path,
        "work_dir": cache_path,
        "zip_path": cache_path / "downloads" / "Moo.zip",
    }


@pytest.fixture()
def tmpdb_file(tmpdir: pathlib.Path) -> pathlib.Path:
    """Return test SQLite database."""
    return tmpdir / "test.db"
