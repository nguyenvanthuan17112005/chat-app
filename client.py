import socket
import threading
import sys

# ================== CẤU HÌNH SERVER ==================
HOST = '127.0.0.1'   # Địa chỉ server (localhost)
PORT = 4321          # Cổng server


def listen_for_msg_from_server(client):
    """
    Luồng này CHỈ để lắng nghe tin nhắn từ server
    """
    while True:
        try:
            # Nhận dữ liệu từ server (tối đa 2048 bytes)
            message = client.recv(2048).decode('utf-8')

            # Nếu không nhận được dữ liệu → mất kết nối
            if not message:
                print("⚠️ Mất kết nối tới server")
                break

            # Tin nhắn có định dạng: username~nội_dung
            if "~" in message:
                username, content = message.split("~", 1)
                print(f"[{username}] {content}")
            else:
                print(message)

        except:
            print("❌ Lỗi khi nhận tin nhắn từ server")
            break

    # Đóng socket khi thoát vòng lặp
    client.close()
    sys.exit(0)


def send_message_to_server(client):
    """
    Luồng chính: gửi tin nhắn người dùng nhập lên server
    """
    while True:
        try:
            # 👉 Người dùng nhập nội dung chat
            message = input("💬 Nhập tin nhắn: ")

            if message:
                # Gửi tin nhắn lên server
                client.sendall(message.encode())
            else:
                print("⚠️ Tin nhắn không được để trống")

        except KeyboardInterrupt:
            # Người dùng nhấn Ctrl + C
            print("\n👋 Thoát khỏi phòng chat...")
            client.close()
            sys.exit(0)


def communicate_to_server(client):
    """
    Xử lý đăng nhập + khởi tạo luồng nghe tin nhắn
    """
    # 👉 Người dùng nhập tên
    username = input("👤 Nhập tên người dùng: ").strip()

    if not username:
        print("❌ Tên người dùng không được để trống")
        client.close()
        sys.exit(1)

    # Gửi username lên server
    client.sendall(username.encode())

    # Tạo thread để nghe tin nhắn từ server
    threading.Thread(
        target=listen_for_msg_from_server,
        args=(client,),
        daemon=True
    ).start()

    # Gửi tin nhắn
    send_message_to_server(client)


def main():
    # Tạo socket TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Kết nối tới server
        client.connect((HOST, PORT))
        print("✅ Đã kết nối tới server chat")
    except:
        print(f"❌ Không thể kết nối tới server {HOST}:{PORT}")
        sys.exit(1)

    communicate_to_server(client)


# Điểm bắt đầu chương trình
if __name__ == "__main__":
    main()
