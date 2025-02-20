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

# 存储所有连接的客户端 (需要加索引对应客户端名字，此处需定义成字典)
clients = {}

def broadcast(message, sender):
    """广播消息给所有客户端"""
    for client_socket in clients.values():
        if client_socket != sender:
            try:
                client_socket.send(message.encode())
            except:
                remove_client(client_socket)

def remove_client(client_socket):
    """移除客户端"""
    for username, sock in clients.items():
        if sock == client_socket:
            del clients[username]
            break
    client_socket.close()
    print(f"客户端 {username} 退出聊天")

def handle_client(client_socket):
    """处理客户端连接"""
    
    # 版本2.要求客户端输入用户名
    client_socket.send("请输入您的用户名：".encode())
    username = client_socket.recv(1024).decode().strip()
    clients[username] = client_socket
    print(f"新用户 {username} 已连接。")

    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if message.lower() == 'exit':
                broadcast(f"{username} 已退出聊天室。", client_socket)
                remove_client(username)
                client_socket.close()
                break
            else:
                broadcast(f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"客户端 {username} 断开连接：{e}")
            remove_client(client_socket)
            break

def close_all_clients():
    """关闭所有客户端连接"""
    print("正在关闭所有客户端连接...")
    for username, sock in clients.items():
        del clients[username]
        sock.close()
        print(f"关闭 客户端 {username}")

    clients.clear()
    print("所有客户端连接已关闭。")

def main():
    """服务器主函数"""
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"新连接：{addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\n检测到 Ctrl+C, 正在关闭服务器...")
        close_all_clients()
        server_socket.close()
        print("服务器已关闭。")

if __name__ == "__main__":
    main()