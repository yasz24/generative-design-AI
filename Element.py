import numpy as np
import math
class Element:

    def __init__(self, nodeA, nodeB, strength, area):
        self.area = area
        self.strength = strength
        if nodeA > nodeB:
            temp = nodeA
            nodeA = nodeB
            nodeB = temp
        self.nodeA = nodeA
        self.nodeB = nodeB


    def getNodeA(self):
        return self.nodeA

    def getNodeB(self):
        return self.nodeB


