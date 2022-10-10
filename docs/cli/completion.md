(completion)=

(completions)=

(cli-completions)=

# Completions

## cihai-cli 0.15+ (experimental)

```{note}
See the [shtab library's documentation on shell completion](https://docs.iterative.ai/shtab/use/#cli-usage) for the most up to date way of connecting completion for cihai-cli.
```

Provisional support for completions in cihai-cli 0.15+ are powered by [shtab](https://docs.iterative.ai/shtab/). This must be **installed separately**, as it's **not currently bundled with cihai-cli**.

```console
$ pip install shtab --user
```

:::{tab} bash

```bash
shtab --shell=bash -u cihai_cli.cli.create_parser \
  | sudo tee "$BASH_COMPLETION_COMPAT_DIR"/CIHAI
```

:::

:::{tab} zsh

```zsh
shtab --shell=zsh -u cihai_cli.cli.create_parser \
  | sudo tee /usr/local/share/zsh/site-functions/_CIHAI
```

:::

:::{tab} tcsh

```zsh
shtab --shell=tcsh -u cihai_cli.cli.create_parser \
  | sudo tee /etc/profile.d/CIHAI.completion.csh
```

:::

## cihai-cli 0.2 to 0.14

```{note}
See the [click library's documentation on shell completion](https://click.palletsprojects.com/en/8.0.x/shell-completion/) for the most up to date way of connecting completion for cihai.
```

cihai-cli 0.2 to 0.14 use [click](https://click.palletsprojects.com)'s completion:

:::{tab} bash

_~/.bashrc_:

```bash

eval "$(_CIHAI_COMPLETE=bash_source cihai)"

```

:::

:::{tab} zsh

_~/.zshrc_:

```zsh

eval "$(_CIHAI_COMPLETE=zsh_source cihai)"

```

:::
