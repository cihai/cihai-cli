(quickstart)=

# Quickstart

cihai-cli installs the `cihai` command and works out-of-the-box without
configuration.

## Run cihai

Choose how you want to invoke the command. `uvx` runs cihai-cli on demand,
`pipx` runs it through an isolated tool environment, and `pip` means you already
installed the `cihai` script into your user Python environment.

```{cihai-usage}
```

## Installation options

Pick the installer that matches how you want to run the command. `uvx` runs
cihai-cli on demand, `pipx` installs an isolated command, and `pip` installs it
into your user Python environment.

```{cihai-install}
```

(developmental-releases)=

### Developmental releases

New versions of cihai CLI are published to [PyPI] as alpha, beta, or release candidates. In their
versions you will see notification like `a1`, `b1`, and `rc1`, respectively. `1.10.0b4` would mean
the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre cihai-cli
  ```

- [pipx]\:

  ```console
  $ pipx install \
      --suffix=@next \
      --pip-args '\--pre' \
      --force \
      'cihai-cli'
  ```

  Run that prerelease command as `cihai@next`:

  ```console
  $ cihai@next info 好
  ```

- [uv tool install][uv-tools]\:

  ```console
  $ uv tool install --prerelease=allow cihai-cli
  ```

- [uv]\:

  ```console
  $ uv add cihai-cli --prerelease allow
  ```

- [uvx]\:

  ```console
  $ uvx --from 'cihai-cli' --prerelease allow cihai
  ```

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install --user -e git+https://github.com/cihai/cihai-cli.git#egg=cihai-cli
  ```

- [uv]\:

  ```console
  $ uv add git+https://github.com/cihai/cihai-cli.git#egg=cihai-cli
  ```

- [pipx]\:

  ```console
  $ pipx install \
      --suffix=@master \
      --include-deps \
      --force \
      'cihai-cli @ git+https://github.com/cihai/cihai-cli.git@master'
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/
[PyPI]: https://pypi.org/project/cihai-cli/
[uv]: https://docs.astral.sh/uv/
[uv-tools]: https://docs.astral.sh/uv/concepts/tools/
[uvx]: https://docs.astral.sh/uv/guides/tools/

## Configuration

See {ref}`cihai's configuration <cihai:configuration>` documentation.
