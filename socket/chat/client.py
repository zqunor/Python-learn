import socket
import threading

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432

# 创建客户端套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("连接到服务器。输入 'exit' 退出聊天。")

def receive():
    """接收服务器消息"""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"收到消息：{message}")

        except:
            print("连接断开。")
            client_socket.close()
            break

def send():
    """发送消息到服务器"""
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode())

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    send_thread = threading.Thread(target=send)
    receive_thread.start()
    send_thread.start()