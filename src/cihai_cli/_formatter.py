"""Argparse help formatter with colored examples."""

from __future__ import annotations

import argparse
import re
import typing as t

if t.TYPE_CHECKING:
    from ._colors import Colors


class HelpTheme(t.NamedTuple):
    """Color codes for help text elements.

    Stores raw ANSI escape sequences for each element type to avoid
    repeated string formatting during help text generation.
    """

    prog: str
    """Program name color (magenta + bold)."""
    action: str
    """Subcommand/action color (cyan)."""
    long_option: str
    """Long option color, e.g. --all (green)."""
    short_option: str
    """Short option color, e.g. -a (green)."""
    label: str
    """Value/label color (yellow)."""
    heading: str
    """Section heading color (blue)."""
    reset: str
    """ANSI reset code."""

    @classmethod
    def default(cls) -> HelpTheme:
        """Create the default color theme.

        Returns
        -------
        HelpTheme
            Theme with standard terminal colors.
        """
        return cls(
            prog="\033[35;1m",  # magenta + bold
            action="\033[36m",  # cyan
            long_option="\033[32m",  # green
            short_option="\033[32m",  # green
            label="\033[33m",  # yellow
            heading="\033[34m",  # blue
            reset="\033[0m",
        )


class CihaiHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Help formatter that colorizes example sections.

    Extends RawDescriptionHelpFormatter to detect example blocks and apply
    syntax highlighting to command tokens. When no theme is set, behaves
    identically to the parent class.

    The formatter detects lines ending with "examples:" as section headings,
    and lines starting with "cihai " as example commands to colorize.
    """

    _theme: HelpTheme | None = None

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        """Format description text, colorizing example sections if theme is set.

        Parameters
        ----------
        text : str
            The text to format.
        width : int
            Maximum line width.
        indent : str
            Indentation prefix for each line.

        Returns
        -------
        str
            Formatted text with colorized examples if theme is enabled.
        """
        theme = self._theme
        if not text or theme is None:
            return super()._fill_text(text, width, indent)

        lines: list[str] = []
        in_examples = False

        for line in text.splitlines(keepends=True):
            stripped = line.strip()
            lower = stripped.lower()

            if lower.endswith("examples:"):
                # Start of examples section
                in_examples = True
                lines.append(f"{indent}{theme.heading}{stripped}{theme.reset}\n")
            elif in_examples and stripped.startswith("cihai "):
                # Colorize example command
                colored = self._colorize_example(stripped, theme)
                lines.append(f"{indent}  {colored}\n")
            elif not stripped:
                # Empty line ends examples section
                in_examples = False
                lines.append(line)
            else:
                # Regular text
                lines.append(f"{indent}{stripped}\n" if stripped else line)

        return "".join(lines)

    def _colorize_example(self, line: str, theme: HelpTheme) -> str:
        """Colorize a single example command line.

        Applies colors to tokens based on their position and prefix:
        - First token (program name): magenta + bold
        - Second token (subcommand): cyan
        - Tokens starting with "--": green (long option)
        - Tokens starting with "-": green (short option)
        - Other tokens: yellow (values/labels)

        Parameters
        ----------
        line : str
            The example command line to colorize.
        theme : HelpTheme
            The color theme to apply.

        Returns
        -------
        str
            The colorized command line.
        """
        tokens = re.split(r"(\s+)", line)
        result: list[str] = []
        seen_prog = False
        seen_action = False
        expect_value = False

        for token in tokens:
            if not token or token.isspace():
                result.append(token)
                continue

            if not seen_prog:
                result.append(f"{theme.prog}{token}{theme.reset}")
                seen_prog = True
            elif not seen_action:
                result.append(f"{theme.action}{token}{theme.reset}")
                seen_action = True
            elif token.startswith("--"):
                result.append(f"{theme.long_option}{token}{theme.reset}")
                expect_value = True
            elif token.startswith("-"):
                result.append(f"{theme.short_option}{token}{theme.reset}")
                expect_value = True
            elif expect_value:
                result.append(f"{theme.label}{token}{theme.reset}")
                expect_value = False
            else:
                result.append(f"{theme.label}{token}{theme.reset}")

        return "".join(result)


def create_formatter(colors: Colors | None = None) -> type[CihaiHelpFormatter]:
    """Create a formatter class with theme bound.

    Uses a class factory pattern to inject the theme into the formatter
    since argparse instantiates formatters internally.

    Parameters
    ----------
    colors : Colors | None
        Color configuration. If None, auto-detects based on environment.

    Returns
    -------
    type[CihaiHelpFormatter]
        A formatter class with the appropriate theme set.

    Examples
    --------
    >>> from cihai_cli._colors import Colors, ColorMode
    >>> formatter_class = create_formatter(Colors(ColorMode.NEVER))
    >>> formatter = formatter_class("cihai")
    >>> formatter._theme is None
    True
    """
    from ._colors import ColorMode, Colors

    if colors is None:
        colors = Colors(ColorMode.AUTO)

    theme = HelpTheme.default() if colors.enabled else None

    class ThemedCihaiHelpFormatter(CihaiHelpFormatter):
        """CihaiHelpFormatter with bound theme."""

        def __init__(self, prog: str, **kwargs: t.Any) -> None:
            super().__init__(prog, **kwargs)
            self._theme = theme

    return ThemedCihaiHelpFormatter
