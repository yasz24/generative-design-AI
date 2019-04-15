import copy

##structure -> list of structures
def extractSubstructures(structure):
    substructures = []
    graph = structureToGraph(structure)
    exploredSet = []
    fringe = [(list(graph.keys())[0], [])]
    while len(fringe) > 0:
        node, path = fringe.pop(0)
        path.append(node)
        if node in exploredSet:
            if path in substructures:
                continue
            else:
                exploredSet = []
                substructures.append(copy.deepcopy(path))
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


print (extractSubstructures({'beam0': ((0, 0), (0, 3)), 'beam1': ((0, 3), (1, 3)), 'beam2': ((1, 3), (2, 3)), 'beam3': ((2, 3), (0, 0)), 'beam4': ((0, 0), (1, 3))}))
