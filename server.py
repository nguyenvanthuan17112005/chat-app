import socket
import threading

# ================== CẤU HÌNH SERVER ==================
HOST = '127.0.0.1'
PORT = 4321
LISTENER_LIMIT = 5  # Số client tối đa chờ kết nối

# Danh sách client đang hoạt động: [(username, socket)]
active_clients = []


def send_message_to_all(message):
    """
    Gửi tin nhắn tới TẤT CẢ client đang kết nối
    """
    for user in active_clients:
        try:
            user[1].sendall(message.encode())
        except:
            pass


def remove_client(username):
    """
    Xoá client khỏi danh sách khi ngắt kết nối
    """
    for user in active_clients:
        if user[0] == username:
            active_clients.remove(user)
            break


def listen_for_message(client, username):
    """
    Lắng nghe tin nhắn từ MỘT client
    """
    while True:
        try:
            message = client.recv(2048).decode('utf-8')

            # Client ngắt kết nối
            if not message:
                break

            # Gộp username + nội dung
            final_msg = f"{username}~{message}"

            # Gửi cho tất cả client
            send_message_to_all(final_msg)

        except:
            break

    # Đóng kết nối
    client.close()
    remove_client(username)

    # Thông báo rời phòng
    send_message_to_all(f"SERVER~{username} đã rời phòng chat")
    print(f"{username} disconnected")


def client_handler(client):
    """
    Xử lý một client mới kết nối
    """
    try:
        # Nhận username từ client
        username = client.recv(2048).decode('utf-8')

        if not username:
            client.close()
            return

        # Thêm client vào danh sách
        active_clients.append((username, client))
        print(f"{username} đã tham gia phòng chat")

        # Thông báo cho mọi người
        send_message_to_all(f"SERVER~{username} đã tham gia phòng chat")

        # Tạo thread lắng nghe tin nhắn của client
        threading.Thread(
            target=listen_for_message,
            args=(client, username),
            daemon=True
        ).start()

    except:
        client.close()


def main():
    # Tạo socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Gán địa chỉ và cổng
    server.bind((HOST, PORT))
    server.listen(LISTENER_LIMIT)

    print(f"🚀 Server đang chạy tại {HOST}:{PORT}")

    while True:
        # Chấp nhận client kết nối
        client, address = server.accept()
        print(f"🔌 Client kết nối từ {address[0]}:{address[1]}")

        threading.Thread(
            target=client_handler,
            args=(client,),
            daemon=True
        ).start()


# Điểm bắt đầu server
if __name__ == "__main__":
    main()
