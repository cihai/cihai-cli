import argparse
import logging
import sys
import typing as t

import yaml

from cihai.__about__ import __version__ as cihai_version
from cihai.core import Cihai
from unihan_etl.__about__ import __version__ as unihan_etl_version

from .__about__ import __version__

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


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cihai")
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
    info_parser = subparsers.add_parser("info", help=INFO_SHORT_HELP)
    create_info_subparser(info_parser)
    reverse_parser = subparsers.add_parser(
        "reverse", help='Search all info for character matches, e.g. "good"'
    )
    create_reverse_subparser(reverse_parser)

    return parser


class CLILoadNamespace(argparse.Namespace):
    config_file: t.Optional[str]
    version: bool
    log_file: t.Optional[str]


def cli(_args: t.Optional[t.List[str]] = None) -> None:
    """Retrieve CJK information via CLI.

    For help and example usage, see documentation:

    https://cihai-cli.git-pull.com and https://cihai.git-pull.com"""

    parser = create_parser()
    args = parser.parse_args(_args, namespace=CLILoadNamespace())

    setup_logger(level=args.log_level.upper())

    c = Cihai.from_file(args.config_file) if args.config_file else Cihai()

    if not c.unihan.is_bootstrapped:
        print("Bootstrapping Unihan database")
        c.unihan.bootstrap(options=c.config.get("unihan_options", {}))

    if args.subparser_name is None:
        parser.print_help()
        return
    elif args.subparser_name == "info":
        command_info(c=c, char=args.char, show_all=args.show_all)
    elif args.subparser_name == "reverse":
        command_reverse(c=c, char=args.char, show_all=args.show_all)
    else:
        print(f"No subparser for {args.subparser_name}")


def create_info_subparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
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
        print("No records found for %s" % char)
        sys.exit()
    for col, _, _ in query.__table__.columns._collection:
        value = getattr(query, col)
        if value:
            if not show_all and str(col) not in HUMAN_UNIHAN_FIELDS:
                continue
            attrs[str(col)] = value
    print(
        yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip("\n")
    )


def create_reverse_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
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
        print("No records found for %s" % char)
        sys.exit()
    for k in query:
        attrs = {}
        for c, _, _ in k.__table__.columns._collection:
            value = getattr(k, c)
            if value:
                if not show_all and str(c) not in HUMAN_UNIHAN_FIELDS:
                    continue
                attrs[str(c)] = value
        print(
            yaml.safe_dump(attrs, allow_unicode=True, default_flow_style=False).strip(
                "\n"
            )
        )
        print("--------")


def setup_logger(
    logger: t.Optional[logging.Logger] = None, level: str = "INFO"
) -> None:
    """Setup logging for CLI use.

    :param logger: instance of logger
    :type logger: :py:class:`Logger`

    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)
