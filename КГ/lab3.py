from tkinter import *

PIXEL_SIZE = 2
HEIGHT = 400
WIDTH = 400
black_rbg = 123456
dots = []

window = Tk()
# Place canvas in the window
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()


def is_point_in_line(point, start_line, end_line):
    x, y = point[0], point[1]
    x0, y0 = start_line[0], start_line[1]
    x1, y1 = end_line[0], end_line[1]
    find_x = (int)((y - y0)*(x1 - x0) / (y1 - y0) + x0)
    return x == find_x and ( x0 < x < x1 or x1 < x < x0)


def find_left_barrier(x_help,y , start_line, end_line):
    x_left = x_help
    while x_help > 0:
        if is_point_in_line([x_help, y], start_line, end_line):
            x_left = x_help
        x_help -= 1
    return x_left


def find_right_barrier(x_help, y , start_line, end_line):
    x_right = x_help
    while x_help < WIDTH:
        if is_point_in_line([x_help, y], start_line, end_line):
            x_right = x_help
        x_help += 1
    return x_right




def fill_by_line(x, y):
    print(y)
    for i in range(0, len(dots) - 1):
        start_line = dots[i]
        if i == len(dots) - 1:
            end_line = dots[0]
        else:
            end_line = dots[i+1]
        x_help = x
        x_left = find_right_barrier(x_help, y, start_line, end_line)
        x_help = x
        x_right = find_left_barrier(x_help, y, start_line, end_line)
        if x_left > 0 and x_right < WIDTH:
            canvas.create_line(x_left, y, x_right, y, fill="black")




def create_one_line(x, y):
    dots_count = len(dots)
    if dots_count == 0:
        canvas.create_oval(x, y, x, y, width=0, fill="black")
    else:
        canvas.create_line(dots[dots_count-1][0], dots[dots_count-1][1], x, y, fill="black")

    dots.append([x, y])


def left_click(event):
    create_one_line(event.x, event.y)


def fill(event):
    fill_by_line(event.x, event.y)


def right_click(event):
    create_one_line(dots[0][0], dots[0][1])





window.bind('<Button-1>', left_click)
window.bind('<Button-2>', fill)
window.bind('<Button-3>', right_click)


window.mainloop()