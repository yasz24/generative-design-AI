from Force import Force
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
            array1.append((startPos, (i,grid_size-1)))
        domains["beam0"] = [array1]

        curBeam = 1
        top = False
        while curBeam < grid_size:
            oldbeam = "beam" + str((curBeam -1))
            newbeam = "beam" + str(curBeam)
            prevMapValue =  domains[oldbeam]
            newMapValue = domains[newbeam]

            startPositions = []
            for domainList in prevMapValue:
                for tup in domainList:
                    startPositions.append(tup[1])

            for startPosition in startPositions:
                temp = []
                if top:
                    for i in range(grid_size):
                        temp.append((startPosition, (i, grid_size-1)))
                else:
                    for i in range(grid_size):
                        temp.append((startPosition, (i, 0)))
                newMapValue.append(temp)
            top = not top
            curBeam+=1
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
            loadPerNode = 1
            forces = []
            for idx in range(len(nodes)):
                forces.append(Force(-1 * loadPerNode, 'y', idx))

            #use finite solver to see if the assignment is good so far.
            maxRight = (0,0)
            maxIdx = 0
            for idx in range(len(nodes)):
                 if nodes[idx][0] > maxRight[0] and nodes[idx][1] == 0:
                     maxRight = nodes[idx]
                     maxIdx = idx
            fixedNodes = [nodes.index((0,0)), idx]
            print("Nodes:{}".format(nodes))
            print("Fixed nodes:{}".format(fixedNodes))
            print("Connections:{}".format(connections))
            print(("Forces:{}".format(forces)))
            system = System(modulus=7500, area=0.005, nodes=nodes, fixedNodes=fixedNodes, connectivity=connections, forces=forces)
            solutions = system.computeDisplacements()
            print(solutions)
            thresholdDisplacement = 10000
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
 


csp = CSP(5, 0)

