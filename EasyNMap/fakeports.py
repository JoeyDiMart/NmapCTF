# /app/fakeports.py
import os
import socket
import threading
import random

ACTIVE_PORTS = {80, 1337}  # container ports already in use by your real services

# default visible decoys if env not provided
DEFAULT_FAKE_PORTS = [21, 25, 3306, 5000, 7000]

FAKE_BANNERS_BY_PORT = {
    21:   b"220 (vsFTPd 2.3.4)\r\n",
    25:   b"220 mail.example.com ESMTP Postfix\r\n",
    3306: b"5.5.5-10.1.48-MariaDB-1~bionic\r\n",
    5000: b"HTTP/1.1 403 Forbidden\r\n\r\n",
    7000: b"RTSP/1.0 403 Forbidden\r\n\r\n",
}

RANDOM_BANNERS = [
    b"220 (vsFTPd 3.0.3)\r\n",
    b"220 mail.example.com ESMTP Exim 4.94\r\n",
    b"10.3.29-MariaDB-1:10.3.29+maria~bionic\r\n",
    b"HTTP/1.1 400 Bad Request\r\n\r\n",
    b"RTSP/1.0 404 Not Found\r\n\r\n",
]

def parse_fake_ports():
    env = os.getenv("FAKE_PORTS", "")
    ports = []
    if env.strip():
        for p in env.split(","):
            p = p.strip()
            if p.isdigit():
                ports.append(int(p))
    if not ports:
        ports = DEFAULT_FAKE_PORTS
    # avoid collisions inside container
    ports = [p for p in ports if p not in ACTIVE_PORTS]
    return sorted(set(ports))

def banner_for(port: int) -> bytes:
    return FAKE_BANNERS_BY_PORT.get(port, random.choice(RANDOM_BANNERS))

def fake_listener(port, banner):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        print(f"[*] Fake service listening on {port}", flush=True)
        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    conn.sendall(banner)
                except Exception as e:
                    print(f"[!] Error on {port} -> {addr}: {e}", flush=True)

if __name__ == "__main__":
    fake_ports = parse_fake_ports()
    print(f"[+] Fake ports: {fake_ports}", flush=True)
    for p in fake_ports:
        t = threading.Thread(target=fake_listener, args=(p, banner_for(p)), daemon=True)
        t.start()
    # keep alive
    threading.Event().wait()
