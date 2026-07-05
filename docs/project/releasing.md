# Releasing

## Release Process

Releases are triggered by git tags and published to [PyPI] via [OIDC trusted
publishing]. Agent-assisted release work stops at the release commit unless the
user explicitly asks for tag handling.

1. Update `CHANGES` with the release notes

2. Bump version in `src/cihai_cli/__about__.py`

3. Commit:

   ```console
   $ git commit -m "Tag v<version>"
   ```

4. Push the release commit:

   ```console
   $ git push
   ```

5. The release owner creates and pushes the `v<version>` tag

6. CI builds and publishes to PyPI automatically via trusted publishing

[OIDC trusted publishing]: https://docs.pypi.org/trusted-publishers/
[PyPI]: https://pypi.org/project/cihai-cli/
