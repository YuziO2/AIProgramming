#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-10-3 13:24
# @Author  : Zim
# @Site    :
# @File    : tmpPuzzle.py
# @Software: PyCharm
# 参考：https://mp.weixin.qq.com/s?__biz=MzA4Nzk0MjQ4NA==&mid=2651832327&idx=1&sn=ebdfdea3c46c4875b01ca9f1a9127832&chksm=8bcad43cbcbd5d2abe7b2bbcedc6b430eadad2949b7fcd9311a435859ff8b2eeaa094577039d&mpshare=1&scene=1&srcid=1002oSRDPlzP1iKjDVpxviCg&sharer_sharetime=1601680745526&sharer_shareid=f79652d3d635914fb4b18ede0397c9e9&key=892b62220735b7b9fc2c1877bb5cc0bf2e0081d50bd7752d76032b0eafba81508676acd33da7d31fb2edef0c1ad1bdf39a3af48c8919087b248bfe81249b20bc3323091e40619746506c4897f03d7569e1d212aa7a89c806f01dbe2449c722867f61f2475159e994ecc4868eeb991ec6b78fe3df652e006cf2194fdbc1ca4ec2&ascene=1&uin=MTM2MjM3NjkzNw%3D%3D&devicetype=Windows+7+x64&version=62090529&lang=zh_CN&exportkey=AwF7Nh%2BFI31v5V%2F6KbTz99w%3D&pass_ticket=jT2e%2BiPw3N%2Bn6YleMmgY8ar4aTAd07SHFJdtebNKaWb9crunKl319QtjoemEDt2r&wx_header=0
# bCut = 1  设置分割图片为3*3
# 增加循环移位功能： 设置： bCycle = 1; # 循环移位标志 added by zim
# 可进一步扩展为： nXn 而不强制n=3
# ----------------------------------------------------------------
# @Time    : 2022-9-13 13:24
# @Author  : Yuzi0201
# @Site    :
# @File    : tmpPuzzleWithAutoPlay.py
# @Software: VsCode


from multiprocessing.dummy import Array
from turtle import pos


if __name__ == "__main__":
    bCut = 0  # bCut = 1时  切割成3*3小图片。# 取图片区域(0, 0, 600, 600)

    if bCut == 1:
        import os
        from PIL import Image

        def splitimage(src, rownum, colnum, dstpath):
            img = Image.open(src)
            w, h = img.size
            if rownum <= h and colnum <= w:
                print('Original image info: %sx%s, %s, %s' %
                      (w, h, img.format, img.mode))
                print('开始处理图片切割, 请稍候...')

                s = os.path.split(src)
                if dstpath == '':
                    dstpath = s[0]
                fn = s[1].split('.')
                basename = fn[0]
                ext = fn[-1]

                num = 0
                rowheight = h // rownum
                colwidth = w // colnum
                for r in range(rownum):
                    for c in range(colnum):
                        box = (c * colwidth, r * rowheight, (c + 1)
                               * colwidth, (r + 1) * rowheight)
                        img.crop(box).save(os.path.join(
                            dstpath, basename + '_' + str(num) + '.' + ext))
                        num = num + 1

                print('图片切割完毕，共生成 %s 张小图片。' % num)
            else:
                print('不合法的行列切割参数！')

        def cropimage(src):
            img = Image.open(src)
            region = (0, 0, 600, 600)  # 取图片区域(0, 0, 600, 600)
            # 裁切图片
            cropImg = img.crop(region)
            # 保存裁切后的图片
            cropImg.save(src)

        # src = input('请输入图片文件路径：')
        src = "pic.png"
        if os.path.isfile(src):
            dstpath = input('请输入图片输出目录（不输入路径则表示使用源图片所在目录）：')

            if (dstpath == '') or os.path.exists(dstpath):
                cropimage(src)
                row = 3
                col = 3
                if row > 0 and col > 0:
                    splitimage(src, row, col, dstpath)
                else:
                    print('无效的行列切割参数！')
            else:
                print('图片输出目录 %s 不存在！' % dstpath)
        else:
            print('图片文件 %s 不存在！' % src)
        # exit(0);

    from tkinter import *
    from tkinter.messagebox import *
    import random

    root = Tk()
    root.title("拼图")
    # 载入外部图像
    Pics = []
    for i in range(9):
        filename = "pic_" + str(i) + ".png"
        Pics.append(PhotoImage(file=filename))
    # 定义常量
    # 画布的尺寸
    WIDTH = 600
    HEIGHT = 600
    # 图像块的边长
    IMAGE_WIDTH = WIDTH // 3
    IMAGE_HEIGHT = HEIGHT // 3

    # 棋盘行列数
    ROWS = 3
    COLS = 3
    # 移动步数
    steps = 0
    #  保存所有图像块的列表
    board = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]

    # 图像块类

    class Square:
        def __init__(self, orderID):
            self.orderID = orderID

        def draw(self, canvas, board_pos):
            img = Pics[self.orderID]
            canvas.create_image(board_pos, image=img)
            # 初始化拼图板

    primaryBoard = [[0 for i in range(ROWS)] for i in range(COLS)]
    finalBoard = [[0 for i in range(ROWS)] for i in range(COLS)]
    nonePos = [0, 0]

    def init_board():
        # 打乱图像块坐标
        L = list(range(8))
        L.append(None)
        random.shuffle(L)
        # 填充拼图板
        for i in range(ROWS):
            for j in range(COLS):
                idx = i * ROWS + j
                finalBoard[i][j] = idx
                orderID = L[idx]
                if orderID is None:
                    primaryBoard[i][j] = 8
                    # nonePos = [i, j]  错误写法，只改了指针指向，在函数外无效！
                    nonePos[0], nonePos[1] = i, j  # 正确写法
                    board[i][j] = None     # 为None时为空格
                else:
                    primaryBoard[i][j] = orderID
                    board[i][j] = Square(orderID)
                    # 重置游戏

    def play_game():
        global steps
        steps = 0
        init_board()

    # 绘制游戏界面各元素

    def drawBoard(canvas):
        # 画黑框
        canvas.create_polygon((0, 0, WIDTH, 0, WIDTH, HEIGHT,
                              0, HEIGHT), width=1, outline='Black', fill='Pink')
        # 画目标图像
        # canvas.draw_image(baymax, [WIDTH/2, WIDTH/2], [WIDTH, WIDTH], [50, WIDTH+50], [98, 98])
        # 画步数
        # canvas.draw_text("步数："+str(steps), [400, 680], 22, "White")
        # 画图像块
        # 代码写在这里
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] is not None:
                    board[i][j].draw(
                        canvas, (IMAGE_WIDTH * (j + 0.5), IMAGE_HEIGHT * (i + 0.5)))

    def mouseclick(pos):
        global steps
        # 将点击位置换算成拼图板上的坐标
        r = int(pos.y // IMAGE_HEIGHT)
        c = int(pos.x // IMAGE_WIDTH)
        print(r, c)
        bCycle = 1  # 循环移位标志 added by zim
        if bCycle == 0:  # 原始版本，没有循环移位
            if r < 3 and c < 3:  # 点击位置在拼图板内才移动图片
                if board[r][c] is None:  # 点到空位置上什么也不移动
                    return
                else:
                    # 依次检查当前图像块的上,下,左,右是否有空位置，如果有就移动当前图像块
                    current_square = board[r][c]
                    if r - 1 >= 0 and board[r - 1][c] is None:  # 判断上面
                        board[r][c] = None
                        board[r - 1][c] = current_square
                        steps += 1
                    elif c + 1 <= 2 and board[r][c + 1] is None:  # 判断右面
                        board[r][c] = None
                        board[r][c + 1] = current_square
                        steps += 1
                    elif r + 1 <= 2 and board[r + 1][c] is None:  # 判断下面
                        board[r][c] = None
                        board[r + 1][c] = current_square
                        steps += 1
                    elif c - 1 >= 0 and board[r][c - 1] is None:  # 判断左面
                        board[r][c] = None
                        board[r][c - 1] = current_square
                        steps += 1
                    # print(board)
                    label1["text"] = str(steps)
                    cv.delete('all')  # 清除canvas画布上的内容
                    drawBoard(cv)
        else:  # 循环移位版本
            if r < 3 and c < 3:  # 点击位置在拼图板内才移动图片
                if board[r][c] is None:  # 点到空位置上什么也不移动
                    return
                else:
                    # 依次检查当前图像块的上,下,左,右是否有空位置，如果有就移动当前图像块
                    current_square = board[r][c]
                    if r - 1 >= 0 and board[r - 1][c] is None:  # 判断上面
                        board[r][c] = None
                        board[r - 1][c] = current_square
                        steps += 1
                    elif c + 1 <= 2 and board[r][c + 1] is None:  # 判断右面
                        board[r][c] = None
                        board[r][c + 1] = current_square
                        steps += 1
                    elif r + 1 <= 2 and board[r + 1][c] is None:  # 判断下面
                        board[r][c] = None
                        board[r + 1][c] = current_square
                        steps += 1
                    elif c - 1 >= 0 and board[r][c - 1] is None:  # 判断左面
                        board[r][c] = None
                        board[r][c - 1] = current_square
                        steps += 1
                    # 循环移位，即类似贪食蛇可从最左边墙移动到最右边 by zim
                    elif r - 2 >= 0 and board[r - 2][c] is None:  # 判断最上面是否为空
                        board[r][c] = None
                        board[r - 2][c] = current_square
                        steps += 1
                    elif r + 2 <= 2 and board[r + 2][c] is None:  # 判断最下面是否为空
                        board[r][c] = None
                        board[r + 2][c] = current_square
                        steps += 1

                    elif c + 2 <= 2 and board[r][c + 2] is None:  # 判断最右面是否为空
                        board[r][c] = None
                        board[r][c + 2] = current_square
                        steps += 1
                    elif c - 2 >= 0 and board[r][c - 2] is None:  # 判断最左面是否为空
                        board[r][c] = None
                        board[r][c - 2] = current_square
                        steps += 1

                    # print(board)
                    label1["text"] = str(steps)
                    cv.delete('all')  # 清除canvas画布上的内容
                    drawBoard(cv)
        if win():
            showinfo(title="恭喜", message="你成功了！")

    def win():
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] is not None and board[i][j].orderID != i * ROWS + j:
                    return False
        return True

    def callBack2():
        print("重新开始")
        cv.bind("<Button-1>", mouseclick)
        play_game()
        label1["text"] = str(steps)
        cv.delete('all')  # 清除canvas画布上的内容
        drawBoard(cv)

    def autoClick(x, y):
        pos.y, pos.x = x*IMAGE_HEIGHT, y*IMAGE_WIDTH
        mouseclick(pos)

    def generateKey(board):  # 转矩阵为一串数字，记录是否访问过
        key = ''
        for i in range(ROWS):
            for j in range(COLS):
                key += str(board[i][j])
        return key

    class Status:
        status: Array
        route: Array  # 路径
        # 空白格位置
        x = 0  # 行
        y = 0  # 列

        def __init__(self, status, route, x, y):
            self.status, self.route, self.x, self.y = status, route, x, y

    def autoPlayBFS():
        import queue
        import copy
        restore()
        b2["text"] = "运算中，请稍后……"
        b1["state"] = DISABLED
        b2["state"] = DISABLED
        b3["state"] = DISABLED
        b4["state"] = DISABLED
        b5["state"] = DISABLED
        b6["state"] = DISABLED
        cv.unbind("<Button-1>")
        dictionary = {}  # 记录访问列表
        statusQueue = queue.Queue()
        statusQueue.put(Status(copy.deepcopy(primaryBoard),
                        [], nonePos[0], nonePos[1]))
        while not statusQueue.empty():
            front = statusQueue.get()
            if front.status == finalBoard:
                print("成功！")
                print("路径：", front.route)
                showinfo(title="计算完成", message="空白方块点击路径为：\n" +
                         str(front.route)+"\n步数为："+str(len(front.route)))
                b2["text"] = "演示中，请稍后……"
                import time
                for step in front.route:
                    autoClick(step[0], step[1])
                    time.sleep(1)
                b2["text"] = "自动游戏（BFS）"
                b1["state"] = NORMAL
                b2["state"] = NORMAL
                b3["state"] = NORMAL
                b4["state"] = NORMAL
                b5["state"] = NORMAL
                b6["state"] = NORMAL
                cv.bind("<Button-1>", mouseclick)
                return 0
            key = generateKey(front.status)
            dictionary[key] = 1
            for i in range(-(COLS-1), COLS):  # 左右->列
                if i == 0:
                    continue
                if front.y+i >= 0 and front.y+i <= COLS-1:  # 判断合法性
                    next = Status(copy.deepcopy(front.status),
                                  copy.deepcopy(front.route), 0, 0)
                    next.status[front.x][front.y +
                                         i], next.status[front.x][front.y] = next.status[front.x][front.y], next.status[front.x][front.y+i]
                    next.route.append([front.x, front.y+i])
                    next.x, next.y = front.x, front.y+i
                    key = generateKey(next.status)
                    print(key)
                    if key not in dictionary:
                        dictionary[key] = 1
                        statusQueue.put(next)
            for j in range(-(ROWS-1), ROWS):  # 上下->行
                if j == 0:
                    continue
                if front.x+j >= 0 and front.x+j <= ROWS-1:  # 判断合法性
                    next = Status(copy.deepcopy(front.status),
                                  copy.deepcopy(front.route), 0, 0)
                    next.status[front.x+j][front.y], next.status[front.x][front.y] = next.status[front.x][front.y], next.status[front.x+j][front.y]
                    next.route.append([front.x+j, front.y])
                    next.x, next.y = front.x+j, front.y
                    key = generateKey(next.status)
                    print(key)
                    if key not in dictionary:
                        dictionary[key] = 1
                        statusQueue.put(next)

    def autoPlayDFS():
        import copy
        restore()
        b3["text"] = "运算中，请稍后……"
        b1["state"] = DISABLED
        b2["state"] = DISABLED
        b3["state"] = DISABLED
        b4["state"] = DISABLED
        b5["state"] = DISABLED
        b6["state"] = DISABLED
        cv.unbind("<Button-1>")
        depthLimit = 20
        statusStack = []
        while depthLimit < 114:  # 最大深度
            statusStack.append(Status(copy.deepcopy(
                primaryBoard), [], nonePos[0], nonePos[1]))
            key = generateKey(primaryBoard)
            dictionary = {key: 0}  # value表示层数
            while len(statusStack):
                front = statusStack.pop()
                if front.status == finalBoard:
                    print("成功！")
                    print("路径：", front.route)
                    showinfo(title="计算完成", message="空白方块点击路径为：\n" +
                             str(front.route)+"\n最深层数为："+str(dictionary[generateKey(finalBoard)]))
                    b3["text"] = "演示中，请稍后……"
                    import time
                    for step in front.route:
                        autoClick(step[0], step[1])
                        time.sleep(1)
                    b3["text"] = "自动游戏（DFS）"
                    b1["state"] = NORMAL
                    b2["state"] = NORMAL
                    b3["state"] = NORMAL
                    b4["state"] = NORMAL
                    b5["state"] = NORMAL
                    b6["state"] = NORMAL
                    cv.bind("<Button-1>", mouseclick)
                    return 0
                key = generateKey(front.status)
                if dictionary[key] > depthLimit:  # 超限了
                    continue
                for i in range(-(COLS-1), COLS):  # 左右->列
                    if i == 0:
                        continue
                    if front.y+i >= 0 and front.y+i <= COLS-1:  # 判断合法性
                        next = Status(copy.deepcopy(front.status),
                                      copy.deepcopy(front.route), 0, 0)
                        next.status[front.x][front.y +
                                             i], next.status[front.x][front.y] = next.status[front.x][front.y], next.status[front.x][front.y+i]
                        next.route.append([front.x, front.y+i])
                        next.x, next.y = front.x, front.y+i
                        newkey = generateKey(next.status)
                        print(newkey)
                        if newkey not in dictionary:
                            dictionary[newkey] = dictionary[key]+1
                            statusStack.append(next)
                for j in range(-(ROWS-1), ROWS):  # 上下->行
                    if j == 0:
                        continue
                    if front.x+j >= 0 and front.x+j <= ROWS-1:  # 判断合法性
                        next = Status(copy.deepcopy(front.status),
                                      copy.deepcopy(front.route), 0, 0)
                        next.status[front.x+j][front.y], next.status[front.x][front.y] = next.status[front.x][front.y], next.status[front.x+j][front.y]
                        next.route.append([front.x+j, front.y])
                        next.x, next.y = front.x+j, front.y
                        newkey = generateKey(next.status)
                        print(newkey)
                        if newkey not in dictionary:
                            dictionary[newkey] = dictionary[key]+1
                            statusStack.append(next)
            depthLimit += 1  # 未找到，扩大界限

    def restore():
        for i in range(ROWS):
            for j in range(COLS):
                board[i][j] = Square(
                    primaryBoard[i][j]) if primaryBoard[i][j] != 8 else None
        cv.delete('all')  # 清除canvas画布上的内容
        global steps
        steps = 0
        label1["text"] = str(steps)
        drawBoard(cv)

    import threading

    def autoPlayBFSThread():
        t = threading.Thread(target=autoPlayBFS)  # 多线程，防止阻塞UI
        t.start()

    def autoPlayDFSThread():
        t = threading.Thread(target=autoPlayDFS)  # 多线程，防止阻塞UI
        t.start()

    # 设置窗口
    cv = Canvas(root, bg='green', width=WIDTH, height=HEIGHT)
    b1 = Button(root, text="重新生成", command=callBack2, width=10)
    b2 = Button(root, text="自动游戏（BFS）", command=autoPlayBFSThread, width=30)
    b3 = Button(root, text="自动游戏（DFS）", command=autoPlayDFSThread, width=30)
    b4 = Button(root, text="自动游戏（）", command=autoPlayBFSThread, width=30)
    b5 = Button(root, text="自动游戏（）", command=autoPlayBFSThread, width=30)
    b6 = Button(root, text="重置回初始（不重生成）", command=restore, width=30)
    label1 = Label(root, text="0", fg="red", width=20)
    label1.pack()
    cv.bind("<Button-1>", mouseclick)
    cv.find
    cv.pack()
    b1.pack()
    b2.pack()
    b3.pack()
    b6.pack()
    play_game()
    drawBoard(cv)
    root.mainloop()
