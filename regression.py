import numpy as np
from featureExtractor import FeatureExtractorUtil
import json
import csv
import csv

results = []
with open("Advertising.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        results.append(row)


def featureMatrix(dataSet):
    featureExtractor = FeatureExtractorUtil()
    data = [json.loads(line) for line in open(dataSet)]
    return [featureExtractor.extractFeatures(structure) for structure in data]

def targetMatrix(dataSet):
    targetExtractor = FeatureExtractorUtil()
    data = [json.loads(line) for line in open(dataSet)]
    return [targetExtractor.extractTargets(structure) for structure in data]

def evaluate(theta, x):
    print(sum([theta[i] * x[i] for i in range(len(x))]))
    return sum([theta[i] * x[i] for i in range(len(x))])

ef lr(features, targets, N = 100, alpha = 0.01):
    for k in range(N):
        i = k % len(features)
        print(i)
        h = evaluate(theta, features[i])
        print("targets {}".format(targets))
        print("i {} hypothesis {}".format(i, h))
        error = targets[i] - h
        for j in range(len(theta)):
            theta[j] -= alpha * error * features[i][j]
    return theta

feature = []
target = []
for i in results:
    for j in i:
        feature.append(i[1:-1])
        target.append(i[-1])

#print(lr(feature,target))
feature = np.array(feature)
target = np.array(target)
AT
