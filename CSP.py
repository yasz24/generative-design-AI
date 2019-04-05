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
		#use finite solver to see if the assignment is good so far.
		return True
        maxRight = (0,0)
        for idx in range(len(nodes)):
            if nodes[idx] > maxRight[idx] and nodes[idx] == 0:
                maxRight = idx
        fixedNodes = [(nodes.index[(0,0)], idx)]
        system = System(modulus=200e9, area=10e-6, nodes=nodes, fixedNodes=fixedNodes)




csp = CSP(5, 0)

