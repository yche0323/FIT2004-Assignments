from math import floor, ceil


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
                         Worst Case: Either the while loop in line 96 will run N + M times or the while loop does not
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

    Time Complexity: O(N + M), where N + M is the total length of the two strings or the number of vertices in the graph
    Space Complexity: O(N + M), where N + M is the total length of the two strings or the number of vertices in the graph
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
