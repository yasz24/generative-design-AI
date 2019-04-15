class ExtractSubStructures:
	def constructGraph(self, assignment):
		graph = {}
		for key in structure:
			if not tuple(structure[key][0]) in graph:
				graph[tuple(structure[key][0])] = []

			if not tuple(structure[key][1]) in graph:
				graph[tuple(structure[key][1])] = []

		for key in structure:
			graph[tuple(structure[key][0])].append([tuple(structure[key][0]), tuple(structure[key][1])])
			graph[tuple(structure[key][1])].append([tuple(structure[key][0]), tuple(structure[key][1])])

		return graph

	def extractSubStructures(self, assignment):
		graph = self.constructGraph(assignment)

		subStructures = {}

		for vertex in graph:
			initialNode = Node(vertex, [], 0)
			frontierStates = []
			frontier = Stack()
			frontier.push(initialNode)
			frontierStates.append(vertex)
			explored = {}

			for j in range(3, len(assignment) + 1):
				while True:
					if frontier.isEmpty():
						break

					cur_node = frontier.pop()
					frontierStates.pop()
					explored[cur_node.state] = True
					if vertex == cur_node.state and cur_node.cost == j:
						if j in subStructures:
							#need to remove duplicates
							#write make structure
							subStructures[j].append(self.makeStructure(cur_node.path))
						else:
							subStructures[j] = []
							subStructures[j].append(self.makeStructure(cur_node.path))
						continue
					for edge in problem.getSuccessors(cur_node.state):
						next_state, action, cost = successor
						if not (next_state in explored):
							updatePath = []
							updatePath.extend(cur_node.path)
							updatePath.append(action)
							next_node = Node(next_state, updatePath, cost)
							frontier.push(next_node)
							frontierStates.append(next_state)





class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state


class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


