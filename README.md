# FTP-Like Application using Python Sockets

This project implements a simplified FTP-like client–server application using Python socket programming.
It demonstrates how real FTP works using separate control and data channels, persistent connections,
command interpretation, and directory-based file handling.

# Project Structure

```
FTP-Like-Application-Using-Python-Sockets/
│
├── client/
│   ├── client.py
│   └── client_files/
│
├── server/
│   ├── server.py
│   └── server_storage/
│
└── README.md
```

## Folder Purpose

| Folder | Used By | Purpose |
|-------|-------------|-------------|
| `client_files/` | Client |  Contains all files that the client uploads using STOR and where downloaded files are saved using RETR. |
| `server_storage/` | Server | Stores all files received from the client using STOR and provides files for download using RETR. |

Client and server never share the same folder, even if both run on the same machine.

## Objective

To understand how the FTP protocol works internally by building a client–server system that maintains
a persistent control connection and opens a new data channel for every file or directory transfer.

## Scope of the Experiment

- This project focuses on:
- Persistent TCP control connection
- Separate TCP data connections for each transfer
- FTP-style command parsing and responses
- Server-side directory handling
- File upload and download logic

Advanced features such as encryption, authentication security, and passive/active FTP modes
are intentionally excluded to keep the focus on core networking concepts.

## Commands Supported

| Command | Description |
|-------|-------------|
| `PWD` | Displays the current working directory on the server |
| `CWD folder` | Changes the working directory on the server |
| `LIST` | Lists all files in the current server directory |
| `STOR file` | Uploads file from client_files to server_storage |
| `RETR file` | Downloads file from server_storage to client_files |
| `QUIT` | Closes the FTP session |

## How STOR Works (Upload)
```
server/server_storage/file.txt
                │
                │ RETR file.txt
                ▼
client/client_files/file.txt
```
The client reads the file from client_files and the server stores a copy inside server_storage.

## How RETR Works (Download)
```
server/server_storage/file.txt
                │
                │ RETR file.txt
                ▼
client/client_files/file.txt
```
The server sends the file from server_storage and the client saves it inside client_files.

## How the Application Works

- Client connects to server using a persistent control connection.
- For every LIST, STOR, or RETR command:
- Server opens a temporary TCP data port.
- The port number is sent to the client.
- Client connects to that data port to transfer data.
- After the transfer, the data connection is closed.
- Control connection remains active until QUIT.

##  How to Run

**Step 1 — Start Server**
```
cd server
python server.py
```
**Step 2 — Start Client (new terminal)**
```
cd client
python client.py
```

## Example Output

1. Client connects to server on the control port.
2. Control channel remains open for entire session.
3. For `LIST`, `STOR`, or `RETR`, server opens a **new temporary data port**.
4. The data port number is sent back to the client.
5. Client connects to the data port for file transfer.
6. Data channel closes after each transfer.
7. Control channel remains active until `QUIT`.


## How to Run

### Step 1 — Start Server
```
python server.py
```
### Step 2 — Start Client (new terminal)
```
python client.py
```

## Example Output
```
ftp> pwd
257 "server/server_storage"

ftp> RETR sample_image.jpg
150 51045
226 Download complete

ftp> STOR upload_test.jpg
150 51049
226 Upload complete

ftp> CWD images
250 Directory changed to images

ftp> RETR demo_photo.jpg
150 51060
226 Download complete
```

## Key Concepts Demonstrated

- TCP socket programming
- Persistent control connections
- Dynamic data channel creation
- File system navigation
- FTP command-response workflow
- Directory handling
- Reliable file transfer    
