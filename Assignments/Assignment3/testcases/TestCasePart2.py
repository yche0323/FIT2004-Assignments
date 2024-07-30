import unittest
from Task2 import compare_subs


class TestMethods(unittest.TestCase):

    def test_1(self):
        # Example 1
        submission1 = "the quick brown fox jumped over the lazy dog"
        submission2 = "my lazy dog has eaten my homework"
        self.assertEqual(compare_subs(submission1, submission2), [" lazy dog", 20, 27])

    def test_2(self):
        # Example 1
        submission1 = "radix sort and counting sort are both non comparison sorting algorithms"
        submission2 = "counting sort and radix sort are both non comparison sorting algorithms"
        self.assertEqual(compare_subs(submission1, submission2), [" sort are both non comparison sorting algorithms", 68, 68])

    def test_3(self):
        # Example 1
        submission1 = "safsa fs afs afs afs afsafsafiosafbanana asfophsafopsafopsafopsafpa"
        submission2 = "safsifaha asdoisaosans banana iosfqwpfwqpoanvsavm"
        self.assertEqual(compare_subs(submission1, submission2), ["banana ", 10, 14])

    def test_4(self):
        # Example 1
        submission1 = "banana"
        submission2 = "banana"
        self.assertEqual(compare_subs(submission1, submission2), ["banana", 100, 100])

    def test_5(self):
        # Example 1
        submission1 = "abcde"
        submission2 = "fghij"
        self.assertEqual(compare_subs(submission1, submission2), ["", 0, 0])

    def test_6(self):
        # Example 1
        submission1 = "abcdefghijklmnopqrstuvwxyzb"
        submission2 = "abcdefghijklmnopqrstuvwxyza"
        self.assertEqual(compare_subs(submission1, submission2), ["abcdefghijklmnopqrstuvwxyz", 96, 96])

    def test_7(self):
        # Example 1
        submission1 = "abcdefghijklmnopqrstuvwxyzb" * 200
        submission2 = "abcdefghijklmnopqrstuvwxyza" * 200
        self.assertEqual(compare_subs(submission1, submission2), ["abcdefghijklmnopqrstuvwxyz", 0, 0])

    """
    Not sure about this test case
    def test_8(self): 
        # Example 1
        submission1 = ""
        submission2 = ""
        self.assertEqual(compare_subs(submission1, submission2), ["", 100, 100])
    """


if __name__ == '__main__':
    unittest.main()
