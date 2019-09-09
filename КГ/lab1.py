# Import all definitions from tkinter

from tkinter import *
import time

PIXEL_SIZE = 5
HEIGHT = 500
WIDTH = 800

def create_button(frame , name , callback, column_number):
    button = Button(frame, text=name, command=callback)
    button.grid(row=1, column=column_number)

class RasterizationAlgorithms:
    surname = {
        "M": [[(10, 30), (15, 10)], [(15, 10), (20, 30)], [(20, 30), (25, 10)], [(25, 10), (30, 30)]],
        "E1": [[(35, 10), (35, 30)], [(35, 30), (40, 30)], [(35, 20), (40, 20)], [(35, 10), (40, 10)]],
        "r": [[(45, 10), (45, 30)], [(45, 20), (53, 10)]],
        "E2": [[(58, 10), (58, 30)], [(58, 30), (63, 30)], [(58, 20), (63, 20)], [(58, 10), (63, 10)]],
        "z": [[(68, 10), (78, 10)], [(68, 30), (78, 30)], [(68, 30), (78, 10)]],
        "h": [[(83, 10), (83, 30)], [(83, 23), (90, 23)], [(90, 23), (90, 30)]],
        "k": [[(95, 10), (95, 30)], [(95, 20), (103, 10)], [(98, 17), (103, 30)]],
        "o": [[(115, 20), (10, 0)]],
    }

    def DDA(self, x1, y1, x2, y2):
        dx, dy = abs(x2 - x1), abs(y2 - y1)

        steps = dx if dx >= dy else dy
        dx, dy= (x2 - x1) / steps, (y2 - y1) / steps

        x, y = x1, y1
        points = [[x, y], [x2, y2]]
        for i in range(steps - 1):
            x += dx
            y += dy
            points.append([round(x), round(y)])
        self.draw(points)
        t2 = time.clock()

    def assymetric_DDA(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        points = [(x1, y1)]
        while (x1 < x2):
            x1 = x1 + 1.0
            y1 = y1 + dy / dx
            points.append([x1, y1])
        self.draw(points)

        dx = x2 - x1
        dy = y2 - y1
        x, y = x1, y1
        if dx and dy:
            if abs(dx) <= abs(dy):
                dy /= dx
                dx = 1.0
            else:
                dx /= dy
                dy = 1.0

            while abs(x) <= abs(x2):
                x += dx
                y += dy
                points.append([round(x), round(y)])

        elif dx:
            while abs(x) <= abs(x2):
                x += 1
                points.append([round(x), round(y1)])

        else:
            while abs(y) < abs(y2):
                y += 1
                points.append([round(x1), round(y)])

        self.draw(points)

    def Bresenham(self, x1, y1, x2, y2):
        t1 = time.clock()
        # Setup initial conditions
        dx = x2 - x1
        dy = y2 - y1
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        # Swap start and end points if necessary
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        self.draw(points)
        t2 = time.clock()
        print("Bresenham:")
        print(t2 - t1)

    def circle_Bresenham(self, xc, yc, radius):
        t1 = time.clock()
        x = 0
        y = radius
        delta = 1 - 2 * radius
        error = 0
        points = []
        while (y >= 0):
            points.append((xc + x, yc + y))
            points.append((xc + x, yc - y))
            points.append((xc - x, yc + y))
            points.append((xc - x, yc - y))
            error = 2 * (delta + y) - 1
            if (delta < 0) and (error <= 0):
                x += 1
                delta += 2 * x + 1
                continue
            error = 2 * (delta - x) - 1
            if delta > 0 and error > 0:
                y -= 1
                delta += 1 - 2 * y
                continue
            x += 1
            delta += 2 * (x - y)
            y -= 1
        self.draw(points)
        t2 = time.clock()
        print("Circle Bresenham:")
        print(t2 - t1)

    def elipse_Bresenham(self, xc, yc, radius, b):
        t1 = time.clock()
        x = 0
        y = radius
        delta = 1 - 2 * radius
        error = 0
        points = []
        if radius > b:
            while (y >= 0):
                points.append((xc + x, yc + y))
                points.append((xc + x, yc - y))
                points.append((xc - x, yc + y))
                points.append((xc - x, yc - y))
                error = 2 * (delta + y) - 1
                if (delta < 0) and (error <= 0):
                    x += 1
                    delta += 2 * x + 1
                    continue
                error = 2 * (delta - x) - 1
                if delta > 0 and error > 0:
                    y -= b / radius
                    delta += 1 - 2 * y
                    continue
                x += 1
                delta += 2 * (x - y)
                y -= b / radius
        self.draw(points)
        t2 = time.clock()
        print("Elipse Bresenham:")
        print(t2 - t1)

    def Wu(self, x1, y1, x2, y2):

        def _fpart(x):
            return x - int(x)

        def _rfpart(x):
            return 1 - _fpart(x)

        points = []
        dx, dy = x2 - x1, y2 - y1
        x, y = x1, y1

        if dy == 0:
            points.append([round(x), round(y1)])
            while abs(x) < abs(x2):
                x += 1
                points.append([round(x), round(y1)])

        elif dx == 0:
            points.append([round(x1), round(y)])
            while abs(y) < abs(y2):
                y += 1
                points.append([round(x1), round(y)])
        else:
            grad = dy / dx
            intery = y1 + _rfpart(x1) * grad

            def draw_endpoint(x, y):
                xend = round(x)
                yend = y + grad * (xend - x)
                px, py = int(xend), int(yend)
                points.append([px, py])
                points.append([px, py + 1])
                return px

            xstart = draw_endpoint(x1, y1)
            xend = draw_endpoint(x2, y2)

            for x in range(xstart, xend):
                y = int(intery)
                points.append([x, y])
                points.append([x, y + 1])
                intery += grad
        self.draw(points)

    def draw(self, coords):
        for point in coords:
            self.canvas.create_rectangle(PIXEL_SIZE * point[0], PIXEL_SIZE * point[1],
                                         PIXEL_SIZE * point[0] + PIXEL_SIZE, PIXEL_SIZE * point[1] + PIXEL_SIZE,
                                         fill="black", tag="surname")

    def clean(self):
        self.canvas.delete("surname")

    def callback(self, func_name):
        if func_name == "elipse_Bresenham":
            return lambda func_name=func_name: getattr(self, func_name)(85, 60, 15, 5)
        if func_name != "circle_Bresenham":
            def func():
                for letter, lines in self.surname.items():
                    for line in lines:
                        if letter == "o":
                            getattr(self, "circle_Bresenham")(line[0][0], line[0][1], line[1][0])
                        else:
                            getattr(self, func_name)(line[0][0], line[0][1], line[1][0], line[1][1])

            return func
        return lambda func_name=func_name: getattr(self, func_name)(85, 60, 15)

    def __init__(self):
        window = Tk()
        window.title("Lab1")
        # Place canvas in the window
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="light blue")
        self.canvas.pack()
        # Draw Frame in the window
        frame = Frame(window, bg="light blue")
        frame.pack()
        create_button(frame, "DDA", self.callback("DDA"), 1)
        create_button(frame, "Assymetric DDA", self.callback("assymetric_DDA"), 2)
        create_button(frame, "Bresenham", self.callback("Bresenham"), 3)
        create_button(frame, "Circle Bresenham", self.callback("circle_Bresenham"), 4)
        create_button(frame, "Elipse Bresenham", self.callback("elipse_Bresenham"), 5)
        create_button(frame, "Wu", self.callback("Wu"), 6)
        create_button(frame, "Clear", self.clean, 7)
        window.mainloop()


if __name__ == "__main__":
    RasterizationAlgorithms()
