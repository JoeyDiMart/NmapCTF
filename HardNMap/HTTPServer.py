# HTTPServer.py
import http.server
import socketserver

PORT = 8080
FLAG_HEADER = "flag{nse_headers_ftw}"


class Handler(http.server.SimpleHTTPRequestHandler):
    # Make -sV/http-headers see this instead of "SimpleHTTP/0.6 Python/3.x"
    def version_string(self):
        return "uberhttpd/1.0"

    def _set_common_headers(self):
        self.send_header("X-CTF-Flag", FLAG_HEADER)
        self.send_header("Content-Type", "text/html; charset=utf-8")

    def do_HEAD(self):
        self.send_response(200)
        self._set_common_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/robots.txt":
            body = (
                "User-agent: *\n"
                "Disallow: /admin\n"
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        body = b"<h1>Welcome</h1><p>Nothing to see here.</p>"
        self.send_response(200)
        self._set_common_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP on {PORT}")
        httpd.serve_forever()
