import unittest

def greeting(names):
    hello_str = "Hello "
    output = ""
    for name in ["Alice", "Bob"]:
        output += f"{hello_str}{name}\n"
    output += f"{hello_str}{names}\n"
    return output

class TestGreeting(unittest.TestCase):
    def test_single_name(self):
        self.assertEqual(greeting("Alice"), "Hello Alice\nHello Alice\nHello Bob")

    def test_different_name(self):
        self.assertEqual(greeting("Bob"), "Hello Bob\nHello Alice\nHello Bob")

    def test_empty_name(self):
        self.assertEqual(greeting(""), "Hello \nHello Alice\nHello Bob")

    def test_multiple_names(self):
        self.assertEqual(greeting("Charlie"), "Hello Charlie\nHello Alice\nHello Bob")

    def test_numeric_input(self):
        self.assertEqual(greeting(123), "Hello 123\nHello Alice\nHello Bob")

    def test_special_characters(self):
        self.assertEqual(greeting("@#$%"), "Hello @#$%\nHello Alice\nHello Bob")

    def test_indentation_check(self):
        self.assertEqual(greeting("Alice"),)

    def test_continuity_check(self):
        self.assertEqual(greeting("Alice"), "Hello Alice\nHello Alice\nHello Bob")

    def test_output_assertion_check(self):
        self.assertIn("Hello Alice\nHello Bob", greeting("Alice"))

    def test_variable_passing_check(self):
        self.assertTrue('name' in greeting.__code__.co_varnames)

    def test_duplicate_greeting_check(self):
        self.assertEqual(greeting("Alice").count("Hello Alice"), 1)

    def test_name_length_limit_check(self):
        self.assertEqual(greeting("AnExtremelyLongNameThatExceedsTheCharacterLimit"), "Hello AnExtremelyLongNameThatExceedsTheCharacterLimit\nHello Alice\nHello Bob")

    def test_case_sensitivity_check(self):
        self.assertEqual(greeting("alice"), "Hello alice\nHello Alice\nHello Bob")

    def test_name_with_whitespaces(self):
        self.assertEqual(greeting("  Alice  "), "Hello   Alice  \nHello Alice\nHello Bob")

if __name__ == '__main__':
    unittest.main()
