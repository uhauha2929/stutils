import random
import numpy as np


class Grid(object):

    def __init__(self, size: int=4, max_score: int=2048):
        self.size = size
        self.max_score = max_score
        self.cell_size = len(str(self.max_score)) + 1
        self.is_over = False
        self.winning = False
        self.total_score = 0

        self.cells = np.zeros((size, size), dtype=int)
        for _ in range(2):
            pos = random.randint(0, self.size**2 - 1)
            i, j = int(pos / self.size), pos % self.size
            self.cells[i][j] = random.choice((2, 4))


    def show(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                print(('{:<'+str(self.cell_size)+'d}').format(self.cells[i][j]), end='')
            print()


    def move_left(self):
        # 网格是否有非0数字移动
        moved = False
        # 随机数字0的位置
        m, n = -1, -1
        # 数字0的个数
        c = 0
        for i, line in enumerate(self.cells):
            j  = 0
            k = 1
            while k < len(line):
                while k < len(line) and line[k] == 0:
                    k += 1  
                if k == len(line):
                    break
                if line[j] == line[k]:
                    line[j] *= 2
                    moved = True
                    self.total_score += line[j]
                    if line[j] == self.max_score:
                        self.winning = True
                    j += 1
                    line[j] = 0  # 下一次不再求和
                else:
                    if line[j] != 0:
                        j += 1
                    if j != k:
                        line[j] = line[k]
                        moved = True
                k += 1
            if line[j] != 0:
                j += 1
            # 每行剩余部分置为0
            while j < len(line):
                c += 1
                # 同时保存一个随机0的位置
                if random.randint(1, c) <= 1:
                    m, n = i, j
                line[j] = 0
                j += 1
        # 只有网格发生移动，才会随机选择数字0替换为2或4
        if moved:
            self.cells[m][n] = random.choice((2, 4))
            # 只有一个数字0，被替换后网格满了，如果再也不能移动则游戏结束
            if c <= 1:
                # 按行检查是否有相邻重复数字
                for i in range(self.size):
                    for j in range(self.size - 1):
                        if self.cells[i][j] == self.cells[i][j + 1]:
                            return
                # 按列检查是否有相邻重复数字
                for j in range(self.size):
                    for i in range(self.size - 1):
                        if self.cells[i][j] == self.cells[i + 1][j]:
                            return

                self.is_over = True

    # 为了节省代码对原矩阵进行翻转或旋转，全部转换成向左移动
    def move_right(self):
        self.cells = np.flip(self.cells, 1)
        self.move_left()
        self.cells = np.flip(self.cells, 1)
        
    def move_up(self):
        self.cells = np.rot90(self.cells, 1)
        self.move_left()
        self.cells = np.rot90(self.cells, -1)

    def move_down(self):
        self.cells = np.rot90(self.cells, -1)
        self.move_left()
        self.cells = np.rot90(self.cells, 1)


def run():
    grid = Grid()
    grid.show()
    while (True):
        d = input('Enter WASD to move (Q to quit): ')
        if d.upper() == 'W':
            grid.move_up()
        elif d.upper() == 'S':
            grid.move_down()
        elif d.upper() == 'A':
            grid.move_left()
        elif d.upper() == 'D':
            grid.move_right()
        elif d.upper() == 'Q':
            break
        else:
            print('Invalid key!')
            continue
        print('Total score: ', grid.total_score)
        grid.show()
        if grid.winning:
            print('Congratulations! You did it!')
            break
        if grid.is_over:
            print('Game over!!!')
            break

if __name__ == '__main__':
    run()
