import unittest
from example_solution import name_check

class TestNameCheck(unittest.TestCase):

    def test_name_check_x_present(self):
        result = name_check("Robert")
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], ('o', 'b', 'e', 'r', 't'))

    def test_name_check_x_not_present_uppercaseX(self):
        result = name_check("Xena")
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], ('e', 'n', 'a'))

    def test_name_check_x_not_present_mixedCase(self):
        result = name_check("Alex")
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], ('l', 'e', 'x'))

    def test_name_check_x_present_multipleX(self):
        result = name_check("Maxim")
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], ('a', 'x', 'i', 'm'))

if __name__ == '__main__': # pragma: no cover
    unittest.main()
