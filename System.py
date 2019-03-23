import numpy
import math
import itertools
import copy

class System:

    def __init__(self, modulus, area, nodes, fixedNodes, connectivity, forces):
        """
        :param modulus: Modulus of the elements
        :param area: Area of the elements
        :param nodes: List of the nodes in the system
        :param fixedNodes: List of numbers of nodes that are fixed in the system
        :param connectivity: List of pairs of position
        :param forces: List of the Forces on the system
        :param displacements: the displacements of the nodes
        """
        self.nodes = nodes
        self.fixedNodes = fixedNodes
        self.forces = numpy.zeros((len(self.nodes) * 2, 1))
        self.addForces(forces)
        self.kglobal = numpy.zeros((len(self.nodes) * 2, len(self.nodes) * 2))
        self.connectivity = connectivity
        self.modulus = modulus
        self.area = area
        self.assemble()

    def addForces(self, forces):
        """
        Adds a force to the system
        :param forces: A Force object
        :return: Void
        """
        self.forces = numpy.zeros((len(self.nodes) * 2, 1))
        for force in forces:
            if force.getDirection() == 'x':
                self.forces[2 * force.getNode()] += force.getMagnitude()
            if force.getDirection() == 'y':
                self.forces[2 * force.getNode() + 1] += force.getMagnitude()
            else:
                raise Exception('Direction of force no in coordinate system')

    def addNode(self, number, pos):
        """
        Adds a node to the system
        :param number: Number of the node within the system
        :param pos: The position of the node in 3d space
        :return: Void
        """
        if number > len(self.nodes):
            while len(self.nodes) <= number:
                self.nodes.append((0,0))
            self.nodes[number] = pos
        elif self.nodes[number] == (0,0):
            self.nodes[number] = pos
        else:
            raise Exception('This node already exists, please number this differently')

    def replaceNode(self, number, pos):
        """
         Replaces a given node if the node exists in the system
        :param number: The number of the node in the system
        :param pos: The position of the node in 3D space
        :return: Void
        """
        if number < len(self.nodes):
            self.nodes[number] = pos
        else:
            raise Exception('This node does not exist')

    def assemble(self):
        """
        Takes the information about the nodes in 3d space and the connevtivity of each node
        and creates a stiffness matrix for the system
        :return: Numpy Array
        """
        for i in range(len(self.connectivity)):
            nodeA, nodeB = self.connectivity[i]
            if nodeA > nodeB:
                temp = nodeA
                nodeA = nodeB
                nodeB = temp
            Ax = self.nodes[nodeA][0]
            Ay = self.nodes[nodeA][1]
            Bx = self.nodes[nodeB][0]
            By = self.nodes[nodeB][1]
            length = math.sqrt((math.pow(Ax - Bx, 2) + math.pow(Ay - By, 2)))
            theta = math.radians(math.atan(By - Ay / (Bx - Ax)))
            k = ((self.modulus * self.area) / length) * numpy.array([[pow(math.cos(theta), 2), math.cos(theta)
                                                                      * math.sin(theta), -1 * pow(math.cos(theta), 2),
                              -1 * math.cos(theta) * math.sin(theta)],
                             [math.cos(theta) * math.sin(theta), pow(math.sin(theta), 2),
                              -1 * math.cos(theta) * math.sin(theta),
                              -1 * pow(math.sin(theta), 2)],
                             [-1 * pow(math.cos(theta), 2), -1 * math.cos(theta) * math.sin(theta),
                              pow(math.cos(theta), 2),
                              math.cos(theta) * math.sin(theta)],
                             [-1 * math.cos(theta) * math.sin(theta), -1 * pow(math.sin(theta), 2),
                              math.cos(theta) * math.sin(theta), pow(math.sin(theta), 2)]])
            indexes = [2 * nodeA, 2 * nodeA + 1, 2 * nodeB, 2 * nodeB + 1]
            inputData = [indexes, indexes]
            positions = list(itertools.product(*inputData))
            k = k.flatten()
            for idx in range(len(positions)):
                self.kglobal[positions[idx][0]][positions[idx][1]] += k[idx]
        return self.kglobal

    def applyBoundaryConditions(self):
        """
        Uses the information about the boundary conditions to remove
        variables from the equations relating displacement to force
        :return: Void
        """
        kglobal = copy.deepcopy(self.kglobal)
        forces = copy.deepcopy(self.forces)
        removed_one = []
        for i in range(len(self.fixedNodes)):
            removed_one.append(self.fixedNodes[i] * 2)
            removed_one.append(self.fixedNodes[i] * 2 + 1)

        removed_one.sort(reverse=True)
        for pos in removed_one:
            kglobal = numpy.delete(kglobal, (pos), axis=0)
            kglobal = numpy.delete(kglobal, (pos), axis=1)
            forces = numpy.delete(forces, (pos), axis=0)

        zeroColumns = numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)
        zeroRows = numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)

        kglobal = kglobal[:, ~numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)]
        kglobal = kglobal[~numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)]

        kglobalidx = 0
        removed = copy.deepcopy(removed_one)
        removed.reverse()
        for idx in range(0, len(removed) - 1):
            if removed[idx + 1] - removed[idx] > 1:
                if zeroRows[kglobalidx]:
                    forces = numpy.delete(forces, (kglobalidx))
                    removed_one.append(idx+kglobalidx)
                if zeroRows[kglobalidx + 1]:
                    forces = numpy.delete(forces, (kglobalidx))
                    removed_one.append(idx+kglobalidx+1)
                kglobalidx += 2

        for row in range(len(zeroRows)):
            if zeroRows[row]:
                forces = numpy.delete(forces, (row))

        return kglobal, forces, removed_one

    def computeDisplacements(self):
        """
        Solves the system using the given parameters
        :return: Returns the displacement of each node in the x and y coordinates
        """
        kglobal, forces, removed_one = self.applyBoundaryConditions()
        allDisplacements = numpy.zeros(len(self.nodes) * 2)
        displacements = numpy.matmul(numpy.linalg.inv(kglobal), forces)
        i = 0
        for idx in range(len(allDisplacements)):
            if idx in removed_one:
                allDisplacements[idx] = 0

            else:
                allDisplacements[idx] = displacements.pop(0)


    def computeStresses(self):
        stresses = []
        for i in range(self.connectivity):
            nodeA, nodeB = self.connectivity[i]
            if nodeA > nodeB:
                temp = nodeA
                nodeA = nodeB
                nodeB = temp
            Ax = self.nodes[nodeA][0]
            Ay = self.nodes[nodeA][1]
            Bx = self.nodes[nodeB][0]
            By = self.nodes[nodeB][1]
            globalDisplacements = self.computeDisplacements()
            localDisplacements = numpy.array([globalDisplacements[2 * nodeA],
                                              globalDisplacements[2*nodeA+1],
                                              globalDisplacements[2*nodeB],
                                              globalDisplacements[2*nodeB+1]])
        length = math.sqrt((math.pow(Ax - Bx, 2) + math.pow(Ay - By, 2)))
        theta = math.radians(math.atan(By - Ay / (Bx - Ax)))
        stresses.append(self.modulus * numpy.matmul(numpy.matmul(numpy.array([-1/length, 1/length]),
                                                 [[math.cos(theta), math.sin(theta), 0, 0],
                                                  [0,0, math.cos(theta), math.sin(theta)]]),
                                    localDisplacements))



s = System(1,1,[(0,0), (1,0), (2,0)],[0,2],[(0,1), (1,2)], [])
print(s.computeDisplacements())