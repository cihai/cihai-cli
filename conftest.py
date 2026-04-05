"""Root pytest configuration for cihai-cli."""

from __future__ import annotations

import typing as t

import pytest


@pytest.fixture(autouse=True)
def _doctest_monkeypatch(
    doctest_namespace: dict[str, object],
) -> t.Iterator[None]:
    """Expose monkeypatch in source doctests and undo env changes after use."""
    monkeypatch = pytest.MonkeyPatch()
    doctest_namespace["monkeypatch"] = monkeypatch
    yield
    monkeypatch.undo()
