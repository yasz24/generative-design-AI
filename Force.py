

class Load:
    def __init__(self, magnitude, type, node):
        self.magnitude = magnitude
        self.type = type
        self.node = node

    def getNode(self):
        return self.node

    def getDirection(self):
        return self.type

    def getMagnitude(self):
        return self.magnitude