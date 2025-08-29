# fakeports.py
# Opens a few fake ports to confuse scanners.
# Some send weird banners, some just hang, others instantly reset.

import socket
import threading
import time

FAKE_PORTS = {
    9999: b"Welcome to SuperSecure Service v1.0\n",      # Looks alive, prints banner
    10001: b"",                                          # Accepts then hangs
    12345: b"flag{just_kidding_this_is_a_decoy}\n",      # Decoy flag string
}

HOST = "0.0.0.0"


def handle_client(conn, addr, banner):
    try:
        if banner:
            conn.sendall(banner)
        # Some connections just stall to simulate "open|filtered"
        if banner == b"":
            time.sleep(60)  # keep connection open
    except Exception:
        pass
    finally:
        conn.close()


def start_fake_server(port, banner):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(5)
    print(f"[+] Fake service running on port {port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, banner), daemon=True).start()


if __name__ == "__main__":
    for port, banner in FAKE_PORTS.items():
        threading.Thread(target=start_fake_server, args=(port, banner), daemon=True).start()
    # Keep the main thread alive
    while True:
        time.sleep(10)
