import unittest
from assignment1 import analyze


class TestMethods(unittest.TestCase):
    # a roster of 2 characters
    roster = 2
    # results with 20 matches
    results = [
        ['AAB', 'AAB', 35], ['AAB', 'BBA', 49], ['BAB', 'BAB', 42],
        ['AAA', 'AAA', 38], ['BAB', 'BAB', 36], ['BAB', 'BAB', 36],
        ['ABA', 'BBA', 57], ['BBB', 'BBA', 32], ['BBA', 'BBB', 49],
        ['BBA', 'ABB', 55], ['AAB', 'AAA', 58], ['ABA', 'AAA', 46],
        ['ABA', 'ABB', 44], ['BBB', 'BAB', 32], ['AAA', 'AAB', 36],
        ['ABA', 'BBB', 48], ['BBB', 'ABA', 33], ['AAB', 'BBA', 30],
        ['ABB', 'BBB', 68], ['BAB', 'BBB', 52]
    ]

    def test_1(self):
        # looking for a score of 64
        score = 64

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]
        ]
        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_2(self):
        # looking for a score of 63
        score = 63

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'AAA', 64], ['ABB', 'ABB', 64]]
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_3(self):
        # looking for a score of 71
        score = 71

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            []
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_4(self):
        # looking for a score of 0
        score = 0

        result = [
            [['ABB', 'AAB', 70],
             ['ABB', 'BBB', 68],
             ['AAB', 'BBB', 67],
             ['AAB', 'AAB', 65],
             ['AAB', 'AAA', 64],
             ['ABB', 'ABB', 64],
             ['AAA', 'AAA', 62],
             ['AAB', 'AAA', 58],
             ['ABB', 'ABB', 58],
             ['AAB', 'ABB', 57]],
            [['AAB', 'ABB', 30]]
        ]

        self.assertEqual(analyze(self.results, self.roster, score), result)

    def test_5(self):
        results = [
            ['ABC', 'ADE', 30],
            ['AAC', 'ACE', 30],
            ['AAC', 'AAE', 30]
        ]

        result = [
            [['AAE', 'AAC', 70],
             ['ACE', 'AAC', 70],
             ['ADE', 'ABC', 70],
             ['AAC', 'AAE', 30],
             ['AAC', 'ACE', 30],
             ['ABC', 'ADE', 30]],
            [['AAE', 'AAC', 70], ['ACE', 'AAC', 70], ['ADE', 'ABC', 70]]
        ]

        self.assertEqual(analyze(results, 5, 40), result)

    def test_6(self):
        results = [
            ['AB', 'BB', 30],
            ['BA', 'AA', 30]
        ]

        result = [
            [['AA', 'AB', 70],
             ['BB', 'AB', 70],
             ['AB', 'AA', 30],
             ['AB', 'BB', 30]],
            [['AA', 'AB', 70], ['BB', 'AB', 70]]
        ]

        self.assertEqual(analyze(results, 2, 40), result)

    def test_7(self):
        results = [
            ['A', 'B', 30],
            ['C', 'A', 40]
        ]

        result = [
            [['B', 'A', 70],
             ['A', 'C', 60],
             ['C', 'A', 40],
             ['A', 'B', 30]],
            [['B', 'A', 70]]
        ]

        self.assertEqual(analyze(results, 3, 70), result)

    def test_8(self):
        results = [
            ['A', 'A', 30],
            ['A', 'A', 70],
            ['A', 'A', 40]
        ]

        result = [
            [['A', 'A', 70],
             ['A', 'A', 60],
             ['A', 'A', 40],
             ['A', 'A', 30]],
            [['A', 'A', 70]]
        ]

        self.assertEqual(analyze(results, 1, 70), result)

    def test_9(self):
        results = [
            ['A', 'B', 50],
        ]

        result = [
            [['A', 'B', 50],
             ['B', 'A', 50]],
            []
        ]

        self.assertEqual(analyze(results, 2, 70), result)

    def test_10(self):
        results = [
            ['A', 'A', 50],
        ]

        result = [
            [['A', 'A', 50]],
            [['A', 'A', 50]]
        ]

        self.assertEqual(analyze(results, 1, 50), result)

    def test_11(self):
        results = [
            ['A', 'B', 50],
        ]

        result = [
            [['A', 'B', 50],
             ['B', 'A', 50]],
            [['A', 'B', 50], ['B', 'A', 50]]
        ]

        self.assertEqual(analyze(results, 2, 50), result)

    def test_12(self):
        results = [
            ['A', 'B', 100],
        ]

        result = [
            [['A', 'B', 100],
             ['B', 'A', 0]],
            [['A', 'B', 100]]
        ]

        self.assertEqual(analyze(results, 2, 50), result)

    def test_13(self):
        results = [
            ['A', 'B', 100],
        ]

        result = [
            [['A', 'B', 100],
             ['B', 'A', 0]],
            [['B', 'A', 0]]
        ]

        self.assertEqual(analyze(results, 2, 0), result)

    def test_14(self):
        results = [
            ['A', 'A', 100],
        ]

        result = [
            [['A', 'A', 100],
             ['A', 'A', 0]],
            [['A', 'A', 0]]
        ]

        self.assertEqual(analyze(results, 1, 0), result)

    def test_15(self):
        results = [
            ['A', 'A', 100],
        ]

        result = [
            [['A', 'A', 100],
             ['A', 'A', 0]],
            [['A', 'A', 100]]
        ]

        self.assertEqual(analyze(results, 1, 1), result)

    def test_16(self):
        results = [
            ['AACDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35],
            ['ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35]
        ]

        result = [
            [['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'AACDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['AACDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35],
             ['ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 35]],
            [['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'AACDEFGHIJKLMNOPQRSTUVWXYZZ', 65],
             ['ABCDEFGHIJKLMNOPQRSTUVWXZZZ', 'ABCDEFGHIJKLMNOPQRSTUVWXYZZ', 65]]
        ]

        self.assertEqual(analyze(results, 26, 65), result)


if __name__ == '__main__':
    unittest.main()
