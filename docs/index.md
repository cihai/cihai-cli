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

## Install

```console
$ pip install cihai-cli
```

```console
$ uv tool install cihai-cli
```

## At a glance

Look up a CJK character:

```console
$ cihai info 好
```

```
char: 好
kDefinition: good, excellent, fine; well
kMandarin: hǎo
```

Search definitions:

```console
$ cihai reverse library
```

```
圕: library
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
