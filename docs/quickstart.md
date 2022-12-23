(usage)=

# Usage

cihai is designed to work out-of-the-box without configuration.

## Installation

```console
$ pip install --user cihai-cli
```

### Developmental releases

New versions of cihai CLI are published to PyPI as alpha, beta, or release candidates. In their
versions you will see notification like `a1`, `b1`, and `rc1`, respectively. `1.10.0b4` would mean
the 4th beta release of `1.10.0` before general availability.

- [pip]\:

  ```console
  $ pip install --user --upgrade --pre cihai-cli
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@next cihai-cli --pip-args '\--pre' --include-deps --force
  ```

  Then use `cihai@next info 好`.

via trunk (can break easily):

- [pip]\:

  ```console
  $ pip install --user -e git+https://github.com/cihai/cihai-cli.git#egg=cihai-cli
  ```

- [pipx]\:

  ```console
  $ pipx install --suffix=@master 'cihai-cli @ git+https://github.com/cihai/cihai.git@master' --include-deps --force
  ```

[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pypa.github.io/pipx/docs/

## Configuration

See {ref}`cihai's configuration <cihai:configuration>` documentation.
