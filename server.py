import socket
import threading

HOST = '127.0.0.1'
PORT = 4321
LISTENER_LIMIT = 5

active_clients = []

def send_message_to_all(message):
    for user in active_clients:
        try:
            user[1].sendall(message.encode())
        except:
            pass

def remove_client(username):
    for user in active_clients:
        if user[0] == username:
            active_clients.remove(user)
            break

def listen_for_message(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                break

            send_message_to_all(f"{username}~{message}")

        except:
            break

    client.close()
    remove_client(username)
    send_message_to_all(f"SERVER~{username} left the chat")
    print(f"{username} disconnected")

def client_handler(client):
    try:
        username = client.recv(2048).decode('utf-8')
        if not username:
            client.close()
            return

        active_clients.append((username, client))
        print(f"{username} joined")

        send_message_to_all(f"SERVER~{username} joined the chat")

        threading.Thread(
            target=listen_for_message,
            args=(client, username),
            daemon=True
        ).start()

    except:
        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(LISTENER_LIMIT)

    print(f"🚀 Server running at {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Connected: {address}")
        threading.Thread(
            target=client_handler,
            args=(client,),
            daemon=True
        ).start()

if __name__ == "__main__":
    main()
