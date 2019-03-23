import math
import numpy
import itertools
elements = 2
nodes = [(0,0), (1,0), (2,0)]
connectivity = [(0,1), (1,2)]
fixedNodes = [0,2]
forces = numpy.zeros((2 * len(nodes), 1))


kglobal = numpy.zeros((2 * len(nodes), 2 * len(nodes)))

for i in range(elements):
    nodeA, nodeB = connectivity[i]
    if nodeA > nodeB:
        temp = nodeA
        nodeA = nodeB
        nodeB = temp
    e = 10000
    a = 10
    Ax = nodes[nodeA][0]
    Ay = nodes[nodeA][1]
    Bx = nodes[nodeB][0]
    By = nodes[nodeB][1]
    l = math.sqrt((math.pow(Ax - Bx, 2) + math.pow(Ay - By, 2)))
    theta = math.radians(math.atan(By - Ay / (Bx - Ax)))
    k = numpy.array([[pow(math.cos(theta), 2), math.cos(theta) * math.sin(theta), -1 * pow(math.cos(theta), 2),
                      -1 * math.cos(theta) * math.sin(theta)],
                     [math.cos(theta) * math.sin(theta), pow(math.sin(theta), 2),
                      -1 * math.cos(theta) * math.sin(theta),
                      -1 * pow(math.sin(theta), 2)],
                     [-1 * pow(math.cos(theta), 2), -1 * math.cos(theta) * math.sin(theta), pow(math.cos(theta), 2),
                      math.cos(theta) * math.sin(theta)],
                     [-1 * math.cos(theta) * math.sin(theta), -1 * pow(math.sin(theta), 2),
                      math.cos(theta) * math.sin(theta), pow(math.sin(theta), 2)]])
    indexes = [2 * nodeA, 2 * nodeA + 1, 2 * nodeB, 2 * nodeB + 1]
    inputData = [indexes, indexes]
    positions = list(itertools.product(*inputData))
    k = k.flatten()
    for idx in range(len(positions)):
        kglobal[positions[idx][0]][positions[idx][1]] += k[idx]
    print(kglobal)

removed_one = []
for i in range(len(fixedNodes)):
    removed_one.append(fixedNodes[i] * 2)
    removed_one.append(fixedNodes[i] * 2 + 1)

removed_one.sort(reverse=True)
for pos in removed_one:
    kglobal = numpy.delete(kglobal, (pos), axis=0)
    kglobal = numpy.delete(kglobal, (pos), axis=1)
    forces = numpy.delete(forces, (pos))

#zeroColumns = numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)
zeroRows = numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)
for row in zeroRows:
    forces = numpy.delete(forces, (row))
#kglobal = kglobal[:, ~numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)]
kglobal = kglobal[~numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)]






