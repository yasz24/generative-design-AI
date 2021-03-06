import numpy as np
from System import System
from Force import Load
import itertools
import math
import json
from graphics import *

class FeatureExtractorUtil:

    def __init__(self):
       pass

    def extractFeatures(self, structure):
        if structure == {}:
            return [0,0,0,0]
        else:
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
        #print(structure)
        #construct a graph from the structure
        vertices = {}
        for key in structure:
            if not tuple(structure[key][0]) in vertices:
                vertices[tuple(structure[key][0])] = []
            
            if not tuple(structure[key][1]) in vertices:
                vertices[tuple(structure[key][1])] = []

        for key in structure:
            #changed the edges from a list to tuples
            vertices[tuple(structure[key][0])].append((tuple(structure[key][0]), tuple(structure[key][1])))
            vertices[tuple(structure[key][1])].append((tuple(structure[key][0]), tuple(structure[key][1])))

        for vertex in vertices:
            #print("vertex {}".format(vertex))
            edges = vertices[vertex]
            #print("edges {}".format(edges))
            angleEnds = list(itertools.combinations(edges, 2))
            #print("angle ends {}".format(angleEnds))
            for pair in angleEnds:
                if pair[0][0] == vertex:
                    vecA = np.asarray(pair[0][1]) - np.asarray(vertex)
                else:
                    vecA = np.asarray(pair[0][0]) - np.asarray(vertex)
                if pair[1][0] == vertex:
                    vecB = np.asarray(pair[1][1]) - np.asarray(vertex)
                else:
                    vecB = np.asarray(pair[1][0]) - np.asarray(vertex)
                magA = np.sqrt((vecA[0])**2+(vecA[1])**2)
                magB = np.sqrt((vecB[0])**2+(vecB[1])**2)
                totalAngle += np.arccos(np.dot(vecA,vecB)/(magA*magB))
                numAngles += 1

        totalAngle = totalAngle / 2
        if numAngles == 0:
            return 0
        else:
            averageAngle = totalAngle / numAngles

        averageAngle = math.degrees(averageAngle)
        #print("averageAngle {}".format(averageAngle))
        return averageAngle
        
    def pointDistribution(self, structure):
        minX = 0
        points = []
        for key in structure:
            points.append(structure[key][0])
            points.append(structure[key][1])
        maxX = max([pos[0] for pos in points])
        center = (maxX-minX)/2
        difference = abs(sum(pos[0] > center for pos in points) - sum(pos[0] < center for pos in points))
        return difference

    def computeSolution(self, structure):
        #print (structure)
        nodes = []
        for key in structure:
            nodeA, nodeB = structure[key]
            if nodeA not in nodes:
                nodes.append(nodeA)
            if nodeB not in nodes:
                nodes.append(nodeB)
        connections = [(nodes.index(structure[key][0]), nodes.index(structure[key][1])) for key in structure]
        nodeLoad = 10000
        loads = [Load(-1 * nodeLoad, 'y', idx) for idx in range(len(nodes))]
        #print("Nodes {}".format(nodes))
        maxRight = (0, 0)
        maxIdx = 0
        for idx in range(len(nodes)):
            if nodes[idx][0] > maxRight[0]:
                maxRight = nodes[idx]
                maxIdx = idx
            if nodes[idx][0] == maxRight[0]:
                if nodes[idx][1] < maxRight[1]:
                    maxRight = nodes[idx]
                    maxIdx = idx
        maxLeft = (float("inf"), float("inf"))
        minIdx = 0 
        for idx in range(len(nodes)):
            if nodes[idx][0] < maxLeft[0]:
                maxLeft = nodes[idx]
                minIdx = idx
            if nodes[idx][0] == maxLeft[0]:
                if nodes[idx][1] < maxLeft[1]:
                    maxLeft = nodes[idx]
                    minIdx = idx
        #not a good way to fix this. think of a better way

        if minIdx == maxIdx:
            maxIdx+=1
        fixedNodes = [minIdx, maxIdx]
        #print("fixedNodes {}".format(fixedNodes))
        #print(fixedNodes)
        #print("structure {}".format(structure))
        system = System(modulus=30e6, area=10, inertia=100, nodes=nodes, fixedNodes=fixedNodes, connectivity=connections,
                        loads=loads)
        return system.computeDisplacements()

    def averageDisplacement(self, structure):
        solution = self.computeSolution(structure)
        return sum(solution)/len(solution)

    def maxDisplacement(self, structure):
        return max(self.computeSolution(structure))

beam = {"beam0": [[0, 0], [4, 0]], "beam1": [[0, 0], [4, 4]], "beam2": [[4, 2], [2, 4]]}
f = FeatureExtractorUtil()
f.computeSolution({'beam0': ((0, 0), (4, 4)), 'beam1': ((4, 4), (0, 4)), 'beam2': ((0, 4), (0, 0))})


