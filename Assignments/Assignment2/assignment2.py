import math
import heapq


# Question 1
class RoadGraph:
    def __init__(self, roads: list, cafes: list) -> None:
        """
        graph is an adjacency list representation of the RoadGraph
        The index of the graph will be the starting point,
        And it contains a tuple for every route from that starting point.
        The first element of the tuple will be the destination point,
        While the second element of the tuple will be the time taken to travel that particular route
        Time Complexity: O(|V|+|E|)
        Aux Space Complexity: O(|V|+|E|)

        :param roads: a list of roads
        :param cafes: a list of cafes
        """
        self.graph = []
        self.construct_graph(roads, cafes)
        self.cafes = cafes

    def routing(self, start: int, end: int) -> list:
        """
        This function will be responsible to iterate through each cafe to find the minimum time spent on travelling
        From the starting point to the ending point while passing by at least one cafe (including the waiting time)
        In this function, we will be using the Dijkstra's algorithm to find the shortest path from the starting point
        To one of the cafes that has the least travelling time and waiting time, then using the same algorithm
        We will find the shortest path from the cafe to the destination point.
        Time Complexity: O(|E|log|V|)
        Aux Space Complexity: O(|V|+|E|)

        :param start: given starting point of the route
        :param end: given destination point of the route
        :return:
        """
        shortest_time = math.inf
        route = []

        for i in range(len(self.cafes)):
            cafe = self.cafes[i][0]
            cafe_wait_time = self.cafes[i][1]
            # checking if the starting point and the cafe location are the same
            if start == cafe:
                start_cafe = [0, []]
            else:
                start_cafe = self.dijkstra_algo(start, cafe)
            # checking if the destination point and the cafe location are the same
            if end == cafe:
                cafe_end = [0, []]
            else:
                cafe_end = self.dijkstra_algo(cafe, end)
            # if a shorter time is found, re-initialise the route
            time_taken = start_cafe[0] + cafe_end[0] + cafe_wait_time
            if time_taken < shortest_time:
                shortest_time = time_taken
                route = [start] + start_cafe[1] + cafe_end[1]

        if len(route) <= 0:
            route = None

        return route

    def construct_graph(self, roads: list, cafes: list) -> None:
        """
        This function will be responsible for constructing the RoadGraph with every route in the road list
        Time Complexity: O(|V|+|E|)
        Aux Space Complexity: O(|V|+|E|)

        :param roads: a list of roads
        :param cafes: a list of cafes
        :return: constructing the RoadGraph
        """
        for i in range(len(roads)):
            self.add_vertex(roads[i][0])
            self.add_edge(roads[i][0], roads[i][1], roads[i][2])

        for i in range(len(cafes)):
            self.add_vertex(cafes[i][0])

    def add_vertex(self, V: int) -> None:
        """
        This function will be responsible for adding vertices into the graph
        It will first check if the vertex exists in the graph,
        Then it will only add the vertex into the graph if it does not exist
        Time Complexity: Worst Case is O(|V|), when the graph is empty, and it will add from vertex 0 to vertex V
        Aux Space Complexity: O(|V|)

        :param V: the vertex to be added
        :return: adding vertices into the graph
        """
        try:
            self.graph[V]
        except IndexError:
            for _ in range(len(self.graph), V + 1):
                self.graph.append([])

    def add_edge(self, u, v, w) -> None:
        """
        This function will be responsible for adding edges between the vertices
        It will append the destination point of the route and time taken to travel that route as a tuple,
        To the starting point of route which is represented by the index of the graph
        Time Complexity: O(|E|)
        Aux Space Complexity: O(|E|)

        :param u: starting point of the route
        :param v: destination point of the route
        :param w: time taken to travel from the starting point to the destination point of the route
        :return: adding edges between the vertices
        """
        if self.graph[u] is not None:
            self.graph[u].append((v, w))
        else:
            raise Exception("This vertex does not exist in the adjacency list")

    def dijkstra_algo(self, start: int, end: int) -> list:
        """
        This function will be responsible to apply Dijkstra's algorithm to find the shortest path between two points.
        It will calculate all possible routes from the starting point to each node
        By iterating through every node in the graph,
        And find the shortest path between the starting point to each node in the graph.
        citation:
        - Week 5 lecture note (for Dijkstra's algorithm pseudocode)
        - https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/ (for using the heappop and heappush concept)
        Time Complexity: O(|E|log|V|),
                         Since O(|E|) dominates O(|V|), hence O(|E|log|V|+|V|log|V|) can be written as O(|E|log|V|)
        Aux Space Complexity: O(|V|+|E|)

        :param start: given starting point of the route
        :param end: given destination point of the route
        :return:
        """
        queue = [(0, start)]
        pred = [None] * len(self.graph)
        dist = [math.inf] * len(self.graph)
        dist[start] = 0

        # finding the shortest path from starting point to the ending point
        while len(queue) > 0:
            node = heapq.heappop(queue)
            u = node[1]
            for v in range(len(self.graph[u])):
                curr_node = self.graph[u][v]
                curr_node_dist = dist[u] + curr_node[1]
                if curr_node_dist < dist[curr_node[0]]:
                    dist[curr_node[0]] = curr_node_dist
                    pred[curr_node[0]] = u
                    heapq.heappush(queue, (curr_node_dist, curr_node[0]))

        # returning the shortest path along with the time taken to travel that path
        v = end
        path_dist = dist[v]
        path = [v]
        while v != start:
            if pred[v] is not None:
                if pred[v] != start:
                    path = [pred[v]] + path
                v = pred[v]
            else:
                v = start
                path = []

        route = [path_dist, path]
        return route


# Question 2
def optimalRoute(downhillScores: list, start: int, finish: int) -> list:
    """
    In this function, we will be using the Depth-First Search(DFS) algorithm to find the path that returns the max score

    Time Complexity: O(|D|),
                     Since O(|D|) dominates O(|P|), hence O(|D|+|P|) is equivalent to O(|D|)
    Aux Space Complexity: O(|D|*|P|)

    :param downhillScores: a list of
    :param start:
    :param finish:
    :return:
    """
    graph = construct_graph(downhillScores)
    visited = [[]] * len(graph)
    path = dfsDP(visited, graph, start, finish)
    route = path[1]

    if len(route) <= 0:
        route = None

    return route


def construct_graph(raw_data: list) -> list:
    """
    This function will be responsible to construct an adjacency list of a given set of raw data.
    Time Complexity: O(|D|)
    Aux Space Complexity: O(|D|+|P|)

    :param raw_data:
    :return:
    """
    graph = []
    # adding vertices
    for i in range(len(raw_data)):
        try:
            graph[raw_data[i][0]]
        except IndexError:
            for _ in range(len(graph), raw_data[i][0] + 1):
                graph.append([])
        try:
            graph[raw_data[i][1]]
        except IndexError:
            for _ in range(len(graph), raw_data[i][1] + 1):
                graph.append([])

    # adding edges
    for i in range(len(raw_data)):
        if graph[raw_data[i][0]] is not None:
            graph[raw_data[i][0]].append([raw_data[i][1], raw_data[i][2]])
        else:
            raise Exception("This vertex does not exist in the adjacent list")

    return graph


def dfsDP(visited: list, graph: list, curr_node: int, finish: int) -> list:
    """
    This function will be responsible to perform the DFS algorithm using the Dynamic Programming approach.
    It will iterate through all the neighbour nodes by performing recursive calls,
    Starting from the source node, and ends when the target node is found.
    Time Complexity: O(|D|),
                     Since O(|D|) dominates O(|P|), hence O(|D|+|P|) is equivalent to O(|D|)
    Aux Space Complexity: O(|D|*|P|)

    :param visited: a list to check if the current node have been visited
    :param graph: an adjacency list of the given data
    :param curr_node: the node that is currently getting iterated
    :param finish: the target node
    :return: a list of all the nodes from the source node to the target node that gives the maximum score
    """
    dfs = [-math.inf, []]
    temp = []

    # if current node is not finish
    if curr_node != finish:
        # if current node has no outgoing path
        if len(graph[curr_node]) == 0:
            return dfs
        # if current node has outgoing path
        else:
            # loop all the outgoing path
            for i in range(len(graph[curr_node])):
                next_node = graph[curr_node][i][0]
                next_score = graph[curr_node][i][1]
                # if a node is visited, then it should return either that node's path with the max score,
                # Or returns -inf with an empty array if the target node cannot be found while traversing that node
                if len(visited[next_node]) > 0 and visited[next_node][0] != -math.inf:
                    if visited[next_node][0] > dfs[0]:
                        dfs[0] = visited[next_node][0] + next_score
                        temp = visited[next_node][1]
                else:
                    dfs_next = dfsDP(visited, graph, next_node, finish)
                    # if the len(dfs_next[1]) == 0, this means that the path has reached the end,
                    # and the finish point could not be found
                    if len(dfs_next[1]) > 0:
                        # popping the element
                        if dfs_next[0] + next_score > dfs[0]:
                            dfs[0] = dfs_next[0] + next_score
                            temp = dfs_next[1]
    else:
        return [0, [curr_node]]

    if len(temp) > 0:
        dfs[1] = [curr_node] + temp
        visited[curr_node] = [dfs[0], dfs[1]]
    else:
        visited[curr_node] = [-math.inf, []]

    return dfs
