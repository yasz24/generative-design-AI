from util import *
import json
from featureExtractor import *

class ExtractSubStructures:
	def __init__(self):
		self.features = []
		self.targets = []
	def constructGraph(self, structure):
		graph = {}
		for key in structure:
			if not tuple(structure[key][0]) in graph:
				graph[tuple(structure[key][0])] = []

			if not tuple(structure[key][1]) in graph:
				graph[tuple(structure[key][1])] = []

		for key in structure:
			graph[tuple(structure[key][0])].append((tuple(structure[key][0]), tuple(structure[key][1])))
			graph[tuple(structure[key][1])].append((tuple(structure[key][0]), tuple(structure[key][1])))

		return graph

	def extractSubStructures(self, assignment):
		graph = self.constructGraph(assignment)

		subStructures = {}

		for vertex in graph:
			for j in range(3, len(assignment) + 1):
				initialNode = Node(vertex, [], 0)
				frontierStates = []
				frontier = Stack()
				frontier.push(initialNode)
				frontierStates.append(vertex)
				explored = {}
				while True:
					if frontier.isEmpty():
						break

					cur_node = frontier.pop()
					frontierStates.pop()
					explored[cur_node.state] = True
					#print("j = {}".format(j))
					#print("cur_node cost = {}".format(cur_node.cost))
					if cur_node.cost > j :
						continue
					#print("vertex {}".format(vertex))
					#print("cur_node.state {}".format(cur_node.state))
					#print(vertex == cur_node.state)
					if vertex == cur_node.state and cur_node.cost == j:
						#print("append to subStructures")
						if j in subStructures:
							#need to remove duplicates
							#write make structure
							subStructures[j].append(cur_node.path)
						else:
							subStructures[j] = []
							subStructures[j].append(cur_node.path)
						continue
					for edge in graph[cur_node.state]:
						#print("edge: {}".format(edge))

						if edge[0] == cur_node.state:
							next_state = edge[1]
						else:
							next_state = edge[0]
						cost = cur_node.cost+1
						if not (next_state in explored) or (next_state == vertex and not edge in cur_node.path):
							updatePath = []
							updatePath.extend(cur_node.path)
							updatePath.append(edge)
							next_node = Node(next_state, updatePath, cost)
							#print("new node--state:{}, path:{}, cost:{}".format(next_node.state, next_node.path, next_node.cost))
							frontier.push(next_node)
							frontierStates.append(next_state)
		#print("here")
		return subStructures

	def assignmentToSubstructureFeatures(self, assignment):
		featureExtractor = FeatureExtractorUtil()
		target = featureExtractor.extractTargets(assignment)
		formattedSubstructures = []
		allSubStructures = self.extractSubStructures(assignment)
		for structureSize in allSubStructures:
			subStructures = allSubStructures[structureSize]
			for subStructure in subStructures:
				formattedDict = {}
				for i in range(len(subStructure)):
					beam = "beam" + str(i)
					formattedDict[beam] = subStructure[i]
				formattedSubstructures.append(formattedDict)
		for formattedSubStructure in formattedSubstructures:
			features = featureExtractor.extractFeatures(formattedSubStructure)
			self.features.append(features)
			self.targets.append(target)

	def createRegressionData(self, dataSet):
		data = [json.loads(line) for line in open(dataSet)]
		for datapoint in data:
			self.assignmentToSubstructureFeatures(datapoint)

	def getFeatures(self):
		return self.features

	def getTargets(self):
		return self.targets


#structure = {'beam0': ((0, 0), (1, 2)), 'beam1': ((1, 2), (2, 2)), 'beam2': ((2, 2), (3, 2)), 'beam3': ((3, 2), (0, 0)), 'beam4': ((0, 0), (2, 2)), 'beam5': ((2, 2), (0, 3)), 'beam6': ((0, 3), (3, 2)), 'beam7': ((3, 2), (1, 2)), 'beam8': ((1, 2), (0, 3)), 'beam9': ((0, 3), (0, 0))}
#substructures = ExtractSubStructures().extractSubStructures(structure)
#count = 0
#for sizes in substructures:
#	for substructure in substructures[sizes]:
#		count += 1
#print (count)

#e.createRegressionData("Database.txt")
#features = e.getFeatures()
#print("Feature length"),
#print(len(features))