import socket

# 客户端设置
host = 'localhost'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# 接收服务器发送的迷宫信息
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

locationX = 1
locationY = 0
win = 0

while win != 1:
    command = input("请输入指令（info/target/move 1-4）：")
    client_socket.send(command.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8').strip()
    if response.startswith("ok"):
        if command == "info":
            parts = response.split()
            locationX = int(parts[2])
            locationY = int(parts[3])
            surroundings = list(map(int, parts[4:8]))
            print(f"位置：({locationX}, {locationY})，周围：上{surroundings[0]} 下{surroundings[1]} 左{surroundings[2]} 右{surroundings[3]}")
        elif command == "target":
            parts = response.split()
            targetX = int(parts[2])
            targetY = int(parts[3])
            print(f"目标位置：({targetX}, {targetY})")
        elif command.startswith("move "):
            print("移动成功")
    elif response == "success":
        print("恭喜！你到达了终点！")
        win = 1
    else:
        print(response)

client_socket.close()