#!/usr/bin/env python3

###############
### FRANTIC ###
###############
# A game demonstrating the use of classes

from tkinter import *
import random, math

#class definitions
class Circle:
    """ There'll be 4 types of circles:
        1. a wobbling ball, the target
        2. a simple circle, the middle of the cross-hair
        3. a filled circle, representing a hit
        4. another simple circle, representing a miss """

    def __init__(self, x, y, radius, outline, outline_color, fill_color):
        """ x, y: coords of center point
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
        """ x-y: starting & ending coordinates
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
        """ parent: parent-widget
            ro, co: grid-coordinates
            color: canvas background color """
        super().__init__(parent, width = size, height = size, bg = color)
        self.size, self.parent = size, parent
        self.grid(row = ro, column = co, columnspan = 3)
        self.initElements()
        self.bind("<Motion>", self.moveCrossHair)
        self.bind("<Button-1>", self.checkHit)

    def initElements(self):
        """ Inits game elements """
        self.ball = None
        self.sight = Circle(self.size / 2, self.size / 2, self.size / 20,
                            1, "green", None)
        self.horizontal = Line(0, self.size / 2, self.size, self.size / 2,
                               1, "green") #horizontal crosshair
        self.vertical = Line(self.size / 2, 0, self.size / 2, self.size,
                             1, "green") #vertical crosshair
        self.sight.draw(self)
        self.horizontal.draw(self)
        self.vertical.draw(self)
        self.initBall()
        self.moveBall()

    def initBall(self):
        """ Separate ball initialization because of respawn after hit """
        self.delete(self.ball)
        self.ball = Circle(self.size / 2, self.size / 2, self.size / 20,
                           1, "blue", "blue")
        self.ball.draw(self)
    
    def moveCrossHair(self, event):
        """ Crosshair follows mouse movement """
        self.sight.fresh(self, event.x, event.y)
        self.horizontal.fresh(self, 0, event.y, self.size, event.y)
        self.vertical.fresh(self, event.x, 0, event.x, self.size)

    def getCoord(self, coord, direction, displace, trig):
        """ Returns new coordinate """
        displace = trig(direction) * displace
        coord += displace
        if coord < self.ball.radius:
            coord = self.ball.radius
        if coord > self.size - self.ball.radius:
            coord = self.size - self.ball.radius
        return coord

    def moveBall(self):
        """ Moves ball in a random direction """
        direction, displace = math.radians(random.randrange(359)), 7
        self.ball.x = self.getCoord(self.ball.x, direction, displace, math.sin)
        self.ball.y = self.getCoord(self.ball.y, direction, displace, math.cos)
        self.ball.fresh(self, self.ball.x, self.ball.y)
        self.after(10, self.moveBall) #delay in milliseconds
    
    def checkHit(self, event):
        """ Checks if crosshair was on ball at left-click """
        distance = math.sqrt((event.x - self.ball.x)**2 + \
                             (event.y - self.ball.y)**2) #to ball's center
        if distance <= self.ball.radius: #within ball
            hit = Circle(event.x, event.y, self.size / 20, 1, "red", "red")
            hit.draw(self)
            self.parent.hit += 1
            self.create_text(event.x, event.y, text = str(self.parent.hit))
            self.initBall()
        else:
            miss = Circle(event.x, event.y, self.size / 20, 2, "blue", None)
            miss.draw(self)
            self.parent.miss += 1
            self.create_text(event.x, event.y, text = str(self.parent.miss))
        total = self.parent.hit + self.parent.miss #all clicks
        self.parent.hitrate.set("{:.2%}".format(self.parent.hit / total))
            
class Frantic(Frame):
    """ Main application """

    def __init__(self, parent = None):
        super().__init__(parent)
        self.master.title("FRANTIC")
        self.setWidgets()
        self.grid()
        self.newGame()

    def setWidgets(self):
        """ Places widgets """
        self.hitrate = StringVar()
        self.canvas = GameField(self, 0, 0, 600, "ivory")
        Label(self,text = "Hitrate:").grid(row = 1, column = 0)
        Label(self, textvariable = self.hitrate).grid(row = 1, column = 1)
        Button(self, text = "Reset", command = self.canvas.initBall).grid(row = 1, column = 2)
    
    def newGame(self):
        """ Starts a new game """
        self.hitrate.set("0.00%")
        self.hit, self.miss = 0, 0

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
    Frantic().mainloop()
