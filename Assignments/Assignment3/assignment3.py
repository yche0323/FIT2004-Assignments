from math import floor, ceil, inf


# Task 1
def bfs(graph, source, sink, parent):
    """
    This function will be using the Breadth-First Search algorithm to visit every node in the graph
    It will return True if the sink node is visited and False otherwise

    Time Complexity: O(n^2), where n is the number of days;
    :param graph: the graph to travers
    :param source: the source node
    :param sink: the sink node
    :param parent: the parent to keep track of each node's parent node
    :return: True or False based on the outcome of the algorithm
    """
    # setting initial values
    visited = [False] * len(graph)

    # visiting the source node
    queue = [source]
    visited[source] = True

    while len(queue) > 0:
        # popping the first node in the queue
        u = queue.pop(0)

        # looping all the nodes from u
        for i, value in enumerate(graph[u]):
            # if this node is not visited and there is an edge from u, then we visit this node
            if visited[i] is False and value > 0:
                queue.append(i)
                visited[i] = True
                parent[i] = u

    return visited[sink]


def ford_fulkerson(G, source, sink):
    """
    This algorithm uses the Breadth-First Search (BFS) algorithm to traverse every node in the graph
    If the BFS algorithm manages to visit the sink node of the graph, then it will return True, meaning that there is
    still a feasible solution, else it will return False, indicating that it is impossible to have feasible solution.
    After performing a round of BSF algorithm, the parent array, which is used to indicate the parent of each node along
    the path, will be used to traverse once again from sink node to the source node to find the smallest flow path.
    While we are backtracking the path, we could also find the housemate that the path had visited.
    Then the graph will traverse the path once again from the sink node to the source node to fill in the flow capacity
    for each edge to ensure that the function do not run forever.

    Time Complexity: O(n^2), where n is the number of days;
                     Explanation: Since the algorithm uses the BFS algorithm, which travers the graph, which is an
                                  adjacency matrix, in O(n^2) time
    :param G: the class of the graph that represents the processed data
    :param source: the source node
    :param sink: the sink node
    :return: the max flow and the allocated table
    """
    graph = G.graph
    parent = [-1] * len(graph)
    max_flow = 0
    allocated = ([-1] * G.days, [-1] * G.days)

    # uses the Breadth-First Search algorithm to traverse through every node in the graph,
    # if there are no feasible solution it will stop running
    while bfs(graph, source, sink, parent):
        path_flow = inf
        t = sink

        # finding the index of the meal
        j = parent[sink] - G.first_meal
        # initializing variables
        found = False
        i = 0

        # Finding the smallest flow capacity along the path
        while t != source:
            path_flow = min(path_flow, graph[parent[t]][t])
            # while traversing the path, we could also find the housemate on this path
            if found is False:
                # if the parent node of the current one is either an origin or source node, then the housemate is found
                if parent[t] == 1 or parent[t] == source:
                    i = t
                    found = True
            t = parent[t]

        # if we found the housemate,
        if found is True:
            # if the index of the meal is an even number or 0, then it will be a breakfast
            if j % 2 == 0:
                allocated[0][round(j/2)] = i - 2
            # else, a dinner
            else:
                allocated[1][floor(j/2)] = i - 2

        max_flow += path_flow

        s = sink

        # Filling in the flow capacity for each edge
        while s != source:
            u = parent[s]
            graph[u][s] -= path_flow
            graph[s][u] += path_flow
            s = parent[s]

    return max_flow, allocated


class Graph:
    def __init__(self, data):
        """
        This class will construct a graph to represent the data, while storing useful information about the graph
        To process the data into useful information, we will have to represent each housemate and meal as a node in the
        graph. In addition to that, we would also need selector nodes to ensure that no housemate will be allocated
        twice on the same day. We would also have an origin node which limits the upper bound and lower bound of the
        allocation for each housemate. Lastly, to process the data into useful information, we would need to perform
        the Ford-Fulkerson's Algorithm which requires a source node and a sink node in the graph.

        variables:
        no_people will be the total number of housemate
        days will be the number of next n days
        no_meals will be the total number of meals that everyone has to prepare for the next n days
        lower will be the minimum amount of times each housemate gets allocated
        upper will be the maximum amount of times each housemate gets allocated
        upper_order will be the maximum amount of time they can order from a restaurant
        no_selectors will be the total number of selectors
        graph will be the representation of the data
        :param data: the raw data to be processed
        """
        self.data = data
        self.no_people = len(self.data[0]) + 1
        self.days = len(self.data)
        self.no_meals = 2 * self.days
        self.lower = floor(0.36 * self.days)
        self.upper = ceil(0.44 * self.days)
        self.upper_order = floor(0.1 * self.days)
        self.no_selectors = 0

        for i in range(self.days):
            for j in range(self.no_people - 1):
                if self.data[i][j] == 1 or self.data[i][j] == 2:
                    self.no_selectors += 1
                elif self.data[i][j] == 3:
                    self.no_selectors += 2

        # useful variables to access element in the graph
        self.first_housemate = 2  # index of the first housemate in the graph
        self.last_housemate = self.no_people  # index of the last housemate in the graph
        self.order_index = self.no_people + 1  # index of the order in the graph
        self.first_selector = self.no_people + 2  # index of the selector in the graph
        self.last_selector = self.first_selector + self.no_selectors - 1  # index of the last selector in the graph
        self.first_meal = self.last_selector + 1  # index of the first meal in the graph
        self.last_meal = self.first_meal + self.no_meals - 1  # index of the last meal in the graph

        self.graph = self.construct_graph()

    def construct_graph(self):
        """
        This main objective of this function would be to construct a graph that represents the data.

        Approach:
        Firstly, this function will create an adjacency matrix (i.e. the graph) with the total number of nodes we had.

        Starting from the first node in the graph, it will be the source node. Then it will be the origin node, then
        the nodes that represent the housemate, followed by the order from the restaurant, then the nodes that
        represent the meals and lastly the sink node.
        For instance, the first n nodes starting at the index of first_selector will be the selectors for the first
        housemate (if any) depending on the number of free slots for allocation that housemate has.
        For every edge from node u to node v, the flow capacity of the edge will be stored in node u at index v.

        To perform the Ford-Fulkerson's Algorithm we would only need the residual graph. Hence, all the nodes with
        positive demand (i.e. the origin node and the nodes that represent the housemate) will be connected by the
        source node with a flow capacity of that demand, while all the nodes with negative demand (i.e. the nodes that
        represent the meals) will connect to the sink node. As for the order node, it will connect to each node that
        represents the meals.

        For each node representing the housemate it will connect to his or her own selector node (if any) and from that
        selector node, it will point to that housemate's free slot.
        Note:
        1) For each selector it will only represent one of the days, hence there is a possibility that the selector may
           point towards two of the meals on the same day.
        2) For each meal node in the graph, they will be arranged according to the order of the day.
           For instance, it starts from day 1 breakfast followed by day 1 winner, then by day 2 breakfast and day 2
           dinner, and so on.

        :return: the graph that represents the data
        """
        total_nodes = self.no_selectors + self.no_meals + self.no_people + 3
        graph = [[0 for _ in range(total_nodes)] for _ in range(total_nodes)]

        # adding edge from source to origin
        graph[0][1] = self.no_meals

        # adding edge from source to each housemate
        for i in range(self.first_housemate, self.last_housemate + 1):
            graph[0][i] = self.lower

        # adding edge from origin to each housemate
        for i in range(self.first_housemate, self.last_housemate + 1):
            graph[1][i] = self.upper - self.lower

        # adding edge from origin to order
        graph[1][self.order_index] = self.upper_order

        # adding edges from each housemate to their correspond selector, then to the corresponding meal
        k = 0  # act as an offset
        for i in range(self.no_people - 1):
            for j in range(self.days):
                if self.data[j][i] != 0:
                    graph[i + 2][self.first_selector + k] = 1
                    if self.data[j][i] == 1:
                        graph[self.first_selector + k][self.first_meal + 2 * j] = 1
                    elif self.data[j][i] == 2:
                        graph[self.first_selector + k][self.first_meal + 2 * j + 1] = 1
                    else:
                        graph[self.first_selector + k][self.first_meal + 2 * j] = 1
                        graph[self.first_selector + k][self.first_meal + 2 * j + 1] = 1
                    k += 1

        # adding edges from order to each meal
        for i in range(self.first_meal, self.last_meal + 1):
            graph[self.order_index][i] = 1

        # adding edges from each meal to sink
        for i in range(self.first_meal, self.last_meal + 1):
            graph[i][total_nodes - 1] = 1

        return graph


def allocate(availability):
    """
    This function will create a new class for the graph to represent the data and make a function call to perform
    Ford Fulkerson's Algorithm on the graph
    If there are feasible solution, then this function will return None, else it will return the allocation table
    :param availability: the raw data (the availability of the housemates)
    :return: None, if no feasible solution; The allocation table, otherwise
    """
    # if the data is empty, return empty table
    if len(availability) > 0:
        # constructing the graph
        G = Graph(availability)
        # performing Ford Fulkerson's Algorithm
        max_flow, allocated = ford_fulkerson(G, 0, len(G.graph) - 1)
        # if there are no feasible solution
        if max_flow < 2*len(availability):
            return None
        else:
            return allocated
    else:
        return [], []


# Task 2
class Node:
    def __init__(self, label):
        """
        This class is used to represent the node of the suffix tree.
        label will be the characters represented by this node
        char will be the first character of every single child's label
        child will be an array of child node
        delimiter will determine if this node exists in both strings (0 means no, more than 0 means yes)
        curr_max_lcs will be the longest possible string going down this node
        :param label: the characters represented by this node
        """
        self.label = label
        self.char = []
        self.child = []
        self.delimiter = [0, 0]
        self.curr_max_lcs = ""


class SuffixTree:
    def __init__(self, string1, string2):
        """
        This class will represent the suffix tree of a given string
        root will be the root node of this tree
        string will be the given string with a "$" sign
        max_lcs will be used to store the longest common substring of the two strings when we compare the strings
        Approach:
        To construct this suffix tree, we will use the naive approach where we will insert each suffixes one by one

        Time Complexity: O((N + M^)2), where N + M is the total length of the given string;
                         Explanation: Since addSuffix() runs at O(N + M) in the worst case, and N + M is the total
                                      number of suffixes of the two combined string, hence adding the suffixes one by
                                      one to the suffix tree will cost O((N + M^)2)
                                      And constructing for two string will have a cost of O((N + M)^2)
        Space Complexity: O((N + M^)2), where N + M is the total length of the given string;
                          Explanation: Since a string of length N + M has N + M suffixes, and each has length
                          O(N + M), hence the total Space Complexity would be O((N + M^)2)
                          And constructing for two string will have a cost of O((N + M)^2)
        :param string1, string2: the strings to be processed
        """
        self.root = Node(None)
        self.string1 = string1 + "$"
        self.max_lcs = ""
        # looping through the suffixes of string1, and adding them one by one to the tree
        for i in range(len(self.string1)):
            self.addSuffix(self.string1[i:], self.root)
        self.string2 = string2 + "#"
        # looping through the suffixes of string2, and adding them one by one to the tree
        for i in range(len(self.string2)):
            self.addSuffix(self.string2[i:], self.root)

    def addSuffix(self, suffix, root):
        """
        This function will be responsible to add the given suffix to the tree
        Approach:
        1) Check if there is a branch existed for the given suffix
        2) If not, insert it to the tree
        3) Else, check if the existed branch and the given suffix has any common prefixes
        4) If there is, creates 2 nodes which will be the children of this existed current branch node
            i) Node 1 (old node)
                - will be created using the current branch node with some modification
                - it will carry the current branch node's char[] and child[]
            ii) Node 2 (new node)
                - will be created using the given suffix
            iii) Current branch node
                - properties will be modified
        5) If the while loop did not run or the suffix is a prefix of the current branch node (vice versa), then a
        recursive function would be called to this same function with the next character on the given suffix and the
        current branch node

        Time Complexity: O(N + M), where N + M is the length of the suffix;
                         Worst Case: Either the while loop in line 362 will run N + M times or the while loop does not
                                     run at all but this function will perform a recursive calls N + M times
        Space Complexity: O((N + M)^2), where N + M is the length of the suffix;
        :param suffix: the given suffix
        :param root: the root node
        """
        # if the tree is empty we can just insert it to the tree
        if len(root.child) == 0:
            new_node = Node(suffix)
            root.child.append(new_node)
            root.char.append(suffix[0])
        else:
            # check if there is an existed branch for the given suffix
            exist = False
            i = -1
            while i < len(root.char) - 1 and exist is False:
                i += 1
                if suffix[0] == root.char[i]:
                    exist = True

            # if there isn't an existed branch for it, we can just insert it to the tree
            if exist is False:
                new_node = Node(suffix)
                root.child.append(new_node)
                root.char.append(suffix[0])
            else:
                j = 0
                match = True
                curr_node = root.child[i]

                if len(curr_node.label) < len(suffix):
                    min_length = len(curr_node.label)
                else:
                    min_length = len(suffix)

                # check is the existed branch and the given suffix has any common prefixes
                while j < min_length - 1 and match is True:
                    j += 1
                    # if there is, creates 2 nodes
                    if suffix[j] != curr_node.label[j]:
                        match = False
                        # creating the "old node"
                        old_node = Node(curr_node.label[j:])
                        old_node.child = curr_node.child
                        old_node.char = curr_node.char
                        # creating the "new node"
                        new_node = Node(suffix[j:])
                        # modifying the properties of current node
                        curr_node.label = suffix[:j]
                        curr_node.child = []
                        curr_node.char = []
                        curr_node.child.append(old_node)
                        curr_node.char.append(old_node.label[0])
                        curr_node.child.append(new_node)
                        curr_node.char.append(new_node.label[0])

                # if the while loop did not run or the suffix is a prefix of the current node (vice versa)
                if match is True:
                    self.addSuffix(suffix[j + 1:], curr_node)


def dfs(node, graph):
    """
    This function will traverse through every node in the tree suffix and find the longest common substring
    Approach:
    Following the Depth First Search algorithm, we will first traverse the deepest nodes of the suffix tree (i.e. the
    nodes that do not have any children), then we will traverse its sibling nodes, if any. Once we have finish
    traversing all its sibling nodes, then only we backtrack to its parent node. Following this pattern, we will
    eventually reach the root node (i.e. the node that does not have any parent node) and exit this function.
    While traversing all these nodes, we will also keep track of the number of occurrences the current node (the one we
    are currently traversing) occur in both strings. If the current node happens to appear in both strings, and it also
    happens to be the longest substring of all the ones that appear in both strings, then it will be the longest common
    substring that we are looking for

    Time Complexity: O(N + M), where N + M is the total length of the strings or the number of vertices in the graph
    Space Complexity: O(N + M), where N + M is the total length of the strings or the number of vertices in the graph
    :param node: the node we are currently traversing
    :param graph: the suffix tree
    """
    # if this is a lead node (Base Case)
    if len(node.child) == 0:
        # if the leaf node ends with "$"
        if node.label[len(node.label) - 1] == "$":
            node.delimiter[0] += 1
        # if the lead node ends with "#"
        elif node.label[len(node.label) - 1] == "#":
            node.delimiter[1] += 1
    # if this is an internal node
    else:
        node.curr_max_lcs = node.label
        longest_child = ""
        # looping through every child node
        for i in range(len(node.child)):
            curr_child_node = node.child[i]
            # recursive call to the child node (unit it reaches base case)
            dfs(curr_child_node, graph)
            # if this is not a root node
            if node.label is not None:
                # if the current child node is the longest child node
                if len(curr_child_node.curr_max_lcs) > len(longest_child):
                    # if the current child node exist in both strings as well
                    if curr_child_node.delimiter[0] > 0 and curr_child_node.delimiter[1] > 0:
                        longest_child = curr_child_node.curr_max_lcs
                        node.curr_max_lcs = node.label + longest_child

                # if the current child node ends with "$'
                if curr_child_node.label[len(curr_child_node.label) - 1] == "$":
                    node.delimiter[0] += 1
                # if the current child node ends with "#"
                elif curr_child_node.label[len(curr_child_node.label) - 1] == "#":
                    node.delimiter[1] += 1
                # if the current child node ends with a character, add both of its delimiter values to the current node
                else:
                    node.delimiter[0] += curr_child_node.delimiter[0]
                    node.delimiter[1] += curr_child_node.delimiter[1]

    # if the suffix appears in both string
    if node.delimiter[0] > 0 and node.delimiter[1] > 0:
        # check if current's node is longer
        if len(node.curr_max_lcs) > len(graph.max_lcs):
            graph.max_lcs = node.curr_max_lcs


def compare_subs(submission1, submission2):
    """
    N will be the length of string 1
    M will be the length of string 2
    Time Complexity for constructing the graph O((N + M)^2)
    Space Complexity for constructing the graph O((N + M)^2)
    Time Complexity for performing Depth-First Search: O(N + M)
    Space Complexity for performing Depth-First Search: O(N + M)
    Time Complexity for performing calculations: O(1)
    Space Complexity for performing calculations: O(1)
    :param submission1, submission2: the texts to be processed
    :return: the longest common substring, the similarity score for submission1 and the similarity score for submission2
    """
    # constructing the suffix tree
    G = SuffixTree(submission1, submission2)
    # traversing the suffix tree
    dfs(G.root, G)
    # finding the similarity score for both strings
    if len(submission1) > 0 and len(submission2) > 0:
        # finding the similarity score for the submission 1
        lcs_s1 = (len(G.max_lcs)/len(submission1)) * 100
        # if the fractional part is greater or equals to 0.5, round up; Otherwise, round down
        if (lcs_s1 - floor(lcs_s1)) >= 0.5:
            lcs_s1 = ceil(lcs_s1)
        else:
            lcs_s1 = floor(lcs_s1)

        # finding the similarity score for the submission 2
        lcs_s2 = (len(G.max_lcs) / len(submission2)) * 100
        # if the fractional part is greater or equals to 0.5, round up; Otherwise, round down
        if (lcs_s2 - floor(lcs_s2)) >= 0.5:
            lcs_s2 = ceil(lcs_s2)
        else:
            lcs_s2 = floor(lcs_s2)
    # if any of the submissions are empty, then the similarity score for both submissions would be 0
    else:
        lcs_s1 = 0
        lcs_s2 = 0
    return [G.max_lcs, lcs_s1, lcs_s2]
