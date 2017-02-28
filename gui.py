from curses import wrapper, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, curs_set
import curses

def main(stdscr, game):
    stdscr.clear()
    curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        while True:
            b = game.get_board()
            r, c = input_coord(stdscr, b)
            if r == None:
                return
            res, msg = game.next_move(r, c)
            if not res:
                break
            res, msg = game.move()
            b = game.get_board()
            draw_board(stdscr, b)
            if not res:
                break
        stdscr.addstr(40, 40, msg, curses.color_pair(1))
        stdscr.getkey()
        game.reinit()


    stdscr.refresh()


def board_to_screen(r, c):
    sr, sc = 10, 10
    dr, dc = 3, 3
    return r * dr + sr, c * dc + sc


def draw_key(scr, r, c):
    nr, nc = board_to_screen(r, c)
    scr.addstr(nr - 1, nc - 1, '***')
    scr.addstr(nr + 1, nc - 1, '***')
    scr.addch(nr, nc - 1, '*')
    scr.addch(nr, nc + 1, '*')

def input_coord(scr, board):
    k = 0
    c = 0
    r = 0
    while k != '\n':
        draw_board(scr, board)
        draw_key(scr, r, c)
        k = scr.getkey()
        if k == 'KEY_UP':
            r = max(0, r - 1)
        elif k == 'KEY_DOWN':
            r = min(2, r + 1)
        elif k == 'KEY_LEFT':
            c = max(0, c - 1)
        elif k == 'KEY_RIGHT':
            c = min(2, c + 1)
        elif k == 'q':
            return None, None
    return r,c


def draw_board(scr, board):
    r,c = board_to_screen(0, 0)
    mr,mc = board_to_screen(2, 2) 
    for ir in range(r - 1, mr + 2):
        scr.move(ir, c - 1)
        scr.clrtoeol()
        scr.addch(ir, c - 2, '|')
        scr.addch(ir, mc + 2, '|')
    scr.addstr(r - 2, c - 2, '*---------*')
    scr.addstr(mr + 2, c - 2, '*---------*')
    for r,c,cell in board.enum_pieces():
        nr, nc = board_to_screen(r, c)
        scr.addch(nr, nc, cell)

def start_gui(game):
    wrapper(main, game)
