*cihai-cli* - Command line interface to the `cihai`_ `CJK`_-language library

|pypi| |docs| |build-status| |coverage| |license|

This project is under active development. Follow our progress and check
back for updates!

Installation
------------

.. code-block:: sh

   $ pip install --user cihai[cli]

Character lookup
----------------

See `CLI`_ in the documentation for full usage information.

.. code-block:: sh

   $ cihai info 好
   char: 好
   kCantonese: hou2 hou3
   kDefinition: good, excellent, fine; well
   kHangul: 호
   kJapaneseOn: KOU
   kKorean: HO
   kMandarin: hǎo
   kTang: '*xɑ̀u *xɑ̌u'
   kTotalStrokes: '6'
   ucn: U+597D

   # retrieve all character information (including book indices)
   $ cihai info 好 -a
   char: 好
   kCangjie: VND
   kCantonese: hou2 hou3
   kCihaiT: '378.103'
   kDefinition: good, excellent, fine; well
   kFenn: 552A
   kFourCornerCode: '4744.7'
   kFrequency: '1'
   kGradeLevel: '1'
   kHKGlyph: 0871
   kHangul: 호
   kHanyuPinlu: hǎo(6060) hāo(142) hào(115)
   kHanyuPinyin: 21028.010:hǎo,hào
   kJapaneseKun: KONOMU SUKU YOI
   kJapaneseOn: KOU
   kKorean: HO
   kMandarin: hǎo
   kPhonetic: '481'
   kRSAdobe_Japan1_6: C+1975+38.3.3 C+1975+39.3.3
   kRSKangXi: '38.3'
   kTang: '*xɑ̀u *xɑ̌u'
   kTotalStrokes: '6'
   kVietnamese: háo
   kXHC1983: 0445.030:hǎo 0448.030:hào
   ucn: U+597D

Reverse lookup
--------------

.. code-block:: sh

   $ cihai reverse library
   char: 圕
   kCantonese: syu1
   kDefinition: library
   kJapaneseOn: TOSHOKAN SHO
   kMandarin: tú
   kTotalStrokes: '13'
   ucn: U+5715
   --------
   char: 嫏
   kCantonese: long4
   kDefinition: the place where the supreme stores his books; library
   kJapaneseOn: ROU
   kMandarin: láng
   kTotalStrokes: '11'
   ucn: U+5ACF
   --------

Developing
----------
`poetry`_ is a required package to develop.

``git clone https://github.com/cihai/cihai-cli.git``

``cd cihai-cli``

``poetry install -E "docs test coverage lint format"``

Makefile commands prefixed with ``watch_`` will watch files and rerun.

Tests
"""""
``poetry run py.test``

Helpers: ``make test``
Rerun tests on file change: ``make watch_test`` (requires `entr(1)`_)

Documentation
"""""""""""""
Default preview server: http://localhost:8037

``cd docs/`` and ``make html`` to build. ``make serve`` to start http server.

Helpers:
``make build_docs``, ``make serve_docs``

Rebuild docs on file change: ``make watch_docs`` (requires `entr(1)`_)

Rebuild docs and run server via one terminal: ``make dev_docs``  (requires above, and a 
``make(1)`` with ``-J`` support, e.g. GNU Make)

Formatting / Linting
""""""""""""""""""""
The project uses `black`_ and `isort`_ (one after the other) and runs `flake8`_ via 
CI. See the configuration in `pyproject.toml` and `setup.cfg`:

``make black isort``: Run ``black`` first, then ``isort`` to handle import nuances
``make flake8``, to watch (requires ``entr(1)``): ``make watch_flake8`` 

Releasing
"""""""""

As of 0.6, `poetry`_ handles virtualenv creation, package requirements, versioning,
building, and publishing. Therefore there is no setup.py or requirements files.

Update `__version__` in `__about__.py` and `pyproject.toml`::

	git commit -m 'build(cihai-cli): Tag v0.1.1'
	git tag v0.1.1
	git push
	git push --tags
	poetry build
	poetry deploy

.. _poetry: https://python-poetry.org/
.. _entr(1): http://eradman.com/entrproject/
.. _black: https://github.com/psf/black
.. _isort: https://pypi.org/project/isort/
.. _flake8: https://flake8.pycqa.org/

Quick links
-----------
- `Usage`_
- Python `API`_
- `2017 roadmap <https://cihai.git-pull.com/design-and-planning/2017/spec.html>`_

.. _API: https://cihai-cli.git-pull.com/api.html
.. _Usage: https://cihai-cli.git-pull.com/usage.html
.. _CLI: https://cihai-cli.git-pull.com/cli.html

- Python support: >= 3.6, pypy
- Source: https://github.com/cihai/cihai-cli
- Docs: https://cihai-cli.git-pull.com
- Changelog: https://cihai-cli.git-pull.com/history.html
- API: https://cihai-cli.git-pull.com/api.html
- Issues: https://github.com/cihai/cihai-cli/issues
- Test coverage   https://codecov.io/gh/cihai/cihai-cli
- pypi: https://pypi.python.org/pypi/cihai-cli
- OpenHub: https://www.openhub.net/p/cihai-cli
- License: MIT

.. |pypi| image:: https://img.shields.io/pypi/v/cihai_cli.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/cihai_cli

.. |docs| image:: https://github.com/cihai/cihai-cli/workflows/Publish%20Docs/badge.svg
   :alt: Docs
   :target: https://github.com/cihai/cihai-cli/actions?query=workflow%3A"Publish+Docs"

.. |build-status| image:: https://github.com/cihai/cihai-cli/workflows/tests/badge.svg
   :alt: Build Status
   :target: https://github.com/cihai/cihai-cli/actions?query=workflow%3A"tests"

.. |coverage| image:: https://codecov.io/gh/cihai/cihai-cli/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/cihai-cli

.. |license| image:: https://img.shields.io/github/license/cihai/cihai-cli.svg
    :alt: License 

.. _cihai: https://cihai.git-pull.com
.. _CJK: https://cihai.git-pull.com/glossary.html#term-cjk
.. _UNIHAN: http://unicode.org/charts/unihan.html
