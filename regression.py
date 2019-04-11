import numpy as np
from featureExtractor import FeatureExtractorUtil

class Regression:
    def __init__(self):
        self.features = []
        self.targets = []

    def featureMatrix(self, dataSet):
        featureExtractor = FeatureExtractorUtil()
        data = [json.loads(line) for line in open(dataSet)]
        self.features = [featureExtractor.extractFeatures(structure) for structure in data]

    def targetMatrix(self, dataSet):
        targetExtractor = FeatureExtractorUtil()
        data = [json.loads(line) for line in open(dataSet)]
        self.features = [targetExtractor.extractTargets(structure) for structure in data]

    def evaluate(self, theta, x):
        return sum([theta[i] * x[i] for i in range(len(x))])

    def lr(self, features, targets, N = 1000, alpha = 0.01):
        theta = [0]*len(features[0])
        for k in range(N):
            i = k % len(features)
            h = evaluate(theta, features[i])
            error = targets[i] - h
            for j in range(len(theta)):
                theta[j] += alpha * error * features[i][j]
        return theta
