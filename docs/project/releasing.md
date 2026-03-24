# Releasing

## Release Process

Releases are triggered by git tags and published to PyPI via OIDC trusted publishing.

1. Update `CHANGES` with the release notes

2. Bump version in `src/cihai_cli/__about__.py`

3. Commit:

   ```console
   $ git commit -m "cihai-cli <version>"
   ```

4. Tag:

   ```console
   $ git tag v<version>
   ```

5. Push:

   ```console
   $ git push && git push --tags
   ```

6. CI builds and publishes to PyPI automatically via trusted publishing
