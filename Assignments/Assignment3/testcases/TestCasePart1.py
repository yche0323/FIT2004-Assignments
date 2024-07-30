import math
import unittest
from assignment3 import allocate


def verify_solution(availability, solution):
    n = len(solution[0])
    takeout_count = 0
    people_counts = [0, 0, 0, 0, 0]

    for i in range(len(solution[0])):
        breakfast = solution[0][i]
        if breakfast == 5:
            takeout_count += 1
        else:
            if availability[i][breakfast] != 1 and availability[i][breakfast] != 3:
                print("\nCannot allocate breakfast to person " + str(breakfast) + "on day " + str(i))
                return False
            people_counts[breakfast] += 1

    for i in range(len(solution[1])):
        dinner = solution[1][i]
        if dinner == 5:
            takeout_count += 1
        else:
            if availability[i][dinner] != 2 and availability[i][dinner] != 3:
                print("\nCannot allocate dinner to person " + str(dinner) + "on day " + str(i))
                return False
            elif availability[i][dinner] == 3 and solution[0][i] == dinner:
                print("\nDinner and Breakfast cannot both be allocated to person " + str(dinner) + " on day " + str(i))
                return False
            people_counts[dinner] += 1

    if takeout_count > math.floor(0.1*n):
        print("\nDoes not satisfy takeout requirements")
        return False

    for person in people_counts:
        if person < math.floor(0.36*n) or person > math.ceil(0.44*n):
            print("\nDoes not satisfy upper and lower requirements for allocations")
            return False

    return True


class TestMethods(unittest.TestCase):

    def test_1(self):
        # Example
        availability = [[2, 0, 2, 1, 2], [3, 3, 1, 0, 0],
                        [0, 1, 0, 3, 0], [0, 0, 2, 0, 3],
                        [1, 0, 0, 2, 1], [0, 0, 3, 0, 2],
                        [0, 2, 0, 1, 0], [1, 3, 3, 2, 0],
                        [0, 0, 1, 2, 1], [2, 0, 0, 3, 0]]
        self.assertTrue(verify_solution(availability, allocate(availability)))

    def test_2(self):
        # Example
        availability = [[0, 0, 0, 0, 0], [3, 3, 1, 0, 0],
                        [0, 1, 0, 3, 0], [0, 0, 2, 0, 3],
                        [1, 0, 0, 2, 1], [0, 0, 3, 0, 2],
                        [0, 2, 0, 1, 0], [1, 3, 3, 2, 0],
                        [0, 0, 1, 2, 1], [2, 0, 0, 3, 0]]
        self.assertIsNone(allocate(availability))

    def test_3(self):
        # Example
        availability = [[3, 3, 3, 3, 3], [3, 3, 3, 3, 3],
                        [3, 3, 3, 3, 3], [3, 3, 3, 3, 3],
                        [3, 3, 3, 3, 3], [3, 3, 3, 3, 3],
                        [3, 3, 3, 3, 3], [3, 3, 3, 3, 3],
                        [3, 3, 3, 3, 3], [3, 3, 3, 3, 3]]
        self.assertTrue(verify_solution(availability, allocate(availability)))

    def test_4(self):
        # Example
        availability = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.assertIsNone(allocate(availability))


if __name__ == '__main__':
    unittest.main()