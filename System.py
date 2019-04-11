import numpy as np
import math
import itertools
import copy
from Force import Load

class System:

    def __init__(self, modulus, area, inertia, nodes, fixedNodes, connectivity, loads):
        """
        :param modulus: Modulus of the elements
        :param area: Area of the elements
        :param nodes: List of the nodes in the system
        :param fixedNodes: List of numbers of nodes that are fixed in the system
        :param connectivity: List of pairs of position
        :param loads: List of the loads on the system
        :param displacements: the displacements of the nodes
        """
        self.degreesOfFreedom = 3
        self.nodes = nodes
        self.fixedNodes = fixedNodes
        self.loads = np.zeros((len(self.nodes) * self.degreesOfFreedom, 1))
        self.addloads(loads)
        self.kglobal = np.zeros((len(self.nodes) * self.degreesOfFreedom, len(self.nodes) * self.degreesOfFreedom))
        self.connectivity = connectivity
        self.modulus = modulus
        self.area = area
        self.inertia = inertia
        self.assemble()

    def addloads(self, loads):
        """
        Adds a load to the system
        :param loads: A load object
        :return: Void
        """
        self.loads = np.zeros((len(self.nodes) * self.degreesOfFreedom, 1))
        for load in loads:
            if load.getDirection() == 'x':
                self.loads[self.degreesOfFreedom * load.getNode()] += load.getMagnitude()
            elif load.getDirection() == 'y':
                self.loads[self.degreesOfFreedom * load.getNode() + 1] += load.getMagnitude()
            elif load.getDirection() == 'k':
                self.loads[self.degreesOfFreedom * load.getNode() + 2] += load.getMagnitude()
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
        return ((self.modulus * self.area) / length) * np.array([[pow(math.cos(theta), 2), math.cos(theta)
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
                                                                  pow(math.sin(theta), 2)]], dtype=np.float64)
    def localBeam(self, length, theta):
        inertia = self.inertia
        klocal = (self.modulus)/length * np.array([[self.area*pow(np.cos(theta),2)+(12*inertia*pow(np.sin(theta),2))/(pow(length,2)),
                            (self.area-(12*inertia)/(pow(length,2))) * np.cos(theta) * np.sin(theta),
                            (-6*inertia*np.sin(theta))/length,
                            -1*(self.area*pow(np.cos(theta), 2) + (12*inertia*pow(np.sin(theta),2))/(pow(length,2))),
                            -1*(self.area-(12*inertia)/pow(length ,2))*np.cos(theta)*np.sin(theta),
                            (-6 * inertia * np.sin(theta)) / length],
                            [(self.area-(12*inertia)/(pow(length,2))) * np.cos(theta) * np.sin(theta),
                             (self.area*pow(np.sin(theta),2)+(12*inertia*pow(np.cos(theta),2))/pow(length,2)),
                             (6*inertia*np.cos(theta))/length,
                             -(self.area-(12*inertia)/pow(length,2))*np.cos(theta)*np.sin(theta),
                             -(self.area*pow(np.sin(theta),2)+(12*inertia*pow(np.cos(theta),2))/pow(length,2)),
                             (6*inertia*np.cos(theta))/length],
                            [(-6*inertia*np.sin(theta))/length,
                             (6 * inertia * np.cos(theta)) / length,
                             4*inertia,
                             (6*inertia*np.sin(theta))/length,
                             (-6*inertia*np.cos(theta))/length,
                             (2*inertia)],
                            [ -1*(self.area*pow(np.cos(theta), 2) + (12*inertia*pow(np.sin(theta),2))/(pow(length,2))),
                              -(self.area - (12 * inertia) / pow(length, 2)) * np.cos(theta) * np.sin(theta),
                              (6 * inertia * np.sin(theta)) / length,
                              (self.area*pow(np.cos(theta),2)+(12*inertia*pow(np.sin(theta),2))/pow(length,2)),
                              (self.area-(12*inertia)/pow(length,2))*np.cos(theta)*np.sin(theta),
                              (6*inertia*np.sin(theta))/length],
                            [ -1*(self.area-(12*inertia)/pow(length ,2))*np.cos(theta)*np.sin(theta),
                              -(self.area * pow(np.sin(theta), 2) + (12 * inertia * pow(np.cos(theta), 2)) / pow(length,2)),
                              (-6 * inertia * np.cos(theta)) / length,
                              (self.area - (12 * inertia) / pow(length, 2)) * np.cos(theta) * np.sin(theta),
                              self.area*pow(np.sin(theta),2)+(12*inertia*pow(np.cos(theta),2))/pow(length,2),
                              -(6*inertia*np.cos(theta))/length],
                            [(-6 * inertia * np.sin(theta)) / length,
                             (6 * inertia * np.cos(theta)) / length,
                             (2 * inertia),
                             (6 * inertia * np.sin(theta)) / length,
                             -(6 * inertia * np.cos(theta)) / length,
                             4*inertia]])
        return klocal

    def assemble(self):
        """
        Takes the information about the nodes in 3d space and the connevtivity of each node
        and creates a stiffness matrix for the system
        :return: np Array
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
            indexes = [self.degreesOfFreedom * nodeA + dof for dof in range(self.degreesOfFreedom)] + \
                      [self.degreesOfFreedom * nodeB + dof for dof in range(self.degreesOfFreedom)]
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
            removed_one.append(self.fixedNodes[i] * self.degreesOfFreedom)
            removed_one.append(self.fixedNodes[i] * self.degreesOfFreedom + 1)
            removed_one.append(self.fixedNodes[i] * self.degreesOfFreedom + 2)

        removed_one.sort(reverse=True)
        for pos in removed_one:
            kglobal = np.delete(kglobal, (pos), axis=0)
            kglobal = np.delete(kglobal, (pos), axis=1)
            loads = np.delete(loads, (pos), axis=0)

        zeroCols = np.all(np.abs(kglobal) < 1e-5, axis=0)
        zeroRows = np.all(np.abs(kglobal) < 1e-5, axis=1)

        kglobal = kglobal[:, ~np.all(np.abs(kglobal) < 1e-5, axis=0)]
        kglobal = kglobal[~np.all(np.abs(kglobal) < 1e-5, axis=1)]

        removed = copy.deepcopy(removed_one)
        removed.reverse()

        for row in range(len(zeroRows)):
            if zeroRows[row]:
                loads = np.delete(loads, (row))
                removed_one.append(row)
        for col in range(len(zeroCols)):
            if zeroCols[col]:
                load = np.degrees(load, (col))
                removed_one.append(col)

        return kglobal, loads, removed_one

    def computeDisplacements(self):
        """
        Solves the system using the given parameters
        :return: Returns the displacement of each node in the x and y coordinates
        """
        kglobal, loads, removed_one = self.applyBoundaryConditions()
        allDisplacements = np.zeros(len(self.nodes) * self.degreesOfFreedom)
        displacements = np.matmul(np.linalg.inv(kglobal), loads)
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
            localDisplacements = np.array([globalDisplacements[2 * nodeA],
                                              globalDisplacements[2*nodeA+1],
                                              globalDisplacements[2*nodeB],
                                              globalDisplacements[2*nodeB+1]], dtype=np.float64)
        length = math.sqrt((math.pow(Ax - Bx, 2) + math.pow(Ay - By, 2)))
        theta = math.radians(math.atan(By - Ay / (Bx - Ax)))
        stresses.append(self.modulus * np.matmul(np.matmul(np.array([-1/length, 1/length]),
                                                 [[math.cos(theta), math.sin(theta), 0, 0],
                                                  [0,0, math.cos(theta), math.sin(theta)]]),
                                    localDisplacements))



s = System(modulus=30e3, area=100, inertia=1000, nodes=[(0,0),(360,360),(840,360)],
            fixedNodes=[0,2], connectivity=[(0,1),(1,2)], loads=[Load(10000,'x',1)])
print(s.computeDisplacements())