import socket
import threading
import json
import base64
import os
import hashlib
import getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
HOST = "127.0.0.1"
PORT = 5000
# Both clients must use the same shared secret.
# This salt is a demo constant, not a unique salt for each user.
KDF_SALT = b"SyntecxhubWeek2ChatDemo"
def derive_key(secret):
    return hashlib.scrypt(
        secret.encode("utf-8"),
        salt=KDF_SALT,
        n=2**14,
        r=8,
        p=1,
        dklen=32
    )
def encrypt_message(name, message, key):
    nonce = os.urandom(12)
    plaintext = json.dumps({
        "name": name,
        "message": message
    }).encode("utf-8")
    ciphertext = AESGCM(key).encrypt(
        nonce, plaintext, None
    )
    return {
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii")
    }
def decrypt_message(packet, key):
    nonce = base64.b64decode(packet["nonce"], validate=True)
    ciphertext = base64.b64decode(
        packet["ciphertext"], validate=True
    )
    plaintext = AESGCM(key).decrypt(
        nonce, ciphertext, None
    )
    return json.loads(plaintext.decode("utf-8"))
def receive_messages(sock, key):
    buffer = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                print("\nDisconnected from server.")
                break
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line:
                    continue
                try:
                    packet = json.loads(line.decode("utf-8"))
                    message = decrypt_message(packet, key)
                    print(
                        f"\n{message['name']}: {message['message']}"
                    )
                    print("Message: ", end="", flush=True)
                except Exception:
                    print("\nCould not decrypt/verify a message.")
    except (ConnectionError, OSError):
        print("\nConnection closed.")
    finally:
        try:
            sock.close()
        except OSError:
            pass
def main():
    name = input("Enter your chat name: ").strip()
    if not name:
        print("Chat name cannot be empty.")
        return
    secret = getpass.getpass("Enter shared chat secret: ")
    if len(secret) < 12:
        print("Use a test secret of at least 12 characters.")
        return
    key = derive_key(secret)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        print("Connected! Type /quit to exit.")
        threading.Thread(
            target=receive_messages,
            args=(sock, key),
            daemon=True
        ).start()
        while True:
            message = input("Message: ")
            if message.strip().lower() == "/quit":
                break
            if not message:
                continue
            packet = encrypt_message(name, message, key)
            encoded = json.dumps(packet).encode("utf-8") + b"\n"
            sock.sendall(encoded)
    except (ConnectionError, OSError) as error:
        print("Connection error:", error)
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()
if __name__ == "__main__":
    main()