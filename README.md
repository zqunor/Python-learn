# python 学习

- 开始日期: 2025.2.20 
- 教程：[菜鸟教程](https://www.runoob.com/python3/python3-socket.html) + deepseek + kimi

## 简单的聊天应用
- **功能描述**：实现一个基于 TCP 的多人聊天室，支持多个客户端连接和消息广播。
- **关键技术**：
 - 使用 `socket` 创建 TCP 服务器和客户端。
 - 使用 `select` 或 `threading` 处理多客户端连接。
 - 服务器广播消息给所有连接的客户端。

### 实现

[代码仓库-chatV1](https://github.com/zqunor/Python-learn/tree/chatV1/socket/chat)

#### 服务端代码

```python
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
```

#### 客户端代码

```python
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
            print(message)
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
```


### 实现效果
![图片](https://cdn.learnku.com/uploads/images/202502/20/33668/KSFnkaAlHk.png!large)


### 优化

#### 优化1: 记录客户端名

clients 需要从列表调整为字典

1. 列表和字典的使用区别

 操作 | 列表 | 字典
--- | --- | ---
定义 | clients=[] | clients = {} 
添加元素 | clients.append(client\_socket) | clients[username]=client_socket
循环遍历 | for client in clients: | for client in clients.values()
移除元素 | del clients[0] | del clients[username]

2. 接收客户端退出消息，并广播给其他用户

3. 实现效果
![图片](https://cdn.learnku.com/uploads/images/202502/20/33668/EJmlGpWIsi.png!large)

4. 代码

[代码仓库-chatV2](https://github.com/zqunor/Python-learn/tree/chatV2/socket/chat)

#### 优化2: 中断服务端进程时，自动关闭连接中的客户端，再关闭服务端进程

1. 捕获键盘Ctrl+C快捷键