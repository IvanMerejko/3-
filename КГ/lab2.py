from tkinter import *
PIXEL_SIZE = 2
HEIGHT = 500
WIDTH = 800


def create_button(frame, name, callback, column_number):
    button = Button(frame, text=name, command=callback)
    button.grid(row=1, column=column_number)


class RasterizationAlgorithms:
    start_points = [[30, 70], [300, -70], [270, 180], [200, 170], [250, 100], [300, 80], [380, 80]]
    points = []
    scale = 1
    shiftY = 0
    shiftX = 0


    def factorial(self, n):
        return 1 if n <= 1 else n * self.factorial(n-1)

    def get_bezier_basic(self, i, n, t):
        return (self.factorial(n) / (self.factorial(i) * self.factorial(n-i))) * t**i * (1 - t) ** (n-i)

    def set_bezier_points(self, arr):
        t = 0
        step = 0.001
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
        self.set_bezier_points(self.start_points)
        for point in self.points:
            self.canvas.create_rectangle( (point[0] + self.shiftX) * self.scale,
                                          (point[1] + self.shiftY) * self.scale,
                                          (point[0] + self.shiftY) * self.scale,
                                          (point[1] + self.shiftY) * self.scale,
                                          tag="bazier_line")

    def __init__(self):
        window = Tk()
        window.title("Lab1")
        # Place canvas in the window
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="light blue")
        self.canvas.pack()
        # Draw Frame in the window
        frame = Frame(window, bg="light blue")
        frame.pack()

        self.draw_bazier_line()

        window.mainloop()



if __name__ == "__main__":
    RasterizationAlgorithms()
