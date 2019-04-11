import numpy as np
from System import System
from Force import Load
import itertools
import json
from graphics import *

class FeatureExtractorUtil:

    def __init__(self):
       pass

    def extractFeatures(self, structure):
        features = [self.totalLengthFeature(structure),
                    self.averageAngle(structure),
                    self.pointDistribution(structure),
                    self.averageDisplacement(structure)]
        return features

    def extractTargets(self, structure):
        return self.maxDisplacement(structure)

    def totalLengthFeature(self, structure):
        totalLength = 0
        for key in structure:
            nodeA, nodeB = structure[key]
            totalLength += np.sqrt(pow(nodeB[0]-nodeA[0], 2) + pow(nodeB[1]-nodeA[1], 2))
        return totalLength

    def averageAngle(self, structure):
        totalAngle = 0
        numAngles = 0
        connections=[structure[key] for key in structure]
        adjacentConnections = {}
        for pair1 in connections:
            for pair2 in connections:
                if pair1[0] in pair2 or pair1[1] in pair2:
                    adjacentConnections[pair1] += [pair2]
        for start in adjacentConnections:
            ends = adjacentConnections[start]
            angleEnds = list(itertools.combinations(ends), 2)
            for pair in angleEnds:
                vecA = 0
                vecB = 0
                magA = np.sqrt((pair[0][0]-start[0])**2+(pair[0][1]-start[0])**2)
                magB = np.sqrt((pair[1][0]-start[0])**2+(pair[1][1]-start[0])**2)
                totalAngle += np.arccos(np.dot(vecA,vecB)/(magA*magB))
                numAngles += 1
        averageAngle = totalAngle / numAngles
        return averageAngle
        
    def pointDistribution(self, structure):
        minX = 0
        points = []
        for key in structure:
            point1 = structure[key][0]
            point2 = structure[key][1]
            if point1 not in points:
                points.append(point1)
            if point2 not in points:
                points.append(point2)

        maxX = max([pos[0] for pos in points])
        center = (maxX-minX)/2
        difference = abs(sum(pos[0] > center for pos in points) - sum(pos[0] < center for pos in points))
        return difference

    def computeSolution(self, structure):
        nodes = []
        for key in assignment:
            nodeA, nodeB = assignment[key]
            if nodeA not in nodes:
                nodes.append(nodeA)
            if nodeB not in nodes:
                nodes.append(nodeB)
        connections = [(nodes.index(structure[key][0]), nodes.index(structure[key][1])) for key in structure]
        nodeLoad = 10000
        loads = [Load(-1 * nodeLoad, 'y', idx) for idx in range(len(nodes))]
        maxRight = (0, 0)
        maxIdx = 0
        for idx in range(len(nodes)):
            if nodes[idx][0] > maxRight[0] and nodes[idx][1] == 0:
                maxRight = nodes[idx]
                maxIdx = idx
        if maxIdx == 0:
            maxIdx = idx
        fixedNodes = [nodes.index((0, 0)), maxIdx]
        system = System(modulus=30e6, area=10, inertia=100, nodes=nodes, fixedNodes=fixedNodes, connectivity=connections,
                        loads=loads)
        return system.computeDisplacements()

    def averageDisplacement(self, structure):
        solution = self.computeSolution(structure)
        return sum(solution)/len(solution)

    def maxDisplacement(self, structure):
        return max(self.computeSolution(structure))

beam = {"beam0": [[0, 0], [4, 0]], "beam1": [[0, 0], [4, 4]], "beam2": [[4, 2], [4, 2]]}
f = FeatureExtractorUtil()
#StructureVisual().drawStructure(beam)
