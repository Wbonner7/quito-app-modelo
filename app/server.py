from __future__ import annotations

from wsgiref.simple_server import make_server

from app.main import app


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    with make_server(host, port, app) as server:
        print(f"Servidor do Quito disponível em http://{host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    run()
