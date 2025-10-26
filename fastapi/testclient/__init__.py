"""Test client compatible with the minimal FastAPI facade."""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI


class Response:
    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> Any:
        return self._payload

    @property
    def text(self) -> str:
        return str(self._payload)


class TestClient:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def get(self, path: str, params: Optional[Dict[str, str]] = None) -> Response:
        status, payload = self.app.handle_request("GET", path, query=params)
        return Response(status, payload)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Response:
        status, payload = self.app.handle_request("POST", path, json_body=json)
        return Response(status, payload)


__all__ = ["TestClient", "Response"]
