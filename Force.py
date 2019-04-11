

class Load:
    def __init__(self, magnitude, direction, node):
        self.magnitude = magnitude
        self.direction = direction
        self.node = node

    def getNode(self):
        return self.node

    def getDirection(self):
        return self.direction

    def getMagnitude(self):
        return self.magnitude