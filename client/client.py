import socket, os

SERVER = "127.0.0.1"
PORT = 3456
BUF = 1024

BASE = os.path.dirname(__file__)
CLIENT_FILES = os.path.join(BASE, "client_files")
os.makedirs(CLIENT_FILES, exist_ok=True)

def open_data(port):
    s = socket.socket()
    s.connect((SERVER, port))
    return s

sock = socket.socket()
sock.connect((SERVER, PORT))
print(sock.recv(1024).decode(), end="")

while True:
    cmd = input("ftp> ")
    sock.sendall(cmd.encode())

    resp = sock.recv(1024).decode()
    print(resp, end="")

    if resp.startswith("150"):
        port = int(resp.split()[-1])
        data = open_data(port)

        if cmd.upper().startswith("STOR"):
            fname = cmd.split()[1]
            path = os.path.join(CLIENT_FILES, fname)
            with open(path, "rb") as f:
                while chunk := f.read(BUF):
                    data.sendall(chunk)

        elif cmd.upper().startswith("RETR"):
            fname = cmd.split()[1]
            path = os.path.join(CLIENT_FILES, fname)
            with open(path, "wb") as f:
                while chunk := data.recv(BUF):
                    if not chunk:
                        break
                    f.write(chunk)

        elif cmd.upper() == "LIST":
            print(data.recv(4096).decode())

        data.close()
        print(sock.recv(1024).decode(), end="")

    if cmd.upper() == "QUIT":
        break

sock.close()
