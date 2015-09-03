#!/usr/bin/env python3

###############
### FRANTIC ###
###############
# A game demonstrating the use of classes

from tkinter import *

#class definitions
class Circle:
    """ There'll be 4 types of circles:
        1. a wobbling ball, the target
        2. a simple circle, the middle of the cross-hair
        3. a filled circle, representing a hit
        4. another simple circle, representing a miss """

    def __init__(self, x, y, radius, outline, outline_color, fill_color):
        """ Mandatory arguments are:
           x, y: coords of center point
           radius: radius of circle
           outline, outline_color: outline width & color
           fill_color: filling color of circle, if any """
        self.x, self.y, self.radius = x, y, radius
        self.outline, self.outline_color = outline, outline_color
        self.fill_color = fill_color

    def rect(self, x, y):
        """ Returns circle's bounding rectangle's coordinates """
        return x - self.radius, y - self.radius, \
               x + self.radius, y + self.radius

    def draw(self, canvas):
        """ Draws circle on canvas """
        self.circle = canvas.create_oval(self.rect(self.x, self.y),
                                             fill = self.fill_color,
                                             width = self.outline,
                                             outline = self.outline_color)

    def fresh(self, canvas, x, y):
        """ Updates circle's coordinates, x, y represent new center """
        canvas.coords(self.circle, self.rect(x, y))

class Line:
    """ Line object for cross-hair """

    def __init__(self, x0, y0, x1, y1, width_, color):
        """ Mandatory arguments are:
            x-y: starting & ending coordinates
            width_: line's width
            color: line's color """
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.width_, self.color = width_, color

    def draw(self, canvas):
        """ Draws line on canvas """
        self.line = canvas.create_line(self.x0, self.y0, self.x1, self.y1,
                                       width = self.width_, fill = self.color)

    def fresh(self, canvas, x0, y0, x1, y1):
        """ Updates line's coordinates """
        canvas.coords(self.line, x0, y0, x1, y1)

class GameField(Canvas):
    """ Implements a canvas in the application frame """

    def __init__(self, parent, ro, co, size, color):
        """ Mandatory arguments are:
            parent: parent-widget
            ro, co: grid-coordinates
            color: canvas background color """
        super().__init__(parent, width = size, height = size, bg = color)
        self.grid(row = ro, column = co)

class Frantic(Frame):
    """ Main application """

    def __init__(self, parent = None):
        super().__init__(parent)
        self.grid()

def testApp():
    """ Test facility """
    w = Tk()
    app = Frantic(w)
    can = GameField(app, 0, 0, 600, "ivory")
    cir = Circle(300, 300, 50, 2, "red", "blue")
    cir.draw(can)
    lin = Line(0,300, 600, 300, 2, "blue")
    lin.draw(can)
    w.mainloop()

if __name__ == "__main__":
    testApp()
