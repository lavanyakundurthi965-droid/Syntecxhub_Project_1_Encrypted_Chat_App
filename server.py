import socket
import threading
import json
import logging
HOST = "127.0.0.1"
PORT = 5000
clients = []
clients_lock = threading.Lock()
logging.basicConfig(
    filename="chat_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def broadcast(data, sender):
    disconnected = []
    with clients_lock:
        recipients = list(clients)
    for client in recipients:
        try:
            client.sendall(data)
        except OSError:
            disconnected.append(client)
    for client in disconnected:
        remove_client(client)
def remove_client(client):
    with clients_lock:
        if client in clients:
            clients.remove(client)
    try:
        client.close()
    except OSError:
        pass
def handle_client(client, address):
    buffer = b""
    logging.info("Client connected: %s:%s", *address)
    try:
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line:
                    continue
                # Validate the JSON structure before forwarding.
                try:
                    packet = json.loads(line.decode("utf-8"))
                    if set(packet.keys()) != {"nonce", "ciphertext"}:
                        continue
                except (ValueError, UnicodeDecodeError):
                    logging.warning("Invalid packet received")
                    continue
                # Forward ciphertext only; do not decrypt messages here.
                broadcast(line + b"\n", client)
                logging.info("Encrypted message forwarded")
    except (ConnectionError, OSError) as error:
        logging.info("Client connection ended: %s", error)
    finally:
        remove_client(client)
        logging.info("Client disconnected: %s:%s", *address)
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Encrypted chat server running on {HOST}:{PORT}")
        print("Waiting for clients...")
        while True:
            client, address = server.accept()
            with clients_lock:
                clients.append(client)
            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server.close()
        with clients_lock:
            connected = list(clients)
        for client in connected:
            remove_client(client)
if __name__ == "__main__":
    main()
