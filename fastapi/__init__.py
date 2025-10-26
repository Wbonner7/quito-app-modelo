"""Minimal FastAPI-compatible facade used for offline testing.

This module provides a very small subset of the `fastapi` API that is
required by the Quito MVP.  The goal is not to be feature complete, but
rather to offer enough surface area so the rest of the codebase and the
unit tests can interact with a web style router without requiring any
third-party dependencies.
"""

from __future__ import annotations

import inspect
import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Callable, Dict, Iterable, Optional, Tuple


class HTTPException(Exception):
    """Exception that mimics ``fastapi.HTTPException``."""

    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class Query:
    """Simple helper used to declare optional query parameters.

    The value returned here is simply the provided default.  The helper is
    kept purely for compatibility with the original FastAPI signature.
    """

    def __init__(self, default: Any = None) -> None:
        self.default = default

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"Query(default={self.default!r})"


@dataclass
class Route:
    method: str
    path: str
    endpoint: Callable[..., Any]
    status_code: int

    def with_prefix(self, prefix: str) -> "Route":
        merged_prefix = prefix.rstrip("/")
        if not merged_prefix:
            return self
        normalized_path = self.path
        if not normalized_path.startswith("/"):
            normalized_path = f"/{normalized_path}"
        return Route(self.method, f"{merged_prefix}{normalized_path}", self.endpoint, self.status_code)


class APIRouter:
    """Extremely small subset of ``fastapi.APIRouter``."""

    def __init__(self) -> None:
        self.routes: list[Route] = []

    def _add_route(self, method: str, path: str, endpoint: Callable[..., Any], status_code: int) -> Callable[..., Any]:
        route = Route(method=method.upper(), path=path, endpoint=endpoint, status_code=status_code)
        self.routes.append(route)
        return endpoint

    def include_router(self, router: "APIRouter", prefix: str = "", tags: Optional[Iterable[str]] = None) -> None:
        del tags
        for route in router.routes:
            self.routes.append(route.with_prefix(prefix))

    def get(self, path: str, *, response_model: Any = None, status_code: int = HTTPStatus.OK) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        del response_model  # Unused but kept for API compatibility
        return lambda endpoint: self._add_route("GET", path, endpoint, status_code)

    def post(self, path: str, *, response_model: Any = None, status_code: int = HTTPStatus.CREATED) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        del response_model
        return lambda endpoint: self._add_route("POST", path, endpoint, status_code)


class FastAPI:
    """A tiny request router compatible with the unit tests."""

    def __init__(self, title: str = "", description: str = "", version: str = "") -> None:
        self.title = title
        self.description = description
        self.version = version
        self.routes: list[Route] = []

    def include_router(self, router: APIRouter, prefix: str = "", tags: Optional[Iterable[str]] = None) -> None:
        del tags  # Tags are metadata-only in this lightweight version
        for route in router.routes:
            self.routes.append(route.with_prefix(prefix))

    def get(self, path: str, *, response_model: Any = None, status_code: int = HTTPStatus.OK) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        del response_model
        return lambda endpoint: self._add_route("GET", path, endpoint, status_code)

    def post(self, path: str, *, response_model: Any = None, status_code: int = HTTPStatus.CREATED) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        del response_model
        return lambda endpoint: self._add_route("POST", path, endpoint, status_code)

    def _add_route(self, method: str, path: str, endpoint: Callable[..., Any], status_code: int) -> Callable[..., Any]:
        route = Route(method=method.upper(), path=path, endpoint=endpoint, status_code=status_code)
        self.routes.append(route)
        return endpoint

    # -- Testing helpers -------------------------------------------------
    def handle_request(self, method: str, path: str, *, json_body: Any = None, query: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        """Execute a request against the registered routes."""

        query = query or {}
        for route in self.routes:
            match, path_params = _match_route(route.path, path)
            if match and route.method == method.upper():
                try:
                    payload = _invoke(route.endpoint, path_params, query, json_body)
                    return route.status_code, payload
                except HTTPException as exc:
                    return exc.status_code, {"detail": exc.detail}
        return HTTPStatus.NOT_FOUND, {"detail": "Not Found"}

    # -- WSGI compatibility ----------------------------------------------
    def __call__(self, environ: Dict[str, Any], start_response: Callable[[str, list[tuple[str, str]]], None]):
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "")
        query_string = environ.get("QUERY_STRING", "")
        query = _parse_query_string(query_string)
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ.get("wsgi.input")
        raw_data = body.read(length) if body and length > 0 else b""
        json_body = json.loads(raw_data.decode("utf-8")) if raw_data else None
        status_code, payload = self.handle_request(method, path, json_body=json_body, query=query)
        response_body = json.dumps(payload).encode("utf-8")
        start_response(f"{status_code} {HTTPStatus(status_code).phrase}", [("Content-Type", "application/json"), ("Content-Length", str(len(response_body)))])
        return [response_body]


def _match_route(route_path: str, requested_path: str) -> Tuple[bool, Dict[str, str]]:
    route_segments = [segment for segment in route_path.strip("/").split("/") if segment]
    request_segments = [segment for segment in requested_path.strip("/").split("/") if segment]
    if route_segments != request_segments and len(route_segments) != len(request_segments):
        return False, {}
    params: Dict[str, str] = {}
    for route_segment, request_segment in zip(route_segments, request_segments):
        if route_segment.startswith("{") and route_segment.endswith("}"):
            params[route_segment.strip("{} ")] = request_segment
        elif route_segment != request_segment:
            return False, {}
    if len(route_segments) != len(request_segments):
        return False, {}
    return True, params


def _invoke(endpoint: Callable[..., Any], path_params: Dict[str, str], query: Dict[str, str], json_body: Any) -> Any:
    signature = inspect.signature(endpoint)
    arguments: Dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        if name in path_params:
            arguments[name] = path_params[name]
        elif name in ("payload", "data", "body") and json_body is not None:
            arguments[name] = json_body
        elif json_body is not None and not arguments and parameter.kind in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.POSITIONAL_ONLY,
        ):
            arguments[name] = json_body
        elif name in query:
            arguments[name] = query[name]
        elif isinstance(parameter.default, Query):
            arguments[name] = parameter.default.default
        elif parameter.default is not inspect._empty:
            arguments[name] = parameter.default
        else:
            raise TypeError(f"Cannot resolve parameter '{name}' for endpoint {endpoint.__name__}")
    return endpoint(**arguments)


def _parse_query_string(query_string: str) -> Dict[str, str]:
    if not query_string:
        return {}
    pairs = [pair.split("=", 1) for pair in query_string.split("&") if pair]
    return {key: value for key, value in pairs if key}


__all__ = [
    "APIRouter",
    "FastAPI",
    "HTTPException",
    "Query",
]
