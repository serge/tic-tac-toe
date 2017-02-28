#!/bin/python
import copy
from gui import start_gui

g_hash = {}
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

    def enum_pieces(self):
        for r in range(self.__side):
            for c in range(self.__side):
                cell = self.get(r, c)
                if not self.is_empty(cell):
                    yield r,c,cell

    def moves(self):
        for r in range(self.__side):
            for c in range(self.__side):
                if self.is_empty(self.get(r, c)):
                    newBoard = copy.deepcopy(self)
                    newBoard.put(r, c)
                    yield newBoard

    def get(self, r, c):
        return self.__board[self.__side * r + c]


    def put(self, r, c):
        self.__board[self.__side * r + c] = self.__next_piece
        self.__next_piece = {'o':'x','x':'o'}[self.__next_piece]

    def next_move(self):
        return self.__next_piece

    def just_moved(self):
        return {'o':'x','x':'o'}[self.__next_piece]

    def __eq__(self, other):
        return self.__board == other.__board

    def __hash__(self):
        return hash(self.__repr__())

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


def CalcScore(board, piece):
    res = board.check_if_won()
    if res == piece:
        return 1, board
    if res != None:
        return -1, board
    sscore = 0
    for b in board.moves():
        if not b in g_hash:
            score, br = CalcScore(b, piece)
            g_hash[b] = score
        sscore += g_hash[b]
    return sscore, board


class Game:

    def __init__(self):
        self.b = Board()

    def get_board(self):
        return self.b

    def reinit(self):
        g_hash = {}
        self.b = Board()

    def move(self):
        if len(g_hash) == 0:
            res = CalcScore(self.b, 'x')
        u = None
        for m in self.b.moves():
            if m.check_if_won() == 'x':
                u = 1, m
                break
            s = g_hash[m]
            skip = False
            for o in m.moves():
                if o.check_if_won() == 'o':
                    skip = True
                    break
            if skip:
                continue
            if u == None or u[0] < s:
                u = s,m
        u, new_board = u
        self.b = new_board
        if self.b.check_if_won() == m.just_moved():
            return False, 'You loose!'
        if self.b.is_full():
            return False, "Draw!"
        return True, 0

    def next_move(self, r, c):
        self.b.put(r, c)
        if self.b.check_if_won() == self.b.just_moved():
            return False, "You won!"
        if self.b.is_full():
            return False, "Draw!"
        return True, 0

if __name__ == '__main__':
    start_gui(Game())
