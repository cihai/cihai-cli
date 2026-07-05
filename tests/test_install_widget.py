"""Tests for the documentation CLI widgets."""

from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import typing as t

import pytest

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]


class WidgetCase(t.NamedTuple):
    """CLI widget test case."""

    test_id: str
    method_id: str
    cooldown_id: str


def _load_widget_module() -> t.Any:
    module_path = pathlib.Path("docs/_ext/cihai_install.py")
    spec = importlib.util.spec_from_file_location("cihai_install", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_uvx_cooldown_exemptions_are_runtime_packages_only() -> None:
    """Keep widget cooldown exemptions scoped to user-facing CLI runtime."""
    widget = _load_widget_module()
    pyproject = tomllib.loads(
        pathlib.Path("pyproject.toml").read_text(encoding="utf-8")
    )
    repo_policy_packages = set(pyproject["tool"]["uv"]["exclude-newer-package"])
    docs_only_packages = {
        package_name
        for package_name in repo_policy_packages
        if package_name == "gp-libs"
        or package_name.startswith("gp-")
        or package_name.startswith("sphinx")
    }

    assert widget.EXCLUDE_NEWER_PACKAGES == ("cihai-cli", "cihai", "unihan-etl")
    assert docs_only_packages.isdisjoint(widget.EXCLUDE_NEWER_PACKAGES)


def test_install_widget_panel_matrix() -> None:
    """Render one panel for every install method and cooldown mode."""
    widget = _load_widget_module()
    panels = widget.build_panels()

    assert len(panels) == len(widget.METHODS) * len(widget.COOLDOWNS)
    assert {(panel.method.id, panel.cooldown.id) for panel in panels} == {
        (method.id, cooldown.id)
        for method in widget.METHODS
        for cooldown in widget.COOLDOWNS
    }
    assert [panel.method.id for panel in panels if panel.is_default] == ["uvx"]
    assert [panel.cooldown.id for panel in panels if panel.is_default] == ["off"]


def test_usage_widget_panel_matrix() -> None:
    """Render one usage panel for every invocation method and cooldown mode."""
    widget = _load_widget_module()
    panels = widget.build_usage_panels()

    assert len(panels) == len(widget.METHODS) * len(widget.COOLDOWNS)
    assert {(panel.method.id, panel.cooldown.id) for panel in panels} == {
        (method.id, cooldown.id)
        for method in widget.METHODS
        for cooldown in widget.COOLDOWNS
    }
    assert [panel.method.id for panel in panels if panel.is_default] == ["uvx"]
    assert [panel.cooldown.id for panel in panels if panel.is_default] == ["off"]


def test_usage_widget_shows_cli_examples() -> None:
    """The usage widget demonstrates real cihai command invocations."""
    widget = _load_widget_module()
    panel = next(
        item
        for item in widget.build_usage_panels()
        if item.method.id == "uvx" and item.cooldown.id == "off"
    )

    assert "$ uvx --from cihai-cli cihai info 好" in panel.commands
    assert "$ uvx --from cihai-cli cihai reverse good" in panel.commands
    assert "$ uvx --from cihai-cli cihai --help" in panel.commands


@pytest.mark.parametrize(
    "case",
    (
        WidgetCase(test_id="pipx-days", method_id="pipx", cooldown_id="days"),
        WidgetCase(test_id="pipx-bypass", method_id="pipx", cooldown_id="bypass"),
        WidgetCase(test_id="pip-days", method_id="pip", cooldown_id="days"),
        WidgetCase(test_id="pip-bypass", method_id="pip", cooldown_id="bypass"),
    ),
    ids=lambda case: case.test_id,
)
def test_pip_backends_fall_back_when_cooldowns_need_package_exemptions(
    case: WidgetCase,
) -> None:
    """Pip and pipx panels do not pretend to have uv-style exemptions."""
    widget = _load_widget_module()
    panels = widget.build_panels()
    panel = next(
        item
        for item in panels
        if item.method.id == case.method_id and item.cooldown.id == case.cooldown_id
    )
    off_panel = next(
        item
        for item in panels
        if item.method.id == case.method_id and item.cooldown.id == "off"
    )

    assert panel.command == off_panel.command
    assert panel.note is not None
    assert "uvx" in panel.note
    assert "--uploaded-prior-to" not in panel.command
    assert "<COOLDOWN_DURATION>" not in panel.command


def test_uvx_days_command_carries_all_cooldown_exemptions() -> None:
    """The uvx days command exempts cihai-cli and git-pull packages."""
    widget = _load_widget_module()
    panel = next(
        item
        for item in widget.build_panels()
        if item.method.id == "uvx" and item.cooldown.id == "days"
    )

    assert "--exclude-newer <COOLDOWN_DURATION>" in panel.command
    for package_name in widget.EXCLUDE_NEWER_PACKAGES:
        assert f"--exclude-newer-package {package_name}=2099-01-01" in panel.command


def test_usage_uvx_days_commands_carry_all_cooldown_exemptions() -> None:
    """Every uvx usage command keeps cooldown package exemptions."""
    widget = _load_widget_module()
    panel = next(
        item
        for item in widget.build_usage_panels()
        if item.method.id == "uvx" and item.cooldown.id == "days"
    )

    for command in panel.commands:
        assert "--exclude-newer <COOLDOWN_DURATION>" in command
        for package_name in widget.EXCLUDE_NEWER_PACKAGES:
            assert f"--exclude-newer-package {package_name}=2099-01-01" in command


def test_prehydrate_snippet_restores_saved_widget_state() -> None:
    """The head snippet restores localStorage state before widget JS loads."""
    widget = _load_widget_module()
    snippet = widget.prehydrate_snippet()

    assert "cihai-cli.install.method" in snippet
    assert "data-cihai-install-method" in snippet
    assert "data-cihai-install-cooldown-enabled" in snippet
    assert "data-cihai-install-cooldown-type" in snippet
    assert "data-cihai-install-cooldown-days" in snippet
    assert "@layer cihai-install-prehydrate" in snippet
    assert 'data-method="pipx"' in snippet
    assert 'data-cooldown="days"' in snippet


@pytest.fixture(scope="session")
def built_docs(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Build docs once for install-widget smoke tests."""
    output = tmp_path_factory.mktemp("install-widget-docs")
    _ = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "dirhtml",
            "-q",
            "docs",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return output


def test_install_widget_renders_in_built_docs(built_docs: pathlib.Path) -> None:
    """The homepage renders usage first and copies widget assets."""
    index = (built_docs / "index.html").read_text(encoding="utf-8")
    quickstart = (built_docs / "quickstart" / "index.html").read_text(encoding="utf-8")

    assert "cihai-usage" in index
    assert "cihai-install" in quickstart
    assert index.index("cihai-usage") < index.index("At a glance")
    assert 'data-tab-value="uvx"' in index
    assert "cihai info" in index
    assert "cihai reverse" in index
    assert "--exclude-newer-package" in index
    assert "data-cooldown-duration-slot" in index
    assert "cihai-cli.install.method" in index
    assert "@layer cihai-install-prehydrate" in index
    assert (
        built_docs / "_static" / "widgets" / "cihai-install" / "widget.css"
    ).is_file()
    assert (
        built_docs / "_static" / "widgets" / "cihai-install" / "widget.js"
    ).is_file()
