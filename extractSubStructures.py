from util import *

class ExtractSubStructures:
	def constructGraph(self, assignment):
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
					print("j = {}".format(j))
					print("cur_node cost = {}".format(cur_node.cost))
					if cur_node.cost > j :
						continue
					print("vertex {}".format(vertex))
					print("cur_node.state {}".format(cur_node.state))
					print(vertex == cur_node.state)
					if vertex == cur_node.state and cur_node.cost == j:
						print("append to subStructures")
						if j in subStructures:
							#need to remove duplicates
							#write make structure
							subStructures[j].append(cur_node.path)
						else:
							subStructures[j] = []
							subStructures[j].append(cur_node.path)
						continue
					for edge in graph[cur_node.state]:
						if edge[0] == cur_node.state:
							next_state = edge[1]
						else:
							next_state = edge[0]
						cost = cur_node.cost+1
						if not (next_state in explored) or next_state == vertex:
							updatePath = []
							updatePath.extend(cur_node.path)
							updatePath.append(edge)
							next_node = Node(next_state, updatePath, cost)
							print("new node--state:{}, path:{}, cost:{}".format(next_node.state, next_node.path, next_node.cost))
							frontier.push(next_node)
							frontierStates.append(next_state)
		print("here")
		return subStructures


structure = {"beam0": [[0, 0], [4, 0]], "beam1": [[4, 0], [4, 4]], "beam2": [[4, 4], [0, 4]], "beam3": [[0, 4], [0, 0]], "beam4": [[0, 4], [4, 0]], "beam5": [[0,0], [4,0]]}

print(ExtractSubStructures().extractSubStructures(structure))