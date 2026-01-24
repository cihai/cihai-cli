"""Terminal color support for cihai-cli."""

from __future__ import annotations

import enum
import os
import sys


class ColorMode(enum.Enum):
    """Color output mode selection."""

    AUTO = "auto"
    ALWAYS = "always"
    NEVER = "never"


class Colors:
    """Terminal color helper with NO_COLOR/FORCE_COLOR support.

    Respects the standard NO_COLOR (https://no-color.org/) and FORCE_COLOR
    environment variables for controlling color output.

    Examples
    --------
    >>> colors = Colors(ColorMode.NEVER)
    >>> colors.enabled
    False

    >>> colors = Colors(ColorMode.ALWAYS)
    >>> colors.enabled
    True
    """

    def __init__(self, mode: ColorMode = ColorMode.AUTO) -> None:
        self.mode = mode
        self._enabled = self._should_enable()

    def _should_enable(self) -> bool:
        """Determine if colors should be enabled based on mode and environment."""
        # NO_COLOR takes highest precedence
        if os.environ.get("NO_COLOR"):
            return False
        if self.mode == ColorMode.NEVER:
            return False
        if self.mode == ColorMode.ALWAYS:
            return True
        # FORCE_COLOR overrides TTY detection
        if os.environ.get("FORCE_COLOR"):
            return True
        return sys.stdout.isatty()

    @property
    def enabled(self) -> bool:
        """Return whether colors are enabled."""
        return self._enabled


# ANSI color code mapping
COLOR_CODES: dict[str, str] = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}


def style(text: str, *, fg: str | None = None, bold: bool = False) -> str:
    """Apply ANSI styling to text.

    Parameters
    ----------
    text : str
        The text to style.
    fg : str | None
        Foreground color name (black, red, green, yellow, blue, magenta, cyan, white).
    bold : bool
        Whether to apply bold styling.

    Returns
    -------
    str
        The styled text with ANSI escape codes, or plain text if no styles applied.

    Examples
    --------
    >>> style("plain")
    'plain'

    >>> style("hello", fg="green")
    '\\x1b[32mhello\\x1b[0m'

    >>> style("world", fg="blue", bold=True)
    '\\x1b[34;1mworld\\x1b[0m'
    """
    codes: list[str] = []

    if fg and fg in COLOR_CODES:
        codes.append(COLOR_CODES[fg])
    if bold:
        codes.append("1")

    if not codes:
        return text

    return f"\033[{';'.join(codes)}m{text}\033[0m"
