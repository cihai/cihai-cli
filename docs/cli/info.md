(cli-info)=

(cihai-info)=

# cihai info

Use `cihai info` when you already have a character and want its readings,
definition, and common lookup fields. The command prints a concise YAML record
by default; ask for the full record only when you need every field.

## Command

```{eval-rst}
.. argparse::
    :module: cihai_cli.cli
    :func: create_parser
    :prog: cihai
    :path: info
```
