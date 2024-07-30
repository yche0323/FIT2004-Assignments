from math import floor, ceil, inf


class Node:
    def __init__(self, index=None):
        self.capacity = []
        self.target_node = []
        self.index = index

    def addCapacity(self, c):
        self.capacity.append(c)

    def addTargetNode(self, t):
        self.target_node.append(t)


class FlowNetwork:
    def __init__(self, data):
        self.data = data
        self.no_people = len(data[0])
        self.days = len(data)
        self.no_meals = 2 * self.days
        self.no_selector = 0
        self.selectors = []
        self.lower = floor(0.36 * self.days)
        self.upper = ceil(0.44 * self.days)
        self.upper_order = floor(0.1 * self.days)
        self.housemates = [Node(i) for i in range(self.no_people + 1)]
        self.meals = [Node(i) for i in range(self.no_meals)]
        self.origin = Node()
        self.source = Node()
        self.sink = Node()
        self.sink.addCapacity(self.no_meals)

        self.construct_graph()
        self.graph = self.source

    def construct_graph(self):
        # adding the housemates' nodes to the graph
        for i in range(self.no_people):
            housemate = self.housemates[i]
            housemate.addCapacity(self.upper - self.lower)
            self.origin.addTargetNode(housemate)
            housemate.addCapacity(self.lower)
            self.source.addTargetNode(housemate)

        # adding the origin node to the graph
        origin_demand = -self.no_meals + self.no_people * self.lower
        self.source.addTargetNode(self.origin)
        self.origin.addCapacity(abs(origin_demand))

        # adding the order node to the graph
        order = self.housemates[self.no_people]
        order.addCapacity(self.upper_order)
        self.origin.addTargetNode(order)

        # adding the selector and meal nodes to the graph
        for i in range(self.days):
            for j in range(self.no_people):
                meal = self.data[i][j]
                if meal != 0:
                    # creating a selector node
                    selector = Node()
                    self.no_selector += 1
                    selector.addCapacity(1)

                    # if the housemate is free for that day's breakfast, add it to the housemate's selector
                    if meal == 1:
                        breakfast = self.meals[i * 2]
                        breakfast.addCapacity(1)
                        selector.addTargetNode(breakfast)
                    # if the housemate is free for that day's dinner, add it to the housemate's selector
                    elif meal == 2:
                        dinner = self.meals[i * 2 + 1]
                        dinner.addCapacity(1)
                        selector.addTargetNode(dinner)
                    # if the housemate is free for that day's breakfast and dinner, add them to the housemate's selector
                    else:
                        breakfast = self.meals[i * 2]
                        breakfast.addCapacity(1)
                        selector.addTargetNode(breakfast)
                        dinner = self.meals[i * 2 + 1]
                        dinner.addCapacity(1)
                        selector.addTargetNode(dinner)

                    self.housemates[j].addTargetNode(selector)
                    self.selectors.append(selector)

        # connecting the order node to every meal and every meal to the sink node
        for i in range(self.no_meals):
            self.housemates[self.no_people].addTargetNode(self.meals[i])
            self.meals[i].addCapacity(1)
            self.meals[i].addTargetNode(self.sink)


def dfs(source, path):
    # Base Case: reaches the sink
    if len(source.target_node) == 0 and source.index is None:
        path.append(source)
        return True
    else:
        sink_found = False
        i = 0
        while i < len(source.target_node) and sink_found is False:
            c = 0
            if source.target_node[i].index is not None and len(source.capacity) == 0:
                c = 1

            if source.target_node[i].capacity[c] > 0:
                sink_found = dfs(source.target_node[i], path)
                if sink_found:
                    path.append(source)
            i += 1

    return sink_found


def ford_fulkerson(G):
    source = G.source
    max_flow = 0
    allocated = ([-1] * G.days, [-1] * G.days)
    path = []

    while dfs(source, path):
        # the minimum path flow will always be 1
        path_flow = 1

        x = 2

        if path[len(path) - 2].index is None:
            path[len(path) - 2].capacity[0] -= path_flow
            path[len(path) - 3].capacity[0] -= path_flow
            x = 3
        else:
            path[len(path) - 2].capacity[1] -= path_flow

        for n in range(len(path) - x):
            path[n].capacity[0] -= path_flow

        max_flow += path_flow

        # last element in the path will either be one of the housemates' node or the origin node
        if path[len(path) - 2].index is not None:
            i = path[len(path) - 2].index
        else:
            i = path[len(path) - 3].index

        # second element in the path will always one of the meals' node
        j = path[1].index
        # if the index is an even number it will be a breakfast
        if j % 2 == 0:
            allocated[0][floor(j / 2)] = i
        else:
            allocated[1][floor(j / 2)] = i

        path = []

    return max_flow, allocated


def allocate(availability):
    # if the data is empty, return empty table
    if len(availability) > 0:
        # constructing the graph
        G = FlowNetwork(availability)
        # performing Ford Fulkerson's Algorithm
        max_flow, allocated = ford_fulkerson(G)
        # if there are no feasible solution
        if max_flow < 2 * len(availability):
            return None
        else:
            return allocated
    else:
        return [], []


availability = [[1, 2, 2, 2, 0], [2, 1, 2, 0, 2], [2, 0, 1, 0, 2], [2, 0, 1, 0, 2], [1, 2, 2, 0, 0], [2, 0, 0, 1, 2],
                [1, 2, 0, 2, 0], [2, 1, 0, 0, 0], [1, 2, 2, 0, 0], [0, 2, 0, 2, 1], [0, 2, 0, 2, 1]]

print(allocate(availability))
