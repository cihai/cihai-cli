"""CLI functionality for cihai-cli."""

from __future__ import annotations

import argparse
import logging
import sys
import textwrap
import typing as t

import yaml

from cihai.__about__ import __version__ as cihai_version
from cihai.core import Cihai
from unihan_etl.__about__ import __version__ as unihan_etl_version

from .__about__ import __version__
from ._formatter import create_formatter

log = logging.getLogger(__name__)


#: fields which are human friendly
HUMAN_UNIHAN_FIELDS = [
    "char",
    "ucn",
    "kDefinition",
    "kCantonese",
    "kHangul",
    "kJapaneseOn",
    "kKorean",
    "kMandarin",
    "kVietnamese",
    "kTang",
    "kTotalStrokes",
]

INFO_SHORT_HELP = 'Get details on a CJK character, e.g. "好"'


def build_description(
    intro: str,
    example_blocks: t.Sequence[tuple[str | None, t.Sequence[str]]],
) -> str:
    """Assemble help text with optional example sections.

    Parameters
    ----------
    intro : str
        Introduction text to display at the top of the help.
    example_blocks : Sequence[tuple[str | None, Sequence[str]]]
        List of (heading, commands) tuples. If heading is None, displays
        as "examples:", otherwise as "{heading} examples:".

    Returns
    -------
    str
        Formatted help text with examples.
    """
    sections: list[str] = []
    intro_text = textwrap.dedent(intro).strip()
    if intro_text:
        sections.append(intro_text)

    for heading, commands in example_blocks:
        if not commands:
            continue
        title = "examples:" if heading is None else f"{heading} examples:"
        lines = [title]
        lines.extend(f"  {command}" for command in commands)
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


CLI_DESCRIPTION = build_description(
    """
    cihai - CJK character lookup tool.

    Look up Chinese, Japanese, and Korean characters using the Unihan database.
    """,
    (
        (
            "info",
            [
                "cihai info 好",
                "cihai info --all 好",
            ],
        ),
        (
            "reverse",
            [
                'cihai reverse "good"',
                'cihai reverse --all "library"',
            ],
        ),
    ),
)

INFO_DESCRIPTION = build_description(
    """
    Get details on a CJK character.
    """,
    (
        (
            None,
            [
                "cihai info 好",
                "cihai info 你",
                "cihai info --all 好",
            ],
        ),
    ),
)

REVERSE_DESCRIPTION = build_description(
    """
    Search definitions for character matches.
    """,
    (
        (
            None,
            [
                'cihai reverse "good"',
                'cihai reverse "library"',
                'cihai reverse --all "love"',
            ],
        ),
    ),
)


def create_parser() -> argparse.ArgumentParser:
    """Create argparse for cihai-cli."""
    formatter_class = create_formatter()

    parser = argparse.ArgumentParser(
        prog="cihai",
        description=CLI_DESCRIPTION,
        formatter_class=formatter_class,
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=(
            f"%(prog)s cihai-cli {__version__}, "
            f"cihai {cihai_version}, unihan-etl {unihan_etl_version}"
        ),
    )
    parser.add_argument(
        "--log-level",
        action="store",
        default="INFO",
        help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--config",
        "-c",
        dest="config_file",
        action="store",
        help="Path to custom config file",
    )
    subparsers = parser.add_subparsers(dest="subparser_name")
    info_parser = subparsers.add_parser(
        "info",
        help=INFO_SHORT_HELP,
        description=INFO_DESCRIPTION,
        formatter_class=formatter_class,
    )
    create_info_subparser(info_parser)
    reverse_parser = subparsers.add_parser(
        "reverse",
        help='Search all info for character matches, e.g. "good"',
        description=REVERSE_DESCRIPTION,
        formatter_class=formatter_class,
    )
    create_reverse_subparser(reverse_parser)

    return parser


class CLILoadNamespace(argparse.Namespace):
    """Typing for CLI namespace."""

    config_file: str | None
    version: bool
    log_file: str | None


def cli(_args: list[str] | None = None) -> None:
    """Retrieve CJK information via CLI.

    For help and example usage, see documentation:

    https://cihai-cli.git-pull.com and https://cihai.git-pull.com
    """
    parser = create_parser()
    args = parser.parse_args(_args, namespace=CLILoadNamespace())

    setup_logger(level=args.log_level.upper())

    c = Cihai.from_file(args.config_file) if args.config_file else Cihai()

    if not c.unihan.is_bootstrapped:
        log.info("Bootstrapping Unihan database")
        c.unihan.bootstrap(options=c.config.get("unihan_options", {}))

    if args.subparser_name is None:
        parser.print_help()
        return
    if args.subparser_name == "info":
        command_info(c=c, char=args.char, show_all=args.show_all)
    elif args.subparser_name == "reverse":
        command_reverse(c=c, char=args.char, show_all=args.show_all)
    else:
        log.info(f"No subparser for {args.subparser_name}")


def create_info_subparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Create ``cihai info`` subparser."""
    parser.add_argument("char", metavar="<character>", help="Lookup term / character")
    parser.add_argument(
        "--all",
        "-a",
        dest="show_all",
        action="store_true",
        help="Show all character details",
    )
    return parser


def command_info(c: Cihai, char: str, show_all: bool) -> None:
    """Look up a definition by term."""
    query = c.unihan.lookup_char(char).first()
    attrs = {}
    if not query:
        log.info("No records found for %s", char)
        sys.exit()
    for col, _, _ in query.__table__.columns._collection:
        value = getattr(query, col)
        if value:
            if not show_all and str(col) not in HUMAN_UNIHAN_FIELDS:
                continue
            attrs[str(col)] = value
    log.info(
        yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip("\n"),
    )


def create_reverse_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    """Create ``cihai reverse`` subparser."""
    parser.add_argument("char", metavar="<character>", help="Lookup term / character")
    parser.add_argument(
        "--all",
        "-a",
        dest="show_all",
        action="store_true",
        help="Show all character details",
    )
    return parser


def command_reverse(c: Cihai, char: str, show_all: bool) -> None:
    """Lookup a word or phrase by searching definitions."""
    query = c.unihan.reverse_char([char])
    if not query.count():
        log.info("No records found for %s", char)
        sys.exit()
    for k in query:
        attrs = {}
        for col, _, _ in k.__table__.columns._collection:
            value = getattr(k, col)
            if value:
                if not show_all and str(col) not in HUMAN_UNIHAN_FIELDS:
                    continue
                attrs[str(col)] = value
        log.info(
            yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip(
                "\n",
            ),
        )
        log.info("--------")


def setup_logger(
    logger: logging.Logger | None = None,
    level: str = "INFO",
) -> None:
    """Configure logging for CLI use.

    Parameters
    ----------
    logger : :py:class:`Logger`
        Instance of logger, if one set up.
    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)
