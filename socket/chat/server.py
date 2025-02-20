import socket
import threading

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432

# 创建服务器套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"服务器启动，监听地址：{HOST}:{PORT}")

# 存储所有连接的客户端
clients = []

def broadcast(message, sender):
    """广播消息给所有客户端"""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """处理客户端连接"""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"收到消息：{message.decode()}")
                broadcast(message, client_socket)
        except Exception as e:
            print(f"客户端断开连接：{e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def main():
    """服务器主函数"""
    while True:
        client_socket, addr = server_socket.accept()
        print(f"新连接：{addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()