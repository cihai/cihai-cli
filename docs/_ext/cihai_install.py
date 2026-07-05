"""Sphinx directive for the cihai-cli install widget."""

from __future__ import annotations

import html
import pathlib
import shutil
import typing as t
from dataclasses import dataclass

import markupsafe
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.docutils import SphinxDirective

if t.TYPE_CHECKING:
    import collections.abc as cabc

    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


@dataclass(frozen=True, slots=True)
class Method:
    """One installer tab."""

    id: str
    label: str
    doc_url: str


@dataclass(frozen=True, slots=True)
class Cooldown:
    """One cooldown mode."""

    id: str
    label: str


@dataclass(frozen=True, slots=True)
class Panel:
    """Rendered command cell for one installer and cooldown mode."""

    method: Method
    cooldown: Cooldown
    command: str
    check_command: str | None
    note: str | None
    is_default: bool


@dataclass(frozen=True, slots=True)
class UsagePanel:
    """Rendered command cell for one CLI invocation method."""

    method: Method
    cooldown: Cooldown
    commands: tuple[str, ...]
    note: str | None
    is_default: bool


METHODS: tuple[Method, ...] = (
    Method(
        id="uvx",
        label="uvx",
        doc_url="https://docs.astral.sh/uv/guides/tools/",
    ),
    Method(
        id="pipx",
        label="pipx",
        doc_url="https://pipx.pypa.io/stable/",
    ),
    Method(
        id="pip",
        label="pip",
        doc_url="https://pip.pypa.io/en/stable/",
    ),
)

COOLDOWNS: tuple[Cooldown, ...] = (
    Cooldown(id="off", label="Off"),
    Cooldown(id="days", label="Apply a cooldown"),
    Cooldown(id="bypass", label="Bypass global cooldown"),
)

DEFAULT_METHOD = "uvx"
DEFAULT_COOLDOWN_DAYS = 7
DEFAULT_COOLDOWN_TYPE = "days"
EXCLUDE_NEWER_PACKAGE_DATE = "2099-01-01"
EXCLUDE_NEWER_PACKAGES: tuple[str, ...] = (
    "cihai-cli",
    "cihai",
    "unihan-etl",
)
_DURATION_SENTINEL = "<COOLDOWN_DURATION>"
_USAGE_SUFFIXES: tuple[str, ...] = ("info 好", "reverse good", "--help")
_TAB_DEACTIVATE_RULE = (
    "html[data-cihai-install-method] .cihai-install__tab"
    '[aria-selected="true"]'
    "{color:var(--color-foreground-muted) !important;"
    "border-bottom-color:transparent !important;"
    "background:transparent !important}"
)
_TAB_ACTIVE_DECL = (
    "{color:var(--color-brand-primary) !important;"
    "border-bottom-color:var(--color-brand-primary) !important;"
    "background:var(--color-background-primary) !important}"
)
_PANEL_HIDE_RULE = (
    "html[data-cihai-install-method] .cihai-install__panel:not([hidden])"
    "{display:none !important}"
)
_PANEL_ACTIVE_DECL = "{display:block !important}"
_COOLDOWN_TOGGLE_RULES = (
    ".cihai-install__cooldown-toggle"
    "{appearance:none !important;"
    "-webkit-appearance:none !important;"
    "width:0.95em !important;"
    "height:0.95em !important;"
    "margin:0 !important;"
    "border:1.5px solid var(--color-foreground-muted) !important;"
    "border-radius:0.2em !important;"
    "background:var(--color-background-primary) !important;"
    "cursor:pointer !important;"
    "position:relative !important;"
    "flex:0 0 auto !important}"
    'html[data-cihai-install-cooldown-enabled="1"]'
    " .cihai-install__cooldown-toggle"
    "{background:var(--color-brand-primary) !important;"
    "border-color:var(--color-brand-primary) !important}"
    'html[data-cihai-install-cooldown-enabled="1"]'
    " .cihai-install__cooldown-toggle::after"
    '{content:"✓" !important;'
    "position:absolute !important;"
    "inset:0 !important;"
    "display:flex !important;"
    "align-items:center !important;"
    "justify-content:center !important;"
    "color:#fff !important;"
    "font-size:0.85em !important;"
    "font-weight:700 !important;"
    "line-height:1 !important}"
    ".cihai-install__cooldown-toggle:focus-visible"
    "{outline:2px solid var(--color-brand-primary) !important;"
    "outline-offset:2px !important}"
)


def _continued_command(parts: cabc.Sequence[str]) -> str:
    """Render one shell command with continuation lines."""
    if len(parts) == 1:
        return f"$ {parts[0]}"
    return "$ " + parts[0] + " \\\n" + " \\\n".join(f"    {part}" for part in parts[1:])


def _exclude_newer_package_args() -> tuple[str, ...]:
    """Return uv package exemption flags for cihai-cli's cooldown policy."""
    return tuple(
        f"--exclude-newer-package {package_name}={EXCLUDE_NEWER_PACKAGE_DATE}"
        for package_name in EXCLUDE_NEWER_PACKAGES
    )


def _command_for(method: Method, cooldown: Cooldown) -> str:
    """Return the command shown for a method and cooldown mode."""
    if method.id == "uvx":
        if cooldown.id == "days":
            return _continued_command(
                (
                    "uvx",
                    f"--exclude-newer {_DURATION_SENTINEL}",
                    *_exclude_newer_package_args(),
                    "--from cihai-cli",
                    "cihai --version",
                )
            )
        if cooldown.id == "bypass":
            return "$ uvx --no-config --from cihai-cli cihai --version"
        return "$ uvx --from cihai-cli cihai --version"
    if method.id == "pipx":
        return "$ pipx install cihai-cli"
    return "$ pip install --user --upgrade cihai-cli"


def _usage_command_for(method: Method, cooldown: Cooldown, suffix: str) -> str:
    """Return a full CLI invocation for a method and cooldown mode."""
    if method.id == "uvx":
        if cooldown.id == "days":
            return _continued_command(
                (
                    "uvx",
                    f"--exclude-newer {_DURATION_SENTINEL}",
                    *_exclude_newer_package_args(),
                    "--from cihai-cli",
                    f"cihai {suffix}",
                )
            )
        if cooldown.id == "bypass":
            return f"$ uvx --no-config --from cihai-cli cihai {suffix}"
        return f"$ uvx --from cihai-cli cihai {suffix}"
    if method.id == "pipx":
        return f"$ pipx run --spec cihai-cli cihai {suffix}"
    return f"$ cihai {suffix}"


def _check_command_for(method: Method) -> str | None:
    """Return a follow-up command after persistent installs."""
    if method.id == "uvx":
        return None
    return "$ cihai --version"


def _cooldown_note(method: Method, cooldown: Cooldown) -> str | None:
    """Return a caveat where a package manager cannot enforce this cooldown safely."""
    if method.id in {"pip", "pipx"} and cooldown.id in {"days", "bypass"}:
        return (
            "pip and pipx do not provide uv's per-package cooldown exemption. "
            "This command stays unchanged; use uvx when you need cooldown "
            "enforcement without filtering out cihai-cli itself."
        )
    return None


def _usage_note(method: Method, cooldown: Cooldown) -> str | None:
    """Return a caveat for usage cells where cooldowns cannot be expressed."""
    if method.id in {"pip", "pipx"} and cooldown.id in {"days", "bypass"}:
        return (
            "pip and pipx do not provide uv's per-package cooldown exemption. "
            "These invocations stay unchanged; use uvx when you need cooldown "
            "enforcement without filtering out cihai-cli itself."
        )
    if method.id == "pip":
        return "Install cihai-cli with pip first, then run the cihai command."
    return None


def build_panels() -> list[Panel]:
    """Return one panel for every installer and cooldown mode."""
    panels: list[Panel] = []
    for method_index, method in enumerate(METHODS):
        for cooldown_index, cooldown in enumerate(COOLDOWNS):
            panels.append(
                Panel(
                    method=method,
                    cooldown=cooldown,
                    command=_command_for(method, cooldown),
                    check_command=_check_command_for(method),
                    note=_cooldown_note(method, cooldown),
                    is_default=method_index == 0 and cooldown_index == 0,
                )
            )
    return panels


def build_usage_panels() -> list[UsagePanel]:
    """Return one usage panel for every invocation method and cooldown mode."""
    panels: list[UsagePanel] = []
    for method_index, method in enumerate(METHODS):
        for cooldown_index, cooldown in enumerate(COOLDOWNS):
            panels.append(
                UsagePanel(
                    method=method,
                    cooldown=cooldown,
                    commands=tuple(
                        _usage_command_for(method, cooldown, suffix)
                        for suffix in _USAGE_SUFFIXES
                    ),
                    note=_usage_note(method, cooldown),
                    is_default=method_index == 0 and cooldown_index == 0,
                )
            )
    return panels


def _highlight(
    env: BuildEnvironment, code: str, language: str = "console"
) -> markupsafe.Markup:
    """Return Sphinx-styled highlighted code for HTML builders."""
    builder = env.app.builder
    if isinstance(builder, StandaloneHTMLBuilder):
        inner = builder.highlighter.highlight_block(code, language)
        return markupsafe.Markup(
            f'<div class="highlight-{language} notranslate">{inner}</div>\n'
        )
    return markupsafe.Markup(f"<pre>{html.escape(code)}</pre>\n")


def _cooldown_days_slot(html_body: markupsafe.Markup) -> markupsafe.Markup:
    """Swap the cooldown duration sentinel for a JS-editable span."""
    slot = (
        '<span class="cihai-install__cooldown-days" '
        f"data-cooldown-duration-slot>P{DEFAULT_COOLDOWN_DAYS}D</span>"
    )
    return markupsafe.Markup(str(html_body).replace("&lt;COOLDOWN_DURATION&gt;", slot))


def _tab_active_selectors() -> str:
    """Return active-tab selectors keyed on prehydrated html state."""
    return ",".join(
        f'html[data-cihai-install-method="{method.id}"] '
        f'.cihai-install__tab[data-tab-value="{method.id}"]'
        for method in METHODS
    )


def _panel_active_selectors() -> str:
    """Return method x cooldown selectors keyed on prehydrated html state."""
    selectors: list[str] = []
    for method in METHODS:
        panel_base = (
            f' .cihai-install__panel[data-method="{method.id}"][data-cooldown="'
        )
        selectors.append(
            f'html[data-cihai-install-method="{method.id}"]'
            f'[data-cihai-install-cooldown-enabled="0"]'
            f'{panel_base}off"]'
        )
        selectors.append(
            f'html[data-cihai-install-method="{method.id}"]'
            f'[data-cihai-install-cooldown-enabled="1"]'
            f'[data-cihai-install-cooldown-type="days"]'
            f'{panel_base}days"]'
        )
        selectors.append(
            f'html[data-cihai-install-method="{method.id}"]'
            f'[data-cihai-install-cooldown-enabled="1"]'
            f'[data-cihai-install-cooldown-type="bypass"]'
            f'{panel_base}bypass"]'
        )
    return ",".join(selectors)


def _prehydrate_style() -> str:
    """Return CSS that paints saved widget state before runtime JS loads."""
    rules = [
        _TAB_DEACTIVATE_RULE,
        _tab_active_selectors() + _TAB_ACTIVE_DECL,
        _PANEL_HIDE_RULE,
        _panel_active_selectors() + _PANEL_ACTIVE_DECL,
        _COOLDOWN_TOGGLE_RULES,
    ]
    return "<style>@layer cihai-install-prehydrate{" + "".join(rules) + "}</style>"


def _prehydrate_script() -> str:
    """Return the head script that mirrors localStorage onto ``<html>``."""
    method_ids = "|".join(method.id for method in METHODS)
    return (
        '<script data-cfasync="false">(function(){'
        "try{"
        "var h=document.documentElement;"
        'var m=localStorage.getItem("cihai-cli.install.method")||"'
        + DEFAULT_METHOD
        + '";'
        "if(!/^(?:" + method_ids + ')$/.test(m))m="' + DEFAULT_METHOD + '";'
        'var ce=localStorage.getItem("cihai-cli.install.cooldown.enabled");'
        'ce=ce==="1"?"1":"0";'
        'var ct=localStorage.getItem("cihai-cli.install.cooldown.type")||"'
        + DEFAULT_COOLDOWN_TYPE
        + '";'
        'if(ct!=="bypass")ct="days";'
        'var cd=parseInt(localStorage.getItem("cihai-cli.install.cooldown.days"),10);'
        "if(isNaN(cd))cd=" + str(DEFAULT_COOLDOWN_DAYS) + ";"
        "if(cd<1)cd=1;"
        "if(cd>365)cd=365;"
        'h.setAttribute("data-cihai-install-method",m);'
        'h.setAttribute("data-cihai-install-cooldown-enabled",ce);'
        'h.setAttribute("data-cihai-install-cooldown-type",ct);'
        'h.setAttribute("data-cihai-install-cooldown-days",String(cd));'
        "}catch(_){}"
        "})();</script>"
    )


def prehydrate_snippet() -> str:
    """Return the head snippet that prevents saved-state widget flicker."""
    return _prehydrate_style() + _prehydrate_script()


def _render_command(env: BuildEnvironment, command: str) -> str:
    """Render a console command block with cooldown slots."""
    return str(_cooldown_days_slot(_highlight(env, command)))


def render_widget(env: BuildEnvironment, *, variant: str) -> str:
    """Render the install widget HTML."""
    panels = build_panels()
    method_tabs = "\n".join(
        (
            '<button type="button" class="cihai-install__tab" role="tab" '
            f'data-tab-value="{method.id}" '
            f'aria-selected="{str(method.id == DEFAULT_METHOD).lower()}" '
            f'tabindex="{0 if method.id == DEFAULT_METHOD else -1}">'
            f"{html.escape(method.label)}</button>"
        )
        for method in METHODS
    )
    panel_html = "\n".join(_render_panel(env, panel) for panel in panels)
    return f"""
<div class="cihai-install cihai-install--{html.escape(variant)}">
  <div class="cihai-install__tabs" role="tablist" aria-label="Installer">
    {method_tabs}
    <div class="cihai-install__cooldown-control">
      <input type="checkbox" class="cihai-install__cooldown-toggle"
             data-action="cooldown-toggle" aria-label="Apply a dependency cooldown">
      <button type="button" class="cihai-install__cooldown-label"
              data-action="cooldown-open">Configure cooldowns</button>
    </div>
  </div>
  <div class="cihai-install__body cihai-install__body--install">
    {panel_html}
  </div>
  {_render_settings_body()}
</div>
"""


def render_usage_widget(env: BuildEnvironment, *, variant: str) -> str:
    """Render the CLI usage widget HTML."""
    panels = build_usage_panels()
    method_tabs = "\n".join(
        (
            '<button type="button" class="cihai-install__tab" role="tab" '
            f'data-tab-value="{method.id}" '
            f'aria-selected="{str(method.id == DEFAULT_METHOD).lower()}" '
            f'tabindex="{0 if method.id == DEFAULT_METHOD else -1}">'
            f"{html.escape(method.label)}</button>"
        )
        for method in METHODS
    )
    panel_html = "\n".join(_render_usage_panel(env, panel) for panel in panels)
    return f"""
<div class="cihai-install cihai-usage cihai-install--{html.escape(variant)}">
  <div class="cihai-install__tabs" role="tablist" aria-label="Invocation method">
    {method_tabs}
    <div class="cihai-install__cooldown-control">
      <input type="checkbox" class="cihai-install__cooldown-toggle"
             data-action="cooldown-toggle" aria-label="Apply a dependency cooldown">
      <button type="button" class="cihai-install__cooldown-label"
              data-action="cooldown-open">Configure cooldowns</button>
    </div>
  </div>
  <div class="cihai-install__body cihai-install__body--install">
    {panel_html}
  </div>
  {_render_settings_body()}
</div>
"""


def _render_panel(env: BuildEnvironment, panel: Panel) -> str:
    """Render one installer panel."""
    hidden = "" if panel.is_default else " hidden"
    method_label = html.escape(panel.method.label)
    method_link = (
        f'<a href="{panel.method.doc_url}" target="_blank" rel="noopener">'
        f"{method_label}</a>"
    )
    check = ""
    if panel.check_command is not None:
        check = (
            '<p class="cihai-install__preamble">Then check the command:</p>'
            f"{_render_command(env, panel.check_command)}"
        )
    note = ""
    if panel.note is not None:
        note = f'<p class="cihai-install__cooldown-note">{html.escape(panel.note)}</p>'
    return f"""
<div class="cihai-install__panel" role="tabpanel"
     data-method="{panel.method.id}" data-cooldown="{panel.cooldown.id}"
     tabindex="0"{hidden}>
  <p class="cihai-install__preamble">
    With {method_link}:
  </p>
  {_render_command(env, panel.command)}
  {check}
  {note}
</div>
"""


def _render_usage_panel(env: BuildEnvironment, panel: UsagePanel) -> str:
    """Render one CLI usage panel."""
    hidden = "" if panel.is_default else " hidden"
    method_label = html.escape(panel.method.label)
    method_link = (
        f'<a href="{panel.method.doc_url}" target="_blank" rel="noopener">'
        f"{method_label}</a>"
    )
    commands = "\n".join(_render_command(env, command) for command in panel.commands)
    note = ""
    if panel.note is not None:
        note = f'<p class="cihai-install__cooldown-note">{html.escape(panel.note)}</p>'
    return f"""
<div class="cihai-install__panel" role="tabpanel"
     data-method="{panel.method.id}" data-cooldown="{panel.cooldown.id}"
     tabindex="0"{hidden}>
  <p class="cihai-install__preamble">
    Run cihai with {method_link}:
  </p>
  {commands}
  {note}
</div>
"""


def _render_settings_body() -> str:
    """Render the shared cooldown settings body."""
    return f"""
<div class="cihai-install__body cihai-install__body--settings"
     role="dialog" aria-label="Cooldown settings" hidden>
  <div class="cihai-install__settings-header">
    <button type="button" class="cihai-install__back" data-action="cooldown-back">
      Back
    </button>
    <h3 class="cihai-install__settings-title">Dependency cooldowns</h3>
  </div>
  <p class="cihai-install__settings-help">
    Cooldowns delay newly uploaded packages. uvx can apply one while exempting
    cihai-cli and the cihai runtime packages it needs.
  </p>
  <fieldset class="cihai-install__settings-modes">
    <legend class="cihai-install__sr-only">Cooldown type</legend>
    <label class="cihai-install__settings-mode">
      <input type="radio" name="cihai-install-cooldown-mode" value="days"
             data-action="cooldown-mode" checked>
      <span>
        Apply a cooldown of
        <input type="number" min="1" max="365"
               value="{DEFAULT_COOLDOWN_DAYS}"
               class="cihai-install__cooldown-days-input"
               data-action="cooldown-days"
               aria-label="Cooldown in days">
        days
      </span>
    </label>
    <label class="cihai-install__settings-mode">
      <input type="radio" name="cihai-install-cooldown-mode" value="bypass"
             data-action="cooldown-mode">
      <span>Bypass global uv cooldown configuration</span>
    </label>
  </fieldset>
</div>
"""


class CihaiInstallDirective(SphinxDirective):
    """Render the ``{cihai-install}`` directive."""

    has_content = False
    option_spec: t.ClassVar[dict[str, t.Callable[[str], t.Any]]] = {
        "variant": lambda arg: directives.choice(arg, ("full", "compact")),
    }
    default_options: t.ClassVar[dict[str, t.Any]] = {
        "variant": "full",
    }

    def run(self) -> list[nodes.Node]:
        """Render widget HTML into the doctree."""
        options = {**self.default_options, **self.options}
        rendered = render_widget(self.env, variant=t.cast(str, options["variant"]))
        return [nodes.raw("", rendered, format="html")]


class CihaiUsageDirective(SphinxDirective):
    """Render the ``{cihai-usage}`` directive."""

    has_content = False
    option_spec: t.ClassVar[dict[str, t.Callable[[str], t.Any]]] = {
        "variant": lambda arg: directives.choice(arg, ("full", "compact")),
    }
    default_options: t.ClassVar[dict[str, t.Any]] = {
        "variant": "full",
    }

    def run(self) -> list[nodes.Node]:
        """Render usage widget HTML into the doctree."""
        options = {**self.default_options, **self.options}
        rendered = render_usage_widget(
            self.env,
            variant=t.cast(str, options["variant"]),
        )
        return [nodes.raw("", rendered, format="html")]


def _copy_assets(app: Sphinx) -> None:
    """Copy widget CSS and JavaScript into the built ``_static`` directory."""
    src = pathlib.Path(app.srcdir) / "_widgets" / "cihai-install"
    dst = pathlib.Path(app.outdir) / "_static" / "widgets" / "cihai-install"
    dst.mkdir(parents=True, exist_ok=True)
    for filename in ("widget.css", "widget.js"):
        shutil.copy2(src / filename, dst / filename)


def inject_prehydrate(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, t.Any],
    doctree: object,
) -> None:
    """Inject the widget prehydrate snippet into the HTML ``<head>``."""
    context["metatags"] = context.get("metatags", "") + prehydrate_snippet()


def setup(app: Sphinx) -> dict[str, t.Any]:
    """Register the cihai install widget."""
    app.add_directive("cihai-install", CihaiInstallDirective)
    app.add_directive("cihai-usage", CihaiUsageDirective)
    app.add_css_file("widgets/cihai-install/widget.css")
    app.add_js_file("widgets/cihai-install/widget.js")
    app.connect("builder-inited", _copy_assets)
    app.connect("html-page-context", inject_prehydrate)
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
