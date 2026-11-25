from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import sys
import threading
import webbrowser

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Quiet clean logging on stdout
        sys.stdout.write(f"[HTTP] {self.address_string()} - {format % args}\n")


def bind_server(handler, requested_port: int | None):
    candidates = []
    if requested_port is not None:
        candidates.append(requested_port)
    candidates.extend(range(8000, 8100))
    candidates.extend(range(8800, 8900))
    candidates.append(0)  # Let OS assign an unreserved ephemeral port as final fallback

    seen = set()
    for p in candidates:
        if p != 0 and p in seen:
            continue
        seen.add(p)
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", p), handler)
            return srv, srv.server_address[1]
        except OSError:
            continue
    raise OSError("Unable to bind any local HTTP port on 127.0.0.1")


def main():
    os.chdir(REPO_ROOT)
    args = sys.argv[1:]
    no_browser = "--no-browser" in args
    pos_ports = [int(a) for a in args if a.isdigit()]
    requested_port = pos_ports[0] if pos_ports else None

    handler = partial(NoCacheHandler, directory=REPO_ROOT)
    server, port = bind_server(handler, requested_port)

    url = f"http://127.0.0.1:{port}/"
    print(f"Serving '{REPO_ROOT}' at {url} (Ctrl+C to stop)", flush=True)

    if not no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped cleanly.")
        server.shutdown()


if __name__ == "__main__":
    main()
