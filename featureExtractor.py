import numpy as np

class FeatureExtractorUtil:

    def __init__(self):
        pass

    def extractFeatures(self, structure):
	    totalLength = totalLengthFeature(structure)

    def totalLengthFeature(self, structure):
        totalLength = 0
        for key in structure:
            nodeA, nodeB = structure[key]
            totalLength += np.sqrt(pow(nodeB[0]-nodeA[0], 2) + pow(nodeB[1]-nodeA[1], 2))
        return totalLength

    def averageAngle(self, structure):
        averageAngle = 0
        totalAngle = 0
        connections=[structure[key] for key in structure]
        adjacentConnections = {}
        for pair1 in connections:
            for pair2 in connections:
                if pair1[0] in pair2 or pair1[1] in pair2:
                    adjacentConnections[pair1] += [pair2]
        for start in adjacentConnections:
            adjacentConnections[start]

    def pointDistribution(self, structure):
        pass




