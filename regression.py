import numpy as np
from featureExtractor import FeatureExtractorUtil
import json
import csv
import csv
from extractSubStructures import *

class Regression:

    def __init__(self, dataSet):
        self.weights = []
        self.dataSet = dataSet
        extractSubstructures = ExtractSubStructures()
        extractSubstructures.createRegressionData(dataSet)
        self.features = extractSubstructures.getFeatures()
        self.targets = extractSubstructures.getTargets()
        self.normalEquations()

    def getWeights(self):
        return self.weights

    def featureMatrix(self):
        self.features

    def targetMatrix(self):
        self.targets

    def evaluate(self, theta, x):
        return sum([theta[i] * x[i] for i in range(len(x))])

    def lr(self, N = 12, alpha = 0.01):
        theta = [0] * len(self.features[0])
        for k in range(N):
            i = k % len(self.features)
            h = self.evaluate(theta, self.features[i])
            # print("targets {}".format(targets))
            # print("i {} hypothesis {}".format(i, h))
            error = h - self.targets[i]
            for j in range(len(theta)):
                theta[j] -= alpha * error * self.features[i][j]
        self.weights = theta

    def normalEquations(self):
        X = np.matmul(np.transpose(self.features), self.features)
        Y = np.matmul(np.transpose(self.features), self.targets)
        self.weights = np.linalg.solve(X, Y)


r = Regression("Database.txt")
print(r.getWeights())



