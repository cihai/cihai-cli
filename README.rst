*cihai-cli* - Command line interface to the `cihai`_ `CJK`_-language library

|pypi| |docs| |build-status| |coverage| |license|

This project is under active development. Follow our progress and check
back for updates!

Installation
------------

.. code-block:: sh

   $ pip install --user cihai_cli

Command line
""""""""""""

Character lookup:

.. code-block:: sh

   $ cihai info 好
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

Reverse lookup:

.. code-block:: sh

   $ cihai lookup library
   --------
   char: 圕
   kCangjie: WLGA
   kCantonese: syu1
   kCihaiT: '308.302'
   kDefinition: library
   kJapaneseOn: TOSHOKAN SHO
   kMandarin: tú
   kPhonetic: 1235 1364
   kRSAdobe_Japan1_6: C+14418+31.3.10
   kRSKangXi: '31.10'
   kSemanticVariant: U+5716<kMatthews
   kTotalStrokes: '13'
   kXHC1983: 1163.040:tú
   ucn: U+5715

   --------
   char: 嫏
   kCangjie: VIIL
   kCantonese: long4
   kCihaiT: '390.506'
   kDefinition: the place where the supreme stores his books; library
   kHanyuPinyin: 21062.030:láng
   kJapaneseOn: ROU
   kMandarin: láng
   kPhonetic: '832'
   kRSAdobe_Japan1_6: C+21424+38.3.10
   kRSKangXi: '38.9'
   kTotalStrokes: '11'
   kXHC1983: 0674.090:láng
   ucn: U+5ACF

Works with any field:

.. code-block:: sh

   $ cihai lookup hào
   --------
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

   --------
   char: 妞
   kCangjie: VNG
   kCantonese: nau2
   kCihaiT: '380.503'
   kDefinition: girl
   kFenn: 676H
   kFourCornerCode: '4741.5'
   kFrequency: '5'
   kHKGlyph: 0876
   kHanyuPinyin: 21033.100:hào,niū
   kJapaneseOn: JUU NYU CHUU
   kMandarin: niū
   kPhonetic: '90'
   kRSKangXi: '38.4'
   kTotalStrokes: '7'
   kXHC1983: 0836.060:niū
   ucn: U+599E

Quick links
-----------

- `Usage`_
- Python `API`_
- `2017 roadmap <https://cihai.git-pull.com/en/latest/design-and-planning/2017/spec.html>`_

.. _API: https://cihai-cli.git-pull.com/en/latest/api.html
.. _Usage: https://cihai-cli.git-pull.com/en/latest/usage.html

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

                    $ pip install cihai_cli
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
