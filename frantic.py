###############
### FRANTIC ###
###############
# A game demonstrating the use of classes

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
        canvas.create_oval(self.rect(self.x, self.y), fill = self.fill_color
                           width = outline, outline = outline_color)

    def update(self, canvas, x, y):
        """ Updates circle's coordinates, x, y represent new center """
        canvas.coords(self, self.rect(x, y))

class GameField(Canvas):
    """ Implements a canvas in the frame """

    def __init__(self, parent, ro, co, color):
        """ Mandatory arguments are:
            parent: parent-widget
            ro, co: grid-coordinates
            color: canvas background color """
        super().__init__(parent, bg = color)
        self.grid(row = ro, column = co)
