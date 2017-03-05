from curses import wrapper, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, curs_set
import curses

def show_msg(stdscr, msg, c):
    tr, tc = 4, 4
    stdscr.move(tr, tc)
    stdscr.clrtoeol()
    stdscr.addstr(tr,tc, msg, curses.color_pair(c))


def main(stdscr, game):
    curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    while True:
        stdscr.clear()
        stdscr.addstr(2,4, "'q' - quit", curses.color_pair(3))
        show_msg(stdscr, "Would you like to go first? (space/yes, anything else/no)", 1)
        key = stdscr.getkey()
        if key == 'q':
            break
        if key != ' ':
            r, c = game.move()
            game.next_move(r, c, None)
        while True:
            b = game.get_board()
            r, c = input_coord(stdscr, b)
            if r == None:
                return
            if r == -1:
                msg = None
                break
            res, msg = game.next_move(r, c, "You win")
            draw_board(stdscr, b)
            if not res:
                break
            r, c = game.move()
            res, msg = game.next_move(r, c, "You loose")
            b = game.get_board()
            draw_board(stdscr, b)
            if not res:
                break
        if msg:
            show_msg(stdscr, msg + " Press any key", 2)
        stdscr.getkey()
        game.reinit()


    stdscr.refresh()


def board_to_screen(r, c):
    sr, sc = 10, 10
    dr, dc = 3, 3
    return r * dr + sr, c * dc + sc


def draw_key(scr, r, c):
    nr, nc = board_to_screen(r, c)
    scr.addstr(nr - 1, nc - 1, '+-+')
    scr.addstr(nr + 1, nc - 1, '+-+')
    scr.addch(nr, nc - 1, '|')
    scr.addch(nr, nc + 1, '|')

def input_coord(scr, board):
    c = r = 0
    while True:
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
        elif k == 'q' or k =="'":
            return None, None
        elif k == 'r':
            return -1, -1
        elif k == '\n':
            if board.is_empty(board.get(r, c)):
                show_msg(scr, "You move", 3)
                return r,c
            show_msg(scr, "You cannot make that move!", 5)
    return r,c


def draw_board(scr, board):
    r,c = board_to_screen(0, 0)
    mr,mc = board_to_screen(2, 2)
    for ir in range(r - 1, mr + 2):
        scr.move(ir, c - 1)
        scr.clrtoeol()
        scr.addch(ir, c - 2, '*')
        scr.addch(ir, mc + 2, '*')
    scr.addstr(r - 2, c - 2, '***********')
    scr.addstr(mr + 2, c - 2, '***********')
    for r,c,cell in board.enum_pieces():
        nr, nc = board_to_screen(r, c)
        if cell == 'x':
            scr.addstr(nr, nc, cell, curses.color_pair(4))
        else:
            scr.addstr(nr, nc, cell)

def start_gui(game):
    wrapper(main, game)
