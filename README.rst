*cihai-cli* - Command line interface to the `cihai`_ `CJK`_-language library

|pypi| |docs| |build-status| |coverage| |license|

This project is under active development. Follow our progress and check
back for updates!

Installation
------------

.. code-block:: sh

   $ pip install --user cihai-cli

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

Quick links
-----------

- `Usage`_
- Python `API`_
- `2017 roadmap <https://cihai.git-pull.com/en/latest/design-and-planning/2017/spec.html>`_

.. _API: https://cihai-cli.git-pull.com/en/latest/api.html
.. _Usage: https://cihai-cli.git-pull.com/en/latest/usage.html
.. _CLI: https://cihai-cli.git-pull.com/en/latest/cli.html

==============  ==========================================================
Python support  Python 2.7, >= 3.5, pypy
Source          https://github.com/cihai/cli
Docs            https://cihai-cli.git-pull.com
Changelog       https://cihai-cli.git-pull.com/en/latest/history.html
API             https://cihai-cli.git-pull.com/en/latest/api.html
Issues          https://github.com/cihai/cihai-cli/issues
Travis          https://travis-ci.org/cihai/cli
Test coverage   https://codecov.io/gh/cihai/cli
pypi            https://pypi.python.org/pypi/cihai-cli
OpenHub         https://www.openhub.net/p/cihai
License         MIT
git repo        .. code-block:: bash

                    $ git clone https://github.com/cihai/cli.git
install stable  .. code-block:: bash

                    $ pip install cihai-cli
install dev     .. code-block:: bash

                    $ git clone https://github.com/cihai/cli.git cihai-cli
                    $ cd ./cihai-cli
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. |pypi| image:: https://img.shields.io/pypi/v/cihai_cli.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/cihai_cli

.. |build-status| image:: https://img.shields.io/travis/cihai/cli.svg
   :alt: Build Status
   :target: https://travis-ci.org/cihai/cli

.. |coverage| image:: https://codecov.io/gh/cihai/cli/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/cli

.. |license| image:: https://img.shields.io/github/license/cihai/cli.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/cihai-cli/badge/?version=latest
    :alt: Documentation Status
    :target: https://readthedocs.org/projects/cihai-cli/

.. _cihai: https://cihai.git-pull.com
.. _CJK: https://cihai.git-pull.com/en/latest/glossary.html#term-cjk
.. _UNIHAN: http://unicode.org/charts/unihan.html
