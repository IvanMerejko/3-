from tkinter import *
import math
PIXEL_SIZE = 2
HEIGHT = 500
WIDTH = 800


def create_button(frame, name, callback, column_number):
    button = Button(frame, text=name, command=callback)
    button.grid(row=1, column=column_number)


class RasterizationAlgorithms:
    start_points = [[130, 170], [400, -70], [370, 280], [300, 370], [350, 200], [400, 180], [480, 180]]
    points = []
    scale = 1
    shiftY = 0
    shiftX = 0
    angle = 0
    d_angle = 0.1


    def factorial(self, n):
        return 1 if n <= 1 else n * self.factorial(n-1)

    def get_bezier_basic(self, i, n, t):
        return (self.factorial(n) / (self.factorial(i) * self.factorial(n-i))) * t**i * (1 - t) ** (n-i)

    def set_bezier_points(self, arr):
        t = 0
        step = 0.001
        self.points = []
        while t < step + 1:
            ind = len(self.points)
            self.points.append([0, 0])
            for i in range(0, len(arr)):
                b = self.get_bezier_basic(i, len(arr) - 1, t)
                self.points[ind][0] += arr[i][0] * b
                self.points[ind][1] += arr[i][1] * b
            t += step

    def clean(self):
        self.canvas.delete("bazier_line")

    def draw_bazier_line(self):
        self.clean()
        for point in self.points:
            self.canvas.create_rectangle( (point[0] + self.shiftX) * self.scale,
                                          (point[1] + self.shiftY) * self.scale,
                                          (point[0] + self.shiftY) * self.scale,
                                          (point[1] + self.shiftY) * self.scale,
                                          tag="bazier_line")

    def draw_simple_line(self):
        self.scale = 1
        self.shiftY = 0
        self.shiftX = 0
        self.angle = 0
        self.set_bezier_points(self.start_points)
        self.draw_bazier_line()

    def alienate(self):
        if self.scale > 0.1:
            self.scale -= 0.1
        self.angle = 0
        self.draw_bazier_line()

    def bring_closer(self):
        if self.scale < 2:
            self.scale += 0.1
        self.set_bezier_points(self.start_points)
        self.angle = 0
        self.draw_bazier_line()

    def mirror_by_x(self):
        self.set_bezier_points(self.start_points)
        self.angle = 0
        for point in self.points:
            point[1] = HEIGHT - point[1]
        self.draw_bazier_line()

    def mirror_by_y(self):
        self.set_bezier_points(self.start_points)
        self.angle = 0
        for point in self.points:
            point[0] = WIDTH - point[0]
        self.draw_bazier_line()

    def rotate_up(self):
        self.angle += 0.01
        self.rotate()

    def rotate_down(self):
        self.angle -= 0.01
        self.rotate()

    def rotate(self):
        self.set_bezier_points(self.start_points)
        for point in self.points:
            point[0] = point[0] * math.cos(self.angle) + point[1] * math.sin(self.angle)
            point[1] = point[1] * math.cos(self.angle) - point[0] * math.sin(self.angle)
        self.draw_bazier_line()

    def __init__(self):
        window = Tk()
        window.title("Lab1")
        # Place canvas in the window
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="light blue")
        self.canvas.pack()
        # Draw Frame in the window
        frame = Frame(window, bg="light blue")
        frame.pack()

        create_button(frame, "simple_line", self.draw_simple_line, 1)
        create_button(frame, "alienate", self.alienate, 2)
        create_button(frame, "bring_closer", self.bring_closer, 3)
        create_button(frame, "mirror_by_x", self.mirror_by_x, 4)
        create_button(frame, "mirror_by_y", self.mirror_by_y, 5)
        create_button(frame, "rotate_up", self.rotate_up, 6)
        create_button(frame, "rotate_down", self.rotate_down, 7)

        window.mainloop()



if __name__ == "__main__":
    RasterizationAlgorithms()