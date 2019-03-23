class CSP:
	def __init__(self, grid_size, discConstant):
		self.variables = self.initializeVariables(grid_size)
		self.domain = self.initializeDomain(grid_size)
		self.constraints = self.checkConstraints()
		self.discConstant = 1


	def initializeVariables(self, grid_size):
		temp = []
		for i in range(grid_size):
			beam = "beam" + i
			temp.append(beam)
		return temp

	def initializeDomain(self, grid_size):
		domains = {}
		startPos = (0,0)
		for beam in self.variables:
			domains[beam] = [[]]

		#array for beam0
		array1 = []
		for i in range(grid_size):
			(startPos, (i,grid_size-1))
		domains["beam0"] = [array1]
		
		curBeam = 1
		top = False
		while curBeam < grid_size: 
			oldbeam = "beam" + (curBeam -1)
			newbeam = "beam" + curBeam
			prevMapValue =  domains[oldbeam]
			newMapValue = domains[newbeam]

			startPositions = []
			for tup in prevMapValue:
				startPositions.append(tup[1])

			for startPosition in startPositions:
				temp = []
				if top:
					for i in range(grid_size):
						(startPosition, (i, grid_size-1))
				else:
					for i in range(grid_size):
						(startPosition, (i, 0))
			top = not top
			curBeam+=1
		return domains

	def checkConstraints()


