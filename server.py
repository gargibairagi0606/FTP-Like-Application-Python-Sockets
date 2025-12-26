import socket
import os
import threading

CONTROL_PORT = 3456
BUF_SIZE = 1024

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server_storage")
os.makedirs(BASE_DIR, exist_ok=True)

def handle_client(ctrl_sock, addr):
    print(f"[+] Client connected: {addr}")
    ctrl_sock.sendall(b"220 FTP Server Ready\n")

    current_dir = BASE_DIR

    while True:
        cmd_line = ctrl_sock.recv(BUF_SIZE).decode().strip()
        if not cmd_line:
            break

        parts = cmd_line.split()
        cmd = parts[0].upper()

        # PWD
        if cmd == "PWD":
            ctrl_sock.sendall(f'257 "{current_dir}"\n'.encode())

        # CWD
        elif cmd == "CWD":
            try:
                new_dir = os.path.join(current_dir, parts[1])
                if os.path.isdir(new_dir):
                    current_dir = new_dir
                    ctrl_sock.sendall(b"250 Directory changed\n")
                else:
                    ctrl_sock.sendall(b"550 Directory not found\n")
            except:
                ctrl_sock.sendall(b"501 Invalid directory\n")

        # LIST
        elif cmd == "LIST":
            data = "\n".join(os.listdir(current_dir))
            ctrl_sock.sendall(b"150 Opening data channel\n")

            data_sock = socket.socket()
            data_sock.bind(("", 0))
            data_sock.listen(1)
            port = data_sock.getsockname()[1]
            ctrl_sock.sendall(f"{port}\n".encode())

            conn, _ = data_sock.accept()
            conn.sendall(data.encode())
            conn.close()
            data_sock.close()
            ctrl_sock.sendall(b"226 Listing complete\n")

        # STOR
        elif cmd == "STOR":
            filename = parts[1]
            filepath = os.path.join(current_dir, filename)

            ctrl_sock.sendall(b"150 Opening data channel\n")
            data_sock = socket.socket()
            data_sock.bind(("", 0))
            data_sock.listen(1)
            port = data_sock.getsockname()[1]
            ctrl_sock.sendall(f"{port}\n".encode())

            conn, _ = data_sock.accept()
            with open(filepath, "wb") as f:
                while True:
                    chunk = conn.recv(BUF_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
            conn.close()
            data_sock.close()
            ctrl_sock.sendall(b"226 Upload complete\n")

        # RETR
        elif cmd == "RETR":
            filename = parts[1]
            filepath = os.path.join(current_dir, filename)

            if not os.path.exists(filepath):
                ctrl_sock.sendall(b"550 File not found\n")
                continue

            ctrl_sock.sendall(b"150 Opening data channel\n")
            data_sock = socket.socket()
            data_sock.bind(("", 0))
            data_sock.listen(1)
            port = data_sock.getsockname()[1]
            ctrl_sock.sendall(f"{port}\n".encode())

            conn, _ = data_sock.accept()
            with open(filepath, "rb") as f:
                while chunk := f.read(BUF_SIZE):
                    conn.sendall(chunk)
            conn.close()
            data_sock.close()
            ctrl_sock.sendall(b"226 Download complete\n")

        elif cmd == "QUIT":
            ctrl_sock.sendall(b"221 Goodbye\n")
            break

        else:
            ctrl_sock.sendall(b"502 Command not implemented\n")

    ctrl_sock.close()
    print(f"[-] Client disconnected: {addr}")

def start_server():
    sock = socket.socket()
    sock.bind(("", CONTROL_PORT))
    sock.listen(5)
    print(f"FTP Server running on port {CONTROL_PORT}")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()
