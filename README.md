# cihai-cli &middot; [![Python Package](https://img.shields.io/pypi/v/cihai_cli.svg)](https://pypi.org/project/cihai-cli/) [![License](https://img.shields.io/github/license/cihai/cihai-cli.svg)](https://github.com/cihai/cihai-cli/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/cihai/cihai-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/cihai-cli)

Command line interface to the [cihai](https://cihai.git-pull.com)
[CJK](https://cihai.git-pull.com/glossary.html#term-cjk)-language library.

This project is under active development. Follow our progress and check back for updates!

## Installation

```console
$ pip install --user cihai-cli
```

### Developmental releases

You can test the unpublished version of cihai-cli before its released.

- [pip](https://pip.pypa.io/en/stable/):

  ```console
  $ pip install --user --upgrade --pre cihai-cli
  ```

- [pipx](https://pypa.github.io/pipx/docs/):

  ```console
  $ pipx install --suffix=@next cihai-cli --pip-args '\--pre' --include-deps --force
  ```

  Then use `cihai@next info 好`.

For more information see
[developmental releases](https://cihai-cli.git-pull.com/quickstart.html#developmental-releases)

## Character lookup

See [CLI](https://cihai-cli.git-pull.com/cli.html) in the documentation for full usage information.

```console
$ cihai info 好
```

```yaml
char: 好
kCantonese: hou2 hou3
kDefinition: good, excellent, fine; well
kHangul: 호
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kTang: "*xɑ̀u *xɑ̌u"
kTotalStrokes: "6"
ucn: U+597D
```

Retrieve all character information (including book indices):

```console
$ cihai info 好 -a
```

```yaml
char: 好
kCangjie: VND
kCantonese: hou2 hou3
kCihaiT: "378.103"
kDefinition: good, excellent, fine; well
kFenn: 552A
kFourCornerCode: "4744.7"
kFrequency: "1"
kGradeLevel: "1"
kHKGlyph: 0871
kHangul: 호
kHanyuPinlu: hǎo(6060) hāo(142) hào(115)
kHanyuPinyin: 21028.010:hǎo,hào
kJapaneseKun: KONOMU SUKU YOI
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kPhonetic: "481"
kRSAdobe_Japan1_6: C+1975+38.3.3 C+1975+39.3.3
kRSKangXi: "38.3"
kTang: "*xɑ̀u *xɑ̌u"
kTotalStrokes: "6"
kVietnamese: háo
kXHC1983: 0445.030:hǎo 0448.030:hào
ucn: U+597D
```

## Reverse lookup

```console
$ cihai reverse library
```

```yaml
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
```

## Developing

```console
$ git clone https://github.com/cihai/cihai-cli.git
```

```console
$ cd cihai-cli
```

[Bootstrap your environment and learn more about contributing](https://cihai.git-pull.com/contributing/). We use the same conventions / tools across all cihai projects: `pytest`, `sphinx`, `flake8`, `mypy`, `black`, `isort`, `tmuxp`, and file watcher helpers (e.g. `entr(1)`).

## Python versions

- Final Python 3.7 version: 0.16.0

## Quick links

- [Quickstart](https://cihai-cli.git-pull.com/quickstart.html)
- Python [API](https://cihai-cli.git-pull.com/api.html)
- [2017 roadmap](https://cihai.git-pull.com/design-and-planning/2017/spec.html)
- Python support: >= 3.8, pypy
- Source: <https://github.com/cihai/cihai-cli>
- Docs: <https://cihai-cli.git-pull.com>
- Changelog: <https://cihai-cli.git-pull.com/history.html>
- API: <https://cihai-cli.git-pull.com/api.html>
- Issues: <https://github.com/cihai/cihai-cli/issues>
- Test coverage <https://codecov.io/gh/cihai/cihai-cli>
- pypi: <https://pypi.python.org/pypi/cihai-cli>
- OpenHub: <https://www.openhub.net/p/cihai-cli>
- License: MIT

[![Docs](https://github.com/cihai/cihai-cli/workflows/docs/badge.svg)](https://cihai-cli.git-pull.com/)
[![Build Status](https://github.com/cihai/cihai-cli/workflows/tests/badge.svg)](https://github.com/cihai/cihai-cli/actions?query=workflow%3A%22tests%22)
