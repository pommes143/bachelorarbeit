import unittest
from example_solution import what_are_you

class TestWhatAreYouFunction(unittest.TestCase):
    def test_string(self):
        self.assertEqual(what_are_you("hello"), "<class 'str'>")
        self.assertEqual(what_are_you(""), "<class 'str'>")

    def test_integer(self):
        self.assertEqual(what_are_you(42), "<class 'int'>")
        self.assertEqual(what_are_you(-1), "<class 'int'>")
        self.assertEqual(what_are_you(0), "<class 'int'>")

    def test_float(self):
        self.assertEqual(what_are_you(3.14), "<class 'float'>")
        self.assertEqual(what_are_you(1.23), "<class 'float'>")
        self.assertEqual(what_are_you(-2.34), "<class 'float'>")

    def test_boolean(self):
        self.assertEqual(what_are_you(True), "<class 'bool'>")
        self.assertEqual(what_are_you(False), "<class 'bool'>")

    def test_none(self):
        self.assertEqual(what_are_you(None), "NoneType")

    def test_collections(self):
        self.assertEqual(what_are_you([]), "<class 'list'>")
        self.assertEqual(what_are_you([1, 2, 3]), "<class 'list'>")
        self.assertEqual(what_are_you(()), "<class 'tuple'>")
        self.assertEqual(what_are_you((1, 2, 3)), "<class 'tuple'>")
        self.assertEqual(what_are_you({}), "<class 'dict'>")
        self.assertEqual(what_are_you({"a": 1, "b": 2}), "<class 'dict'>")

    def test_set(self):
        self.assertEqual(what_are_you(set()), "<class 'set'>")
        self.assertEqual(what_are_you({1, 2, 3}), "<class 'set'>")

if __name__ == "__main__":
    unittest.main()
if __name__ == '__main__': #pragma: no cover
        unittest.main()