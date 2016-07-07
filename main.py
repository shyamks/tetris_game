from random import randrange as rand
import os
from copy import deepcopy

rows = 21
cols = 22
WALL = 10
SPACE = 0

tetris_shapes = [
    [[1, 1, 1, 1],
     ],

    [[2, 0],
     [2, 0],
     [2, 2]],

    [[0, 3],
     [0, 3],
     [3, 3]],

    [[0, 4],
     [4, 4],
     [4, 0]],

    [[5, 5],
     [5, 5]],
]


class Tetris:
    def __init__(self):
        temp = []
        for j in range(rows - 1):
            temp1 = []
            for i in range(cols):
                if i == 0 or i == cols - 1:
                    temp1.append(WALL)
                else:
                    temp1.append(SPACE)
            temp.append(temp1)
        temp1 = []
        for i in range(cols):
            temp1.append(WALL)
        temp.append(temp1)
        self.arr = temp
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_pos_y = rand(len(range(1, cols - 1 - (len(self.next_stone[0]) - 1))))
        self.stone_pos_x = 0
        self.game_status_finish = False

        # self.piece

    def counter_clockwise(self, stone):
        rotated = zip(*stone)[::-1]
        return rotated

    def clockwise(self, stone):
        rotated = zip(*stone[::-1])
        return rotated

    def display_mat(self, array):
        fin = []
        temp = []
        for row in array:
            temp = []
            for unit in row:
                if unit == SPACE:
                    temp.append(" ")
                else:
                    temp.append("*")
            fin.append(temp)
        for row in fin:
            print (''.join(row))

    def setState(self, stone, x, y):
        self.next_stone = stone
        self.stone_pos_x = x
        self.stone_pos_y = y

    def new_stone(self, board):
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_pos_y = rand(len(range(1, cols - 1 - (len(self.next_stone[0])))))
        self.stone_pos_x = 0
        if self.check_collision(board, self.stone_pos_x, self.stone_pos_y, self.next_stone):
            self.game_status_finish = True

    def check_collision(self, board, sx, sy, stone):
        for x, row in enumerate(stone):
            for y, unit in enumerate(row):
                if unit != SPACE:
                    if board[sx + x][sy + y] != SPACE:
                        return True
        return False

    def validate(self, button):
        if button == 'a':
            return 'MOVE_LEFT'
        elif button == 'd':
            return 'MOVE_RIGHT'
        elif button == 'w':
            return 'COUNTER_CLOCKWISE'
        elif button == 's':
            return 'CLOCKWISE'
        return False

    def update_board(self, sx, sy, stone, board):
        for x, row in enumerate(board):
            for y, unit in enumerate(row):
                if board[x][y] != SPACE and board[x][y] != WALL:
                    board[x][y] = SPACE
        for x, row in enumerate(stone):
            for y, unit in enumerate(row):
                if board[sx + x][sy + y] == SPACE:
                    board[sx + x][sy + y] = stone[x][y]
                else:
                    board[sx + x][sy + y] = WALL
        return (sy, board)

    def stone_board(self, board):
        for x, row in enumerate(board):
            for y, unit in enumerate(row):
                if board[x][y] != SPACE and board[x][y] != WALL:
                    self.arr[x][y] = WALL
                    board[x][y] = WALL

    #zip(*original)[::-1]
    def turn(self,clock = False,antiClock= False):
        board = deepcopy(self.arr)
        stone = deepcopy(self.next_stone)
        sx = self.stone_pos_x
        sy = self.stone_pos_y
        flag = 0
        flag1 = 0
        f1 = 0
        if clock:
            stone_chg = zip(*stone[::-1])
        else:
            stone_chg = zip(*stone)[::-1]

        tempboard = deepcopy(board)
        board = self.clear(board)
        for x, row in enumerate(stone_chg):
            for y, unit in enumerate(row):
                if stone_chg[x][y] != SPACE:
                    if board[sx + x + 1][sy + y] != SPACE:
                        flag = 1

        if flag == 1:  # cannot perfrom the given action specifically
            # if cant move down
            board = deepcopy(tempboard)
            for x, row in enumerate(stone):
                for y, unit in enumerate(row):
                    if stone[x][y] != SPACE:
                        if board[sx + x + 1][sy + y] == WALL:
                            print ('New stone !')
                            self.stone_board(board)
                            self.new_stone(board)
                            f1 = 1
                            break
                if f1 == 1:
                    break
            # come down if not possible to move
            if f1 != 1:
                self.stone_pos_x += 1
                sx = self.stone_pos_x
                (self.stone_pos_y, self.arr) = self.update_board(sx, sy, stone, board)

        else:
            self.stone_pos_x += 1
            sx = self.stone_pos_x
            (self.stone_pos_y, self.arr) = self.update_board(sx, sy , stone_chg, board)
            return stone_chg

        return stone

    def clear(self,board):
        for x, row in enumerate(board):
            for y, unit in enumerate(row):
                if board[x][y] != SPACE and board[x][y] != WALL:
                    board[x][y] = SPACE
        return board

    def move(self, pos):
        board = deepcopy(self.arr)
        stone = deepcopy(self.next_stone)
        sx = self.stone_pos_x
        sy = self.stone_pos_y
        flag = 0
        flag1 = 0
        f1 = 0
        tempboard = deepcopy(board)
        board = self.clear(board)
        for x, row in enumerate(stone):
            for y, unit in enumerate(row):
                if stone[x][y] != SPACE:
                    if board[sx + x + 1][sy + y + pos] != SPACE:
                        flag = 1

        if flag == 1:  # cannot perfrom the given action specifically
            # if cant move down
            board = deepcopy(tempboard)
            for x, row in enumerate(stone):
                for y, unit in enumerate(row):
                    if stone[x][y] != SPACE:
                        if board[sx + x + 1][sy + y] == WALL:
                            print ('New stone !')
                            self.stone_board(board)
                            self.new_stone(board)
                            f1 = 1
                            break
                if f1 == 1:
                    break
            # come down if not possible to move
            if f1 != 1:
                self.stone_pos_x += 1
                sx = self.stone_pos_x
                (self.stone_pos_y, self.arr) = self.update_board(sx, sy, stone, board)

        else:
            self.stone_pos_x += 1
            sx = self.stone_pos_x
            (self.stone_pos_y, self.arr) = self.update_board(sx, sy + pos, stone, board)

    def run_game(self):
        self.keys = {
            'MOVE_LEFT': -1,
            'MOVE_RIGHT': +1,
            # 'CLOCKWISE': 2,
            # 'COUNTER_CLOCKWISE': 3,
        }
        while self.game_status_finish is False:
            (self.stone_pos_y, self.arr) = self.update_board(self.stone_pos_x, self.stone_pos_y, self.next_stone,
                                                             self.arr)
            self.display_mat(self.arr)
            button = raw_input("Press key:")
            while self.validate(button) is False:
                button = raw_input("Press key:")
            p = self.keys[self.validate(button)]
            if p == 1 or p == -1:
                self.move(p)
            elif p == 2:
                self.next_stone = self.turn(clock=True)
            else:
                self.next_stone = self.turn(clock=False)

                # should clear screen here
        print ("GAME OVER ! Thank you for playing !")


if __name__ == '__main__':
    obj = Tetris()
    obj.run_game()
    # (obj.display_mat(obj.clockwise(tetris_shapes[0])))
    # obj.display_mat(tetris_shapes[0])
    # (obj.display_mat(obj.counter_clockwise(tetris_shapes[0])))
