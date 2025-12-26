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
│       ├── Text.txt
│       └── upload_test.jpg
│
├── server/
│   ├── server.py
│   └── server_storage/
│       └── sample_image.jpg
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

This project focuses on:
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
client/client_files/upload_test.jpg
            │
            │ STOR upload_test.jpg
            ▼
server/server_storage/upload_test.jpg
```

The client reads the file from client_files and uploads a copy to server_storage on the server.
The original file stays on the client.

## How RETR Works (Download)
```
server/server_storage/sample_image.jpg
                │
                │ RETR sample_image.jpg
                ▼
client/client_files/sample_image.jpg
```

- The server sends the file from server_storage.
- The client saves it inside client_files.

## How the Application Works

- Client connects to server using a persistent control connection.
- For every LIST, STOR, or RETR command:
  - Server opens a temporary TCP data port.
  - The port number is sent to the client.
  - Client connects to that data port to transfer data.
- After the transfer, the data connection is closed.
- Control connection remains active until QUIT.

## Sample Files

Client (`client_files/`)
- Text.txt
- upload_test.jpg

Server (`server_storage/`)
- sample_image.jpg

##  How to Run

**Step 1 — Start Server**
```bash
cd server
python server.py
```
**Step 2 — Start Client (new terminal)**
```bash
cd client
python client.py
```

## Example Output
```text
ftp> pwd
257 "server/server_storage"

ftp> RETR sample_image.jpg
150 Opening data port
226 Download complete

ftp> STOR upload_test.jpg
150 Opening data port
226 Upload complete

ftp> CWD images
250 Directory changed to images

ftp> RETR demo_photo.jpg
150 Opening data port
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
