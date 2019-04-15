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
        print(graph)
        return graph

    def extractSubStructures(self, assignment):
        graph = self.constructGraph(assignment)
        subStructures = {}
        for vertex in graph:
            print("vertex")
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
                    if cur_node.cost > j :
                        continue
                    if vertex == cur_node.state and cur_node.cost == j:
                        if j in subStructures:
                            #need to remove duplicates
                            # #write make structure
                            subStructures[j].append(cur_node.path)
                        else:
                            subStructures[j] = []
                            subStructures[j].append(cur_node.path)
                        continue
                    for edge in graph[vertex]:
                        if edge[0] == cur_node.state:
                            next_state = edge[1]
                        else:
                            next_state = edge[0]
                        cost = cur_node.cost+1
                        if not (next_state in explored):
                            updatePath = []
                            updatePath.extend(cur_node.path)
                            updatePath.append(edge)
                            next_node = Node(next_state, updatePath, cost)
                            frontier.push(next_node)
                            frontierStates.append(next_state)
        print("here")
        return subStructures

structure = {'beam0': ((0, 0), (1, 2)), 'beam1': ((1, 2), (2, 2)), 'beam2': ((2, 2), (3, 2)),'beam3': ((3, 2), (0, 0)), 'beam4': ((0, 0), (2, 2)), 'beam5': ((2, 2), (0, 3)), 'beam6': ((0, 3), (3, 2)), 'beam7': ((3, 2), (1, 2)), 'beam8': ((1, 2), (0, 3)), 'beam9': ((0, 3), (0, 0))}
print(ExtractSubStructures().extractSubStructures(structure))
