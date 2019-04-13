import numpy as np
from featureExtractor import FeatureExtractorUtil
import json
import csv
import csv


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

def lr(features, targets, N = 12, alpha = 0.01):
    theta = [0] * len(features[0])
    for k in range(N):
        i = k % len(features)
        h = evaluate(theta, features[i])
        #print("targets {}".format(targets))
        #print("i {} hypothesis {}".format(i, h))
        error = targets[i] - h
        for j in range(len(theta)):
            theta[j] -= alpha * error * features[i][j]
    return theta

def normalEquations(features, targets):
    X = np.matmul(np.transpose(features), features)
    Y = np.matmul(np.transpose(features), targets)
    return np.linalg.solve(X,Y)

#weights = normalEquations(featureMatrix('Database.txt'),targetMatrix('Database.txt'))
#print(weights)


"""feature = []
target = []
for i in results:
    for j in i:
        feature.append(i[1:-1])
        target.append(i[-1])

#print(lr(feature,target))
feature = np.array(feature)
target = np.array(target)
normalEquations(feature,target)"""

