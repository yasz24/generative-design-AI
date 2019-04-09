import _json
from System import System
from Force import Load
from graphics import StructureVisual

s = StructureVisual()

struct1 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0))}



struct2 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 4), (4, 0)),
           'beam5': ((0, 0), (4, 4))}

struct3 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 4), (4, 0))}

struct4 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((4, 0), (4, 4)),
           'beam2': ((4, 4), (0, 4)),
           'beam3': ((0, 4), (0, 0)),
           'beam4': ((0, 0), (4, 4))}

struct5 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (2, 4)),
           'beam2': ((2, 4), (4, 0))}

struct6 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((4, 0), (4, 2)),
           'beam3': ((0, 2), (2, 2)),
           'beam4': ((2, 2), (4, 2)),
           'beam5': ((2, 2), (4, 0)),
           'beam6': ((0, 0), (2, 2))}

struct7 = {'beam0': ((0, 0), (2, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((0, 2), (2, 2)),
           'beam3': ((2, 2), (4, 2)),
           'beam5': ((4, 2), (4, 0)),
           'beam6': ((2, 0), (4, 0)),
           'beam7': ((2, 0), (2, 2))}

struct8 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 2)),
           'beam2': ((4, 0), (4, 2)),
           'beam3': ((0, 2), (2, 2)),
           'beam4': ((2, 2), (4, 2)),
           'beam5': ((2, 2), (4, 0))}

struct9 = {'beam0': ((0, 0), (4, 0)),
           'beam1': ((0, 0), (0, 4)),
           'beam2': ((0, 4), (2, 4)),
           'beam3': ((2, 4), (4, 4)),
           'beam4': ((4, 4), (4, 0)),
           'beam5': ((2, 4), (2, 2)),
           'beam6': ((0, 0), (2, 2)),
           'beam7': ((2, 2), (4, 0))}



s.drawStructure(struct4)


def noSameBeams(assignmentTups):
    i = 0
    while i < len(assignmentTups):
        cur = assignmentTups[i]
        for j in range(i + 1, len(assignmentTups)):
            if assignmentTups[j][0] == cur[1] and assignmentTups[j][1] == cur[0]:
                return False
            if assignmentTups[j] == cur:
                return False
        i += 1
    return True

def checkConstraints(assignment):
    print("assignment:{}".format(assignment))
    # code to make sure no to beams are the same.
    assignmentTups = []
    for key in assignment:
        tup = assignment[key]
        assignmentTups.append(tup)

    if noSameBeams(assignmentTups):
        nodes = []
        for key in assignment:
            nodeA, nodeB = assignment[key]
            if nodeA not in nodes:
                nodes.append(nodeA)
            if nodeB not in nodes:
                nodes.append(nodeB)

        connections = []
        for key in assignment:
            nodeA, nodeB = assignment[key]
            connections.append((nodes.index(nodeA), nodes.index(nodeB)))

        # uniformly distribute the load
        loadPerNode = 10000
        loads = []
        for idx in range(len(nodes)):
            loads.append(Load(-1 * loadPerNode, 'f', idx))

        # use finite solver to see if the assignment is good so far.
        maxRight = (0, 0)
        maxIdx = 0
        for idx in range(len(nodes)):
            if nodes[idx][0] > maxRight[0] and nodes[idx][1] == 0:
                maxRight = nodes[idx]
                maxIdx = idx
        fixedNodes = [nodes.index((0, 0)), maxIdx]
        print("Nodes:{}".format(nodes))
        print("Fixed nodes:{}".format(fixedNodes))
        print("Connections:{}".format(connections))
        print(("Loads:{}".format(loads)))
        system = System(200e9, 0.06928, nodes,fixedNodes, connections,loads)
        solutions = system.computeDisplacements()
        print(solutions)
        thresholdDisplacement = 0.0001
        validAssignment = not (
                    abs(max(solutions)) > thresholdDisplacement or abs(min(solutions)) > thresholdDisplacement)
        print(validAssignment)
        return validAssignment
    else:
        return False

print(checkConstraints(struct4))