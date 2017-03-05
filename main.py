#!/bin/python
import copy
from gui import start_gui

class CheckWinner:

    def __init__(self, board):
        self.piece = None
        self.won = False
        self.board = board

    def eval(self, r, c):
        cell = self.board.get(r, c)
        if self.board.is_empty(cell):
            self.won = False
            return False
        if self.piece == None:
            self.won = True
            self.piece = cell
            return True
        elif self.piece == cell:
            return True
        self.won = False
        return False


class Board:

    def __init__(self, *argv):
        self.__side = 3
        self.__board = [' '] * self.__side * self.__side
        self.__next_piece = 'o'

    def is_empty(self, piece):
        return piece == ' '

    def get(self, r, c):
        return self.__board[self.__side * r + c]


    def put(self, r, c):
        if not self.is_empty(self.get(r, c)):
            raise Exception("This cell is not empty")
        self.__board[self.__side * r + c] = self.__next_piece
        self.__next_piece = {'o':'x','x':'o'}[self.__next_piece]

    def get_moves(self):
        for r in range(self.__side):
            for c in range(self.__side):
                if self.is_empty(self.get(r, c)):
                    yield (r,c)

    def next_move(self):
        return self.__next_piece

    def check_if_won(self):
        for r in range(self.__side):
            checker = CheckWinner(self)
            for c in range(self.__side):
                if not checker.eval(r, c):
                    break
            if checker.won:
                return checker.piece
        for c in range(self.__side):
            checker = CheckWinner(self)
            for r in range(self.__side):
                if not checker.eval(r, c):
                    break
            if checker.won:
                return checker.piece
        checker = CheckWinner(self)
        for c in range(self.__side):
            if not checker.eval(c, c):
                break
        if checker.won:
            return checker.piece
        checker = CheckWinner(self)
        for c in range(self.__side):
            if not checker.eval(self.__side - c - 1, c):
                break
        if checker.won:
            return checker.piece

    def __repr__(self):
        v = ['---']
        for r in range(self.__side):
            v.append(''.join([self.get(r, c) for c in range(self.__side)]))
        return '\n'.join(v)

    def is_full(self):
        for cell in self.__board:
            if self.is_empty(cell):
                return False
        return True

    def enum_lines(self, pr, pc):
        p = []
        for r in range(self.__side):
            if r == pr:
                continue
            p.append((r, pc))
        yield p
        p = []
        for c in range(self.__side):
            if c == pc:
                continue
            p.append((pr, c))
        yield p
        if pr == pc:
            p = []
            for c in range(self.__side):
                if c == pc:
                    continue
                p.append((c, c))
            yield p
        if pr == self.__side - pc -1:
            p = []
            for c in range(self.__side):
                if c == pc:
                    continue
                p.append((self.__side - c - 1, c))
            yield p


def ScoreBoard(board, r, c, piece):
    totalDefense = totalOffence = 0
    for line in board.enum_lines(r, c):
        offence = defense = 0
        for (pr, pc) in line:
            cell = board.get(pr, pc)
            if cell == piece:
                offence += 2
            elif board.is_empty(cell):
                offence += 1
            else:
                defense += 1
        if offence == 4:
            return 100, 0
        if defense > 0:
            offence = 0;
        totalDefense += [0, 1, 10][defense] * defense
        totalOffence += offence
    return totalOffence, totalDefense


class Game:

    def __init__(self):
        self.b = Board()

    def get_board(self):
        return self.b

    def reinit(self):
        self.b = Board()

    def move(self):
        m = None
        piece = self.b.next_move()
        for (r, c) in self.b.get_moves():
            a = ScoreBoard(self.b, r, c, piece)
            offence, defense = a
            if offence >= 100: # we are about to we
                m = a, r, c
                break
            if m == None:
                m = a, r, c
                continue
            o, d = m[0]
            if defense >= 20: # that the way to go or we will loose
                m = a, r, c
            elif d < 20 and (offence > o or (offence == o and d < defense)):
                m = a, r, c
        return m[1:]

    def next_move(self, r, c, win_msg):
        piece = self.b.next_move()
        self.b.put(r, c)
        if self.b.check_if_won() == piece:
            return False, win_msg
        if self.b.is_full():
            return False, "Draw!"
        return True, 0

if __name__ == '__main__':
    start_gui(Game())
