# TCP banner server
import socket

HOST = "0.0.0.0"
PORT = 1337  # TCP port

BANNER = (
    b"see /robots.txt\n"
    b"Connection closing...\n"
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))  # bind listening to any ip: 1337
    s.listen(5)

    while True:
        conn, addr = s.accept()      # blocks until a client connects
        with conn:
            try:
                conn.sendall(BANNER)  # send the banner/flag bytes

            except Exception as e:  # cannot send the bytes for some reason
                print(f"[!] Send error to {addr}: {e}")
