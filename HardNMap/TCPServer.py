# TCPServer.py
import socket, threading

HOST, PORT = "0.0.0.0", 2222
BANNER = b"SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.2 flag{service_detected}\r\n"


def client(conn, addr):
    try:
        conn.sendall(BANNER)
    finally:
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT));
    s.listen(5)
    print(f"Banner TCP on {PORT}")
    while True:
        c, a = s.accept()
        threading.Thread(target=client, args=(c, a), daemon=True).start()
