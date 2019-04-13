from Force import Load
from System import System

class CSP:
    def __init__(self, grid_size, discConstant):
        self.variables = self.initializeVariables(grid_size)
        self.domains = self.initializeDomain(grid_size)
        self.constraints = self.checkConstraints
        self.discConstant = 1

    def initializeVariables(self, grid_size):
        temp = []
        for i in range(grid_size):
            beam = "beam" + str(i)
            temp.append(beam)
        return temp

    def initializeDomain(self, grid_size):
        domains = {}
        startPos = (0,0)
        for beam in self.variables:
            domains[beam] = []

        #array for beam0
        array1 = []
        for i in range(grid_size):
            for j in range(grid_size):
                if not ((i ==0) and (j==0)): 
                    array1.append((startPos, (i, j)))
        domains["beam0"] = tuple([array1])

        commonDomain = []
        for i in range(grid_size):
            for j in range(grid_size):
                domainList = []
                for k in range(grid_size):
                    for l in range(grid_size):
                        if (k, l) != (i, j):
                            domainList.append(((i, j), (k, l)))
                commonDomain.append(tuple(domainList))


        for idx in range(1, grid_size):
            beam = "beam" + str(idx)
            beamDomain = []

            for domainTuple in commonDomain:
                beamDomain.append(domainTuple)

            domains[beam] = beamDomain

        return domains

    def checkConstraints(self, assignment):
        print("assignment:{}".format(assignment))
        #code to make sure no to beams are the same.
        assignmentTups = []
        for key in assignment:
            tup = assignment[key]
            assignmentTups.append(tup)

        if self.noSameBeams(assignmentTups):
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
                loads.append(Load(-1 * loadPerNode, 'y', idx))
                loads.append(Load(loadPerNode/10, 'k', idx))

            #use finite solver to see if the assignment is good so far.
            maxRight = (0,0)
            maxIdx = 0
            for idx in range(len(nodes)):
                 if nodes[idx][0] > maxRight[0] and nodes[idx][1] == 0:
                     maxRight = nodes[idx]
                     maxIdx = idx
            if maxIdx == 0:
                maxIdx = idx
            fixedNodes = [nodes.index((0,0)), maxIdx]
            print("Nodes:{}".format(nodes))
            print("Fixed nodes:{}".format(fixedNodes))
            print("Connections:{}".format(connections))
            print(("Loads:{}".format(loads)))
            system = System(modulus=30e6, area=10, inertia=100, nodes=nodes, fixedNodes=fixedNodes, connectivity=connections, loads=loads)
            solutions = system.computeDisplacements()
            print(solutions)
            thresholdDisplacement = 0.00001
            validAssignment = not(abs(max(solutions)) > thresholdDisplacement or abs(min(solutions)) > thresholdDisplacement)
            print(validAssignment)
            return validAssignment
        else:
            return False

    def noSameBeams(self, assignmentTups):
        i = 0
        while i < len(assignmentTups):
            cur = assignmentTups[i]
            for j in range(i+1, len(assignmentTups)):
                if assignmentTups[j][0] == cur[1] and assignmentTups[j][1] == cur[0]:
                    return False
                if assignmentTups[j] == cur:
                    return False
            i+=1
        return True
 




# total = 0
# for domainList in csp.domains["beam1"]:
#     for domain in domainList:
#         total+=1



