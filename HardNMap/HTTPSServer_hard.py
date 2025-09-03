# HTTPSserver_hard.py
import http.server
import socketserver
import ssl

PORT = 8443


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h2>Nothing here. Look deeper (cert?).</h2>")
        else:
            super().do_GET()


httpd = socketserver.TCPServer(("", PORT), Handler)
# Wrap with TLS using the self-signed cert we’ll generate at build time
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    server_side=True,
    certfile="/app/cert.pem",
    keyfile="/app/key.pem",
    ssl_version=ssl.PROTOCOL_TLS_SERVER,
)
print(f"HTTPS (hard flag) on {PORT}")
httpd.serve_forever()