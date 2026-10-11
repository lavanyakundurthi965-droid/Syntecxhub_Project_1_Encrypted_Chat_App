# Encrypted Chat App 🔐
## Syntecxhub Cybersecurity Internship — Week 2, Project 1
### Project Overview
The Encrypted Chat App is a Python-based client-server messaging application that uses TCP sockets for communication and AES-GCM authenticated encryption to protect messages during transmission.
The application supports multiple clients, encrypted message exchange, and server-side activity logging.
### Features
- Client-server communication using TCP sockets
- AES-GCM encryption and authenticated decryption
- Shared-secret-based encryption key derivation using scrypt
- Unique random nonce for each encrypted message
- Multiple simultaneous client connections using threads
- Encrypted message forwarding through the server
- Server activity logging
- Basic connection and error handling
### Technologies Used
- Python 3
- Socket Programming
- TCP/IP
- AES-GCM
- Scrypt Key Derivation
- Multithreading
- JSON
- Logging
### Project Structure
```text
Syntecxhub_Project_1_Encrypted_Chat_App/
├── server.py
├── client.py
├── README.md
└── chat_server.log
```
### Prerequisites
- Python 3 installed
- pip package manager
### Installation
Install the required library:
```bash
python -m pip install cryptography
```
### How to Run
**1. Start the server**
Open a terminal in the project folder:
```bash
python server.py
```
**2. Start the first client**
Open another terminal:
```bash
python client.py
```
Enter a chat name and a shared secret of at least 12 characters.
**3. Start another client**
Open a third terminal and run:
```bash
python client.py
```
Enter a different chat name and the same shared secret.
**4. Exchange messages**
Type a message in either client. The receiving client decrypts and displays the message.
Type `/quit` to exit a client. Press `Ctrl+C` to stop the server.
### Security Implementation
- Messages are encrypted with AES-GCM before transmission.
- A fresh, randomly generated 12-byte nonce is used for each encrypted message.
- The encryption key is derived from a shared secret using scrypt.
- The server forwards encrypted message packets without intentionally decrypting or logging message contents.
### Limitations
This project is an educational prototype and is not intended for production use.
- The demo uses a fixed key-derivation salt.
- The shared secret must be distributed securely outside the application.
- Forward secrecy, key rotation, and replay protection are not implemented.
- The default server address, `127.0.0.1`, allows testing on the same computer only.
### Ethical Use
This project is intended for educational and authorized cybersecurity testing.
### Author
Developed as part of the Syntecxhub Cybersecurity Internship.
