import curses
import random

s = curses.initscr()
curses.curs_set(0)
sh, sw = s.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# initialize values
s_x = int(sw/4)
s_y = int(sh/2)
snake = [
    [s_y, s_x],
    [s_y, s_x-1],
    [s_y, s_x-2]
]
key = curses.KEY_RIGHT
play = True
points = 0
hunger = 0

apple = [int(sh/2), int(sw/2)]
w.addch(apple[0], apple[1], '@')

while play:
    if hunger == 111:
        play = False

    key_next = w.getch()
    key_prev = key
    key = key if key_next == -1 else key_next

    if (key == curses.KEY_LEFT and key_prev == curses.KEY_RIGHT) \
            or (key == curses.KEY_RIGHT and key_prev == curses.KEY_LEFT) \
            or (key == curses.KEY_DOWN and key_prev == curses.KEY_UP) \
            or (key == curses.KEY_UP and key_prev == curses.KEY_DOWN):
        key = key_prev

    if snake[0][0] in [0, sh - 1] or snake[0][1] in [0, sw - 1] or snake[0] in snake[1:]:
        play = False

    head_new = [
        snake[0][0],
        snake[0][1]
    ]

    if key == curses.KEY_RIGHT:
        head_new[1] += 1
    if key == curses.KEY_DOWN:
        head_new[0] += 1
    if key == curses.KEY_LEFT:
        head_new[1] -= 1
    if key == curses.KEY_UP:
        head_new[0] -= 1

    snake.insert(0, head_new)

    # comment this block to enable deadly borders
    if snake[0][0] == 0:
        snake[0][0] = sh - 2
    if snake[0][0] == sh - 1:
        snake[0][0] = 1
    if snake[0][1] == 0:
        snake[0][1] = sw - 2
    if snake[0][1] == sw - 1:
        snake[0][1] = 1

    if snake[0] == apple:
        points += 1
        hunger = 0
        apple = None
        while apple is None:
            apple_new = [random.randint(1, sh-2), random.randint(1, sw-2)]
            apple = apple_new if apple_new not in snake else None
        w.addch(apple[0], apple[1], '@')
    else:
        hunger += 1
        tail = snake.pop()
        w.addch(tail[0], tail[1], ' ')

    w.addch(snake[0][0], snake[0][1], '#')

key = 1
endMsg = "Apples eaten: " + str(points)
w.addstr(endMsg)
w.addstr("          Press spacebar to exit")
while key != 32:
    key = w.getch()
curses.endwin()
