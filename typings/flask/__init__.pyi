"""Minimal Flask stub for Pyright only. Runtime still uses the real package from requirements.txt."""

from collections.abc import Callable
from typing import Any, TypeVar

_C = TypeVar("_C", bound=Callable[..., Any])

class Response:
    """Subset of werkzeug.Response used by tests / Pyright."""

    status_code: int
    text: str

class FlaskClient:
    def get(self, path: str, **kwargs: Any) -> Response: ...

class Flask:
    def __init__(self, import_name: str, **kwargs: Any) -> None: ...
    def route(self, rule: str, **options: Any) -> Callable[[_C], _C]: ...
    def test_client(self, use_cookies: bool = True, **kwargs: Any) -> FlaskClient: ...
    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        **options: Any,
    ) -> None: ...
