import numpy
import math
import itertools
import copy
from Force import Load

class System:

    def __init__(self, modulus, area, nodes, fixedNodes, connectivity, loads):
        """
        :param modulus: Modulus of the elements
        :param area: Area of the elements
        :param nodes: List of the nodes in the system
        :param fixedNodes: List of numbers of nodes that are fixed in the system
        :param connectivity: List of pairs of position
        :param loads: List of the loads on the system
        :param displacements: the displacements of the nodes
        """
        self.nodes = nodes
        self.fixedNodes = fixedNodes
        self.loads = numpy.zeros((len(self.nodes) * 2, 1))
        self.addloads(loads)
        self.kglobal = numpy.zeros((len(self.nodes) * 2, len(self.nodes) * 2))
        self.connectivity = connectivity
        self.modulus = modulus
        self.area = area
        self.assemble()

    def addloads(self, loads):
        """
        Adds a load to the system
        :param loads: A load object
        :return: Void
        """
        self.loads = numpy.zeros((len(self.nodes) * 2, 1))
        for load in loads:
            if load.getDirection() == 'f':
                self.loads[2 * load.getNode()] += load.getMagnitude()
            elif load.getDirection() == 'm':
                self.loads[2 * load.getNode() + 1] += load.getMagnitude()
            else:
                raise Exception('Direction of load no in coordinate system')

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

    def localTruss(self, length, theta):
        return ((self.modulus * self.area) / length) * numpy.array([[pow(math.cos(theta), 2), math.cos(theta)
                                                                  * math.sin(theta), -1 * pow(math.cos(theta), 2),
                                                                  -1 * math.cos(theta) * math.sin(theta)],
                                                                 [math.cos(theta) * math.sin(theta),
                                                                  pow(math.sin(theta), 2),
                                                                  -1 * math.cos(theta) * math.sin(theta),
                                                                  -1 * pow(math.sin(theta), 2)],
                                                                 [-1 * pow(math.cos(theta), 2),
                                                                  -1 * math.cos(theta) * math.sin(theta),
                                                                  pow(math.cos(theta), 2),
                                                                  math.cos(theta) * math.sin(theta)],
                                                                 [-1 * math.cos(theta) * math.sin(theta),
                                                                  -1 * pow(math.sin(theta), 2),
                                                                  math.cos(theta) * math.sin(theta),
                                                                  pow(math.sin(theta), 2)]], dtype=numpy.float64)
    def localBeam(self, length, theta):
        areaInertia = (1/12)*pow(self.area, 2)
        return ((self.modulus * areaInertia) / pow(length, 3)) \
                 * numpy.array([[pow(math.cos(theta), 2) * (12 - 4 * pow(length, 2)) - 12 * math.sin(theta) * math.cos(
            theta) * length + 4 * pow(length, 2),
                                 12 * pow(math.cos(theta), 2) * length + math.sin(theta) * math.cos(theta) * (
                                             12 - 4 * pow(length, 2)) - 6 * length,
                                 pow(math.cos(theta), 2) * (-2 * pow(length, 2) - 12) + 2 * pow(length, 2),
                                 math.sin(theta) * math.cos(theta) * (-2 * pow(length, 2) - 12) + 6*length],
                                [12 * pow(math.cos(theta), 2) * length + math.sin(theta) * math.cos(theta) * (
                                            12 - 4 * pow(length, 2)) - (6 * length),
                                 pow(math.cos(theta), 2) * (4 * pow(length, 2) - 12) + 12 * math.sin(theta) * math.cos(
                                     theta) * length + 12,
                                 math.sin(theta) * math.cos(theta) * (-2 * pow(length, 2) - 12) - (6 * length),
                                 pow(math.cos(theta), 2) * (2 * pow(length, 2) + 12) - 12],
                                [pow(math.cos(theta), 2) * (-2 * pow(length, 2) - 12) + 2 * pow(length, 2),
                                 math.sin(theta) * math.cos(theta) * (-2 * pow(length, 2) - 12) - (6 * length),
                                 pow(math.cos(theta), 2) * (12 - 4 * pow(length, 2)) + 12 * math.sin(theta) * math.cos(
                                     theta) * length + 4 * pow(length, 2),
                                 -12 * pow(math.cos(theta), 2) * length + math.sin(theta) * math.cos(theta) * (
                                             12 - 4 * pow(length, 2)) + (6 * length)],
                                [math.sin(theta) * math.cos(theta) * (-2 * pow(length, 2) - 12) + (6 * length),
                                 pow(math.cos(theta), 2) * (2 * pow(length, 2) + 12) - 12,
                                 -12 * pow(math.cos(theta), 2) * length + math.sin(theta) * math.cos(theta) * (
                                             12 - 4 * pow(length, 2)) + (6 * length),
                                 pow(math.cos(theta), 2) * (4 * pow(length, 2) - 12) - 12 * math.sin(theta) * math.cos(
                                     theta) * length + 12]])

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
            if abs(Bx-Ax) < 0.000001 and By-Ay > 0:
                theta = (math.pi/2)
            elif abs(Bx-Ax) < 0.000001 and By-Ay < 0:
                theta = -(math.pi/2)
            else:
                theta = math.atan((By - Ay) / (Bx - Ax))
            k = self.localBeam(length, theta)
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
        variables from the equations relating displacement to load
        :return: Void
        """
        kglobal = copy.deepcopy(self.kglobal)
        loads = copy.deepcopy(self.loads)
        removed_one = []
        for i in range(len(self.fixedNodes)):
            removed_one.append(self.fixedNodes[i] * 2)
            removed_one.append(self.fixedNodes[i] * 2 + 1)

        removed_one.sort(reverse=True)
        for pos in removed_one:
            kglobal = numpy.delete(kglobal, (pos), axis=0)
            kglobal = numpy.delete(kglobal, (pos), axis=1)
            loads = numpy.delete(loads, (pos), axis=0)

        zeroCols = numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)
        zeroRows = numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)

        kglobal = kglobal[:, ~numpy.all(numpy.abs(kglobal) < 1e-5, axis=0)]
        kglobal = kglobal[~numpy.all(numpy.abs(kglobal) < 1e-5, axis=1)]

        removed = copy.deepcopy(removed_one)
        removed.reverse()

        for row in range(len(zeroRows)):
            if zeroRows[row]:
                loads = numpy.delete(loads, (row))
                removed_one.append(row)
        for col in range(len(zeroCols)):
            if zeroCols[col]:
                load = numpy.degrees(load, (col))
                removed_one.append(col)

        return kglobal, loads, removed_one

    def computeDisplacements(self):
        """
        Solves the system using the given parameters
        :return: Returns the displacement of each node in the x and y coordinates
        """
        kglobal, loads, removed_one = self.applyBoundaryConditions()
        allDisplacements = numpy.zeros(len(self.nodes) * 2)
        a = kglobal
        displacements = numpy.matmul(numpy.linalg.inv(a), loads)
        i = 0
        for idx in range(len(allDisplacements)):
            if idx in removed_one:
                allDisplacements[idx] = 0
            else:
                allDisplacements[idx] = displacements[0]
                displacements = displacements[1:]
        print (allDisplacements)
        return allDisplacements

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
                                              globalDisplacements[2*nodeB+1]], dtype=numpy.float64)
        length = math.sqrt((math.pow(Ax - Bx, 2) + math.pow(Ay - By, 2)))
        theta = math.radians(math.atan(By - Ay / (Bx - Ax)))
        stresses.append(self.modulus * numpy.matmul(numpy.matmul(numpy.array([-1/length, 1/length]),
                                                 [[math.cos(theta), math.sin(theta), 0, 0],
                                                  [0,0, math.cos(theta), math.sin(theta)]]),
                                    localDisplacements))



#s = System(modulus=200e9, area=4e-4, nodes=[(0,0),(3,0),(6,0)],
#            fixedNodes=[0,2], connectivity=[(0,1),(1,2)], loads=[load(-10000,'x',1), load(10000,'y', 1)])
#print(s.computeDisplacements())