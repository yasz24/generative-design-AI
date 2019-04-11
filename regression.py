import numpy as np
from featureExtractor import FeatureExtractorUtil
import json


def featureMatrix(dataSet):
    featureExtractor = FeatureExtractorUtil()
    data = [json.loads(line) for line in open(dataSet)]
    return [featureExtractor.extractFeatures(structure) for structure in data]

def targetMatrix(dataSet):
    targetExtractor = FeatureExtractorUtil()
    data = [json.loads(line) for line in open(dataSet)]
    return [targetExtractor.extractTargets(structure) for structure in data]

def evaluate(theta, x):
    return sum([theta[i] * x[i] for i in range(len(x))])

def lr(features, targets, N = 10000, alpha = 0.001):
    theta = [0]*len(features[0])
    for k in range(N):
        i = k % len(features)
        h = evaluate(theta, features[i])
        error = targets[i] - h
        for j in range(len(theta)):
            theta[j] += alpha * error * features[i][j]
    return theta
