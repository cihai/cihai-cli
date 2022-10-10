(cli)=

# Commands

```{toctree}
:caption: General

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
