from collections import deque


def bfs(maze, start, end):
    # 定义四个方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 获取迷宫的行数和列数
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0

    # 检查起点和终点是否合法
    if not (0 <= start[0] < rows and 0 <= start[1] < cols and maze[start[0]][start[1]] == 0):
        return []
    if not (0 <= end[0] < rows and 0 <= end[1] < cols and maze[end[0]][end[1]] == 0):
        return []

    # 记录每个节点的前驱节点，用于重建路径
    predecessor = [[None for _ in range(cols)] for _ in range(rows)]

    # 队列用于 BFS，存储节点的坐标
    queue = deque()
    queue.append(start)
    predecessor[start[0]][start[1]] = (-1, -1)  # 起点的前驱设为无效值

    while queue:
        current = queue.popleft()
        current_x, current_y = current

        # 如果到达终点，重建路径并返回
        if current == end:
            path = []
            while current != (-1, -1):
                path.append(current)
                current = predecessor[current[0]][current[1]]
            path.reverse()
            return path

        # 探索四个方向
        for dx, dy in directions:
            neighbor_x = current_x + dx
            neighbor_y = current_y + dy

            # 检查是否越界或遇到墙壁或已访问过
            if (0 <= neighbor_x < rows and 0 <= neighbor_y < cols and
                    maze[neighbor_x][neighbor_y] == 0 and
                    predecessor[neighbor_x][neighbor_y] is None):
                predecessor[neighbor_x][neighbor_y] = current
                queue.append((neighbor_x, neighbor_y))

    # 如果无法找到路径，返回空列表
    return []

import socket

# 客户端设置
host = 'localhost'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
data = client_socket.recv(1024).decode('utf-8').strip()
if data.startswith("ok"):
    maze_str = data[3:]
    maze = [list(map(str, row.split())) for row in maze_str.split('\n')]
    print("迷宫已加载：")
    for row in maze:
        print(' '.join(row))
else:
    print("连接失败")
    client_socket.close()
    exit()
# 示例迷宫（0 表示可通行，1 表示墙壁）

width = 21
height = 21
start = (1, 0)
end = (width-1, height-2)

path = bfs(maze, start, end)

# 打印路径
if path:
    print("找到路径：")
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if (row, col) == start:
                print("S", end=" ")
            elif (row, col) == end:
                print("E", end=" ")
            elif (row, col) in path:
                print("*", end=" ")
            elif maze[row][col] == 1:
                print("#", end=" ")
            else:
                print(" ", end=" ")
        print()
else:
    print("没有找到路径")