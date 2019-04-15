

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
                substructures.append(path)
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


print (extractSubstructures({'beam0': ((0, 0), (9, 7)), 'beam1': ((9, 7), (8, 7)), 'beam2': ((8, 7), (7, 7)), 'beam3': ((7, 7), (0, 0)), 'beam4': ((0, 0), (8, 7)), 'beam5': ((8, 7), (6, 7)), 'beam6': ((6, 7), (9, 7)), 'beam7': ((9, 7), (7, 7)), 'beam8': ((7, 7), (6, 7)), 'beam9': ((6, 7), (0, 0))}))
