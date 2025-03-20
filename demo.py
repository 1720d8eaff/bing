import random

width=21
height=21
maze = [[1 for _ in range(width)] for _ in range(height)]
locationX=1
locationY=0
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
maze[width-1][height-2] = "终"

userinput = input()
if userinput == "start":
    print("ok")
    for i in range(height):
            for j in range(width):
                print(maze[i][j], end=" ")
            print()
win=0
while(win != 1):
    Input=input()
    if Input == "info":
        print("ok",locationX, locationY, maze[locationX-1][locationY],maze[locationX+1][locationY],maze[locationX][locationY-1],maze[locationX][locationY+1])
    if Input == "target":
        print("ok",width-1,height-2)
    if Input == "move 1":
        locationX = locationX -1
        print("ok")
    if Input == "move 2":
        locationX = locationX +1
        print("ok")
    if Input == "move 3":
        locationY = locationY - 1
        print("ok")
    if Input == "move 4":
        locationY = locationY +1
        print("ok")
    if locationX == width-1 and locationY == height-2:
        win=1
        print("success")
    Input=" "