(cli)=

# CLI Reference

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} cihai info
:link: info
:link-type: doc
Look up a CJK character by glyph or codepoint.
:::

:::{grid-item-card} cihai reverse
:link: reverse
:link-type: doc
Search definitions for a given term.
:::

:::{grid-item-card} Completions
:link: completion
:link-type: doc
Shell completion for bash, zsh, and tcsh.
:::

::::

```{toctree}
:caption: General
:maxdepth: 1

info
reverse
```

```{toctree}
:caption: Completion
:maxdepth: 1

completion
```

(cli-main)=

(cihai-main)=

(cihai-cli-main)=

## Command: `cihai`

```{eval-rst}
.. argparse::
    :module: cihai_cli.cli
    :func: create_parser
    :prog: cihai
    :nosubcommands:

    subparser_name : @replace
        See :ref:`cli-info`, :ref:`cli-reverse`
```
