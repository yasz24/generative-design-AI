import numpy as np

def evaluate(theta, x):
    return sum([theta[i] * x[i] for i in range(len(x))])

def lr(features, targets, sq =False, N = 1000, alpha = 0.01):
    theta = [0]*len(features[0])
    for k in range(N):
        i = k % len(features)
        h = evaluate(theta, features[i])
        error = targets[i] - h
        for j in range(len(theta)):
            theta[j] += alpha * error * features[i][j]
    return theta
