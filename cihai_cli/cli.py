# -*- encoding: utf8 - *-
from __future__ import absolute_import, print_function

import logging
import sys

import click
import yaml

from cihai._compat import PY2
from cihai.bootstrap import bootstrap_unihan
from cihai.core import Cihai

from .__about__ import __version__

#: fields which are human friendly
HUMAN_UNIHAN_FIELDS = [
    'char',
    'ucn',
    'kDefinition',
    'kCantonese',
    'kHangul',
    'kJapaneseOn',
    'kKorean',
    'kMandarin',
    'kVietnamese',
    'kTang',
    'kTotalStrokes',
]


@click.group(context_settings={'obj': {}})
@click.version_option(
    __version__, '-V', '--version', message='%(prog)s %(version)s'
)
@click.option('-c', '--config', type=click.Path(exists=True),
              metavar='<config-file>', help="path to custom config file")
@click.option('--log_level', default='INFO', metavar='<log-level>',
              help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
@click.pass_context
def cli(ctx, config, log_level):
    """Retrieve CJK information via CLI.

    For help and example usage, see documentation:

    https://cihai-cli.git-pull.com and https://cihai.git-pull.com"""
    setup_logger(
        level=log_level.upper()
    )
    if config:
        c = Cihai.from_file(config)
    else:
        c = Cihai()

    if not c.is_bootstrapped:
        click.echo("Bootstrapping Unihan database")
        bootstrap_unihan(c.metadata, c.config.get('unihan_options', {}))
        c.reflect_db()

    ctx.obj['c'] = c  # pass Cihai object down to other commands


@cli.command(name='info',
             short_help=u'Get details on a CJK character, e.g. "好"')
@click.argument('char', metavar='<character>')
@click.option('-a', '--all', 'show_all', is_flag=True,
              help="Show all character details")
@click.pass_context
def command_info(ctx, char, show_all):
    c = ctx.obj['c']
    query = c.lookup_char(char).first()
    attrs = {}
    if not query:
        click.echo("No records found for %s" % char, err=True)
        sys.exit()
    for c in query.__table__.columns._data.keys():
        value = getattr(query, c)
        if value:
            if PY2:
                value = value.encode('utf-8')
            if not show_all and str(c) not in HUMAN_UNIHAN_FIELDS:
                continue
            attrs[str(c)] = value
    click.echo(
        yaml.safe_dump(
            attrs, allow_unicode=True, default_flow_style=False
        ).strip('\n')
    )


@cli.command(name='reverse',
             short_help='Search all info for character matches, e.g. "good"')
@click.argument('char', metavar='<character>')
@click.option('-a', '--all', 'show_all', is_flag=True,
              help="Show all character details")
@click.pass_context
def command_reverse(ctx, char, show_all):
    c = ctx.obj['c']
    query = c.reverse_char([char])
    if not query.count():
        click.echo("No records found for %s" % char, err=True)
        sys.exit()
    for k in query:
        attrs = {}
        for c in k.__table__.columns._data.keys():
            value = getattr(k, c)
            if value:
                if PY2:
                    value = value.encode('utf-8')
                if not show_all and str(c) not in HUMAN_UNIHAN_FIELDS:
                    continue
                attrs[str(c)] = value
        click.echo(yaml.safe_dump(
            attrs, allow_unicode=True, default_flow_style=False
        ).strip('\n'))
        click.echo('--------')


def setup_logger(logger=None, level='INFO'):
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
