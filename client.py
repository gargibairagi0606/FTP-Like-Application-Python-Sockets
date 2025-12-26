import socket
BUF_SIZE = 1024
SERVER="127.0.0.1"
PORT=3456

def open_data(port):
    s=socket.socket()
    s.connect((SERVER,port))
    return s

sock=socket.socket()
sock.connect((SERVER,PORT))
print(sock.recv(1024).decode(),end="")

while True:
    cmd=input("ftp> ")
    sock.sendall(cmd.encode())
    resp=sock.recv(1024).decode()
    print(resp,end="")

    if resp.startswith("150"):
        port=int(resp.split()[-1])
        data=open_data(port)

        if cmd.startswith("STOR"):
            fname=cmd.split()[1]
            with open(fname,"rb") as f:
                while chunk:=f.read(BUF_SIZE):
                    data.sendall(chunk)

        elif cmd.startswith("RETR"):
            fname=cmd.split()[1]
            with open(fname,"wb") as f:
                while chunk:=data.recv(BUF_SIZE):
                    if not chunk: break
                    f.write(chunk)

        elif cmd=="LIST":
            print(data.recv(4096).decode())

        data.close()
        print(sock.recv(1024).decode(),end="")

    if cmd=="QUIT": break

sock.close()
