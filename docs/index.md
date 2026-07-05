(index)=

# cihai-cli

Command line frontend for the [cihai](https://cihai.git-pull.com/) CJK language library.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and look up your first character.
:::

:::{grid-item-card} CLI Reference
:link: cli/index
:link-type: doc
Every command, flag, and option.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, and releases.
:::

::::

## Run cihai

Choose how you want to invoke the `cihai` command. The cooldown control only
changes `uvx` commands because `uvx` can keep cihai-cli itself out of the
cooldown window.

```{cihai-usage}
:variant: compact
```

## At a glance

Use {ref}`cihai info <cihai-info>` to look up a CJK character:

```console
$ cihai info 好
```

```yaml
char: 好
kCantonese: hou2 hou3
kDefinition: good, excellent, fine; well
kHangul: 호:0E
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kTang: '*xɑ̀u *xɑ̌u'
kVietnamese: háo
ucn: U+597D
```

Use {ref}`cihai reverse <cihai-reverse>` to search definitions:

```console
$ cihai reverse good
```

```yaml
char: 好
kCantonese: hou2 hou3
kDefinition: good, excellent, fine; well
kHangul: 호:0E
kJapaneseOn: KOU
kKorean: HO
kMandarin: hǎo
kTang: '*xɑ̀u *xɑ̌u'
kVietnamese: háo
ucn: U+597D
```

Data is downloaded automatically on first use via [cihai](https://cihai.git-pull.com/).

```{toctree}
:hidden:

quickstart
cli/index
api
project/index
history
migration
GitHub <https://github.com/cihai/cihai-cli>
```
