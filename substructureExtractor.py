import copy
import numpy as np
from graphics import StructureVisual
import itertools

##structure -> list of structures
def extractSubstructures(structure):
    substructures = []
    graph = structureToGraph(structure)
    print(graph)
    #spanningTree, removed = GraphToSpanningTree(graph)
    exploredSet = []
    fringe = [(list(graph.keys())[0], [])]
    while len(fringe) > 0:
        node, path = fringe.pop(0)
        path.append(node)
        if node in exploredSet:
            if path in substructures:
                continue
            else:
                occurances = [index for index, n in enumerate(path) if n ==node]
                cycle = []
                for i in range(occurances[0], occurances[1]):
                    cycle.append(path[i])
                path = []
                substructures.append(cycle)
        else:
            exploredSet.append(node)
        children = graph[node]
        for child in children:
            fringe.append((child, path))
    return substructures


##structure to graph
def structureToGraph(structure):
    graph = {}
    for key in structure:
        nodeA, nodeB = structure[key]
        nodeA = (nodeA[0], nodeA[1])
        nodeB = (nodeB[0], nodeB[1])
        if nodeA not in graph:
            graph[nodeA] = [nodeB]
        else:
            graph[nodeA] += [nodeB]
        if nodeB not in graph:
            graph[nodeB] = [nodeA]
        else:
            graph[nodeB] += [nodeA]
    return graph

def GraphToSpanningTree(graph):
    removed = {}
    spanningTree = copy.deepcopy(graph)
    cyclesExist = True
    while cyclesExist:
        for key in spanningTree:
            removeCycle(spanningTree, removed, key, key)
        for i in spanningTree:
            children = spanningTree[i]
            childrenConnections = itertools.combinations(children, 2)
            for connection in childrenConnections:
                if connection[1] in spanningTree[connection[0]]:
                    spanningTree[connection[0]].remove(connection[1])
                    removed[connection[0]] = connection[1]
        cyclesExist = False
    return spanningTree, removed

def removeCycle(spanningTree, removed, key, start):

    if (start in spanningTree[key]):
        spanningTree[key].remove(start)
        removed[key] = start
        return
    else:
        for node in spanningTree[key]:
            removeCycle(spanningTree, removed, node, start)


def getLength(nodeA, nodeB):
    return np.sqrt((nodeA[0]-nodeB[0])**2 + (nodeA[1]-nodeB[1])**2)

print (extractSubstructures({'beam0': ((0, 0), (0, 3)), 'beam1': ((0, 3), (1, 3)), 'beam2': ((1, 3), (2, 3)), 'beam3': ((2, 3), (0, 0)), 'beam4': ((0, 0), (1, 3))}))
