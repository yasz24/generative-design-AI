import turtle

class StructureVisual:
    def __init__(self):
        self.turtle = turtle.Turtle()

    def drawStructure(self, assignments):
        for key in assignments:
            point1, point2 = assignments[key]
            self.turtle.setpos(50*point1[0], 50*point1[1])
            self.turtle.pendown()
            self.turtle.setpos(50*point2[0], 50*point2[1])
            self.turtle.penup()
        turtle.done()

