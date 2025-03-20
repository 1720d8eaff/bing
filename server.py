import socket
import random

# 迷宫生成逻辑
width = 21
height = 21
maze = [[1 for _ in range(width)] for _ in range(height)]
locationX = 1
locationY = 0

def dfs(x, y):
    maze[y][x] = 0  # 打通当前单元格
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)  # 随机打乱方向

    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2  # 下一个单元格
        if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0  # 打通中间的墙
            dfs(nx, ny)

dfs(1, 1)  # 从起点开始生成
maze[1][0] = "起"  # 起点
maze[width-1][height-2] = "终"  # 终点

# 服务器设置
host = 'localhost'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print("服务器已启动，等待客户端连接...")

client_socket, addr = server_socket.accept()
print(f"客户端 {addr} 已连接")

# 向客户端发送迷宫初始信息
maze_str = '\n'.join([' '.join(map(str, row)) for row in maze])
client_socket.send(f"ok\n{maze_str}".encode('utf-8'))

win = 0
while win != 1:
    # 接收客户端指令
    data = client_socket.recv(1024).decode('utf-8').strip()
    if not data:
        break

    response = "ok"
    if data == "info":
        # 发送当前位置和周围信息
        surroundings = [
            maze[locationY-1][locationX] if locationY-1 >= 0 else 1,
            maze[locationY+1][locationX] if locationY+1 < height else 1,
            maze[locationY][locationX-1] if locationX-1 >= 0 else 1,
            maze[locationY][locationX+1] if locationX+1 < width else 1
        ]
        response = f"ok {locationX} {locationY} {' '.join(map(str, surroundings))}"
    elif data == "target":
        # 发送目标位置
        response = f"ok {width-1} {height-2}"
    elif data.startswith("move "):
        # 处理移动指令
        direction = data.split()[1]
        if direction == "1" and locationY > 0 and maze[locationY-1][locationX] != 1:
            locationY -= 1
        elif direction == "2" and locationY < height-1 and maze[locationY+1][locationX] != 1:
            locationY += 1
        elif direction == "3" and locationX > 0 and maze[locationY][locationX-1] != 1:
            locationX -= 1
        elif direction == "4" and locationX < width-1 and maze[locationY][locationX+1] != 1:
            locationX += 1
        else:
            response = "error 无效的移动"
    else:
        response = "error 无效的指令"

    # 检查是否到达终点
    if locationX == width-1 and locationY == height-2:
        win = 1
        response = "success"

    # 发送响应
    client_socket.send(response.encode('utf-8'))

client_socket.close()
server_socket.close()
print("服务器已关闭")