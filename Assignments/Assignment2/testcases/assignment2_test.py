from msilib import sequence
import unittest
from assignment2 import optimalRoute


# Standard graph, nothing special
downhillScores = [(0, 1, 10), (0, 2, 50), (1, 2, 100),
                  (2, 3, 10), (2, 4, 5), (3, 4, -10),
                  (4, 5, 10), (5, 6, -5), (4, 7, 100), (7, 6, -100),
                  (6, 8, 50), (8, 9, -10), (6, 10, 10), (10, 9, 20)]
start_finish_inputs = [(0, 2), (2, 4), (4, 6), (6, 9)]  # nice
expected_outputs = [[0, 1, 2], [2, 4], [4, 5, 6], [6, 8, 9]]

# Small input
singleDownhill = [(0, 1, 1000)]  # single, just like irl

# Standard Graph, the sequel
downhillScoresTheSequel = [(1, 2, 9), (1, 13, 6), (1, 9, -9),
                           (2, 14, 4), (2, 12, -1), (2, 13, -6), (2, 10, 7),
                           (0, 13, -9), (0, 14, -1), (0, 10, 8), (0, 7, 1),
                           (4, 7, 3),
                           (5, 10, -9), (5, 7, 7), (5, 9, -10), (5, 6, 0),
                           (3, 9, -9), (3, 6, -3), (3, 11, 4), (3, 8, 2),
                           (10, 14, 1),
                           (7, 14, 5),
                           (9, 14, 9), (9, 11, -1),
                           (6, 15, 4),
                           (8, 15, -4),
                           (12, 14, 10),
                           (13, 14, 10),
                           (7, 11, -8),
                           (6, 11, 1)]
endpoints = [14, 11, 15]
startpoints = [0, 1, 2, 3, 5]
inputs_the_sequel = [(s, e) for s in startpoints for e in endpoints]
outputs_the_sequel = [[0, 10, 14], [0, 7, 11], None,
                      [1, 2, 12, 14], [1, 9, 11], None,
                      [2, 12, 14], None, None,
                      [3, 9, 14], [3, 11], [3, 6, 15],
                      [5, 7, 14], [5, 6, 11], [5, 6, 15]]

# Standard Graph, The Trilogy
downhillScoresTheTrilogy = [(0, 1, 10), (1, 2, 50), (1, 3, 50), (1, 4, 50)]
inputs_the_trilogy = [(0, 2), (0, 3), (0, 4)]
outputs_the_trilogy = [[0, 1, 2], [0, 1, 3], [0, 1, 4]]

# Sneaky Graph
scores = [(1, 2, 200), (1, 0, 10), (3, 1, 5), (2, 0, 50), (3, 0, 25)]
sneaky_inputs = [(3, 0)]
sneaky_output = [[3, 1, 2, 0]]

# Simple triangle graph
tri_scores = [(0, 1, 10), (0, 2, 10), (1, 2, 5)]
tri_input = (0, 2)
tri_output = [0, 1, 2]


class TestOptimalRoute(unittest.TestCase):
    def base_tester(self, lst, s, e, o):
        self.assertEqual(optimalRoute(lst, s, e), o)

    def test_optimalRoute(self):
        for (start, end), output in zip(start_finish_inputs, expected_outputs):
            self.base_tester(downhillScores, start, end, output)

    def test_the_sequel(self):
        for (start, end), output in zip(inputs_the_sequel, outputs_the_sequel):
            self.base_tester(downhillScoresTheSequel, start, end, output)

    def test_the_trilogy(self):
        for (start, end), output in zip(inputs_the_trilogy, outputs_the_trilogy):
            self.base_tester(downhillScoresTheTrilogy, start, end, output)

    def test_sneaky(self):
        for (start, end), output in zip(sneaky_inputs, sneaky_output):
            self.base_tester(scores, start, end, output)

    def test_triangle(self):
        start, end = tri_input
        self.base_tester(tri_scores, start, end, tri_output)

    def test_oneDownhill(self):
        self.base_tester(singleDownhill, 0, 1, [0, 1])

    def test_oneDownhill_but_flip(self):
        self.base_tester(singleDownhill, 1, 0, None)

    def test_do_not_move(self):
        for i in range(5):
            self.base_tester([(0, 1, 6), (1, 2, 9), (2, 3, 4),
                             (3, 4, 2), (4, 5, 0)], i, i, [i])

    def test_shortcut(self):
        for i in range(50):
            self.base_tester([(u, u + 1, 1) for u in range(i + 1)] +
                             [(0, i + 1, i + 2)], 0, i + 1, [0, i + 1])

    # Just for fun
    def test_binary_fib_hill(self):
        self.base_tester(bin_fib_score, 0, 21, [0, 2, 6, 14, 18, 20, 21])

    def test_alt_bin_fib_hill(self):
        self.base_tester(alt_bin_fib_score, 0, 21, [0, 1, 3, 7, 15, 19, 21])

    def test_neg_bin_fib(self):
        self.base_tester(neg_bin_fib_score, 0, 21, [0, 1, 3, 7, 15, 19, 21])


class FibBoi:
    """ Infinite sequence of fibonacci sequence """

    def __init__(self, val=1, prev=0):
        self.val = val
        self.prev = prev

    def next(self):
        """ To go to the next value """
        self.val, self.prev = self.val + self.prev, self.val


# Binary Tree with root 0, scores = fibonacci values
bin_fib_score = []
fib_seq = FibBoi()
root = 0
for _ in range(7):
    u = root
    score1 = (u, 2*u + 1, fib_seq.val)
    fib_seq.next()
    score2 = (u, 2*u + 2, fib_seq.val)
    fib_seq.next()

    root += 1
    bin_fib_score.append(score1)
    bin_fib_score.append(score2)

for _ in range(7):
    u1 = root
    u2 = u1 + 1
    v = int((45 + u1 + u2) / 4)

    score1 = (u1, v, fib_seq.val)
    fib_seq.next()
    score2 = (u2, v, fib_seq.val)
    fib_seq.next()

    root += 2
    bin_fib_score.append(score1)
    bin_fib_score.append(score2)

alt_bin_fib_score = [(u, v, -w) if i % 2 else (u, v, w)
                     for i, (u, v, w) in enumerate(bin_fib_score)]
neg_bin_fib_score = [(u, v, -w) for u, v, w in bin_fib_score]

if __name__ == '__main__':
    unittest.main()
