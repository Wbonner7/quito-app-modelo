from __future__ import annotations

import contextlib
import threading
import time
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from app.server import run as run_backend


class FrontendHandler(SimpleHTTPRequestHandler):
    """Serve os arquivos estáticos do painel web."""

    def __init__(self, *args, **kwargs):
        directory = kwargs.pop("directory", Path(__file__).parent / "frontend")
        super().__init__(*args, directory=directory, **kwargs)


def run_frontend(host: str = "127.0.0.1", port: int = 9000) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), FrontendHandler)
    print(f"Painel do Quito disponível em http://{host}:{port}")

    def serve() -> None:
        with contextlib.suppress(KeyboardInterrupt):
            server.serve_forever()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    return server


def main() -> None:
    print("Iniciando serviços do Quito...")
    backend_thread = threading.Thread(target=run_backend, kwargs={"host": "127.0.0.1", "port": 8000}, daemon=True)
    backend_thread.start()

    frontend_server = run_frontend()

    # Dar tempo para os servidores subirem antes de abrir o navegador.
    time.sleep(1.0)
    webbrowser.open("http://127.0.0.1:9000")

    print("Quito em execução. Pressione CTRL+C para encerrar.")
    try:
        while backend_thread.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Encerrando serviços...")
    finally:
        frontend_server.shutdown()


if __name__ == "__main__":
    main()
