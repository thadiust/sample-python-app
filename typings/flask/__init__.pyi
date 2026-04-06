"""Minimal Flask stub for Pyright only. Runtime still uses the real package from requirements.txt."""

from collections.abc import Callable
from typing import Any, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

class Flask:
    def __init__(self, import_name: str, **kwargs: Any) -> None: ...
    def route(self, rule: str, **options: Any) -> Callable[[_C], _C]: ...
    def run(self, host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        **options: Any,
    ) -> None: ...
