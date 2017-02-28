#!/bin/python
import copy

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


def CalcScore(board, piece):
    res = board.check_if_won()
    if res == piece:
        return 100, board
    if res != None:
        return -100, board
    highest = (None, None)
    for b in board.moves():
        if not b in g_hash:
            board_score,temp = CalcScore(b, piece)
            g_hash[b] = board_score
        board_score = g_hash[b]
        score, rBoard = highest
        if score == None or score < board_score:
            highest = (board_score, b)
    score, rBoard = highest
    if score == None:
        rBoard = board
        score = 0
    return score - 1, rBoard


if __name__ == '__main__':
    b = Board()
    while True:
        res = CalcScore(b, 'o')
        b = res[1]
        print(b)
        r = int(input('input row:'))
        c = int(input('input col:'))
        b.put(r, c)
        print(b)
        if b.check_if_won() == 'x':
            break
