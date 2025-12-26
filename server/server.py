import socket, os, threading

CONTROL_PORT = 3456
BUF = 1024

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.join(BASE_DIR, "server_storage")
os.makedirs(ROOT_DIR, exist_ok=True)

def handle_client(ctrl, addr):
    print("Connected:", addr)
    ctrl.sendall(b"220 FTP Server Ready\n")

    current_dir = ROOT_DIR

    while True:
        cmdline = ctrl.recv(BUF).decode().strip()
        if not cmdline:
            break

        parts = cmdline.split()
        cmd = parts[0].upper()

        if cmd == "PWD":
            ctrl.sendall(f'257 "{current_dir}"\n'.encode())

        elif cmd == "CWD":
            new_dir = os.path.join(current_dir, " ".join(parts[1:]))
            if os.path.isdir(new_dir):
                current_dir = new_dir
                ctrl.sendall(f"250 Directory changed to {current_dir}\n".encode())
            else:
                ctrl.sendall(b"550 Directory not found\n")

        elif cmd == "LIST":
            listing = "\n".join(os.listdir(current_dir))

            data = socket.socket()
            data.bind(("", 0))
            data.listen(1)
            port = data.getsockname()[1]
            ctrl.sendall(f"150 {port}\n".encode())

            conn, _ = data.accept()
            conn.sendall(listing.encode())
            conn.close()
            data.close()
            ctrl.sendall(b"226 Listing complete\n")

        elif cmd == "RETR":
            filename = " ".join(parts[1:])
            path = os.path.join(current_dir, filename)

            if not os.path.exists(path):
                ctrl.sendall(b"550 File not found\n")
                continue

            data = socket.socket()
            data.bind(("", 0))
            data.listen(1)
            port = data.getsockname()[1]
            ctrl.sendall(f"150 {port}\n".encode())

            conn, _ = data.accept()
            with open(path, "rb") as f:
                while chunk := f.read(BUF):
                    conn.sendall(chunk)

            conn.close()
            data.close()
            ctrl.sendall(b"226 Download complete\n")

        elif cmd == "STOR":
            filename = os.path.basename(parts[1])
            save_path = os.path.join(current_dir, filename)

            data = socket.socket()
            data.bind(("", 0))
            data.listen(1)
            port = data.getsockname()[1]
            ctrl.sendall(f"150 {port}\n".encode())

            conn, _ = data.accept()
            with open(save_path, "wb") as f:
                while True:
                    chunk = conn.recv(BUF)
                    if not chunk:
                        break
                    f.write(chunk)

            conn.close()
            data.close()
            ctrl.sendall(b"226 Upload complete\n")

        elif cmd == "QUIT":
            ctrl.sendall(b"221 Goodbye\n")
            break

        else:
            ctrl.sendall(b"502 Command not implemented\n")

    ctrl.close()

def start():
    s = socket.socket()
    s.bind(("", CONTROL_PORT))
    s.listen(5)
    print("FTP Server running...")
    while True:
        c, a = s.accept()
        threading.Thread(target=handle_client, args=(c,a)).start()

start()
