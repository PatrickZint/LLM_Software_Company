import unittest
import tkinter as tk
from gui import SimpleCalculatorApp


class TestCalculatorGUI(unittest.TestCase):
    def setUp(self):
        # Create a hidden Tk root for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent the GUI from popping up
        self.app = SimpleCalculatorApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def set_entries(self, val1, val2):
        self.app.entry1.delete(0, tk.END)
        self.app.entry1.insert(0, val1)
        self.app.entry2.delete(0, tk.END)
        self.app.entry2.insert(0, val2)

    def get_result_text(self):
        return self.app.result_label.cget("text")

    def test_addition(self):
        self.set_entries("2", "3")
        self.app.perform_operation("add")
        self.assertEqual(self.get_result_text(), "Result: 5.0")

    def test_subtraction(self):
        self.set_entries("10", "4")
        self.app.perform_operation("subtract")
        self.assertEqual(self.get_result_text(), "Result: 6.0")

    def test_multiplication(self):
        self.set_entries("3", "7")
        self.app.perform_operation("multiply")
        self.assertEqual(self.get_result_text(), "Result: 21.0")

    def test_division(self):
        self.set_entries("8", "2")
        self.app.perform_operation("divide")
        self.assertEqual(self.get_result_text(), "Result: 4.0")

    def test_division_by_zero(self):
        self.set_entries("5", "0")
        self.app.perform_operation("divide")
        self.assertIn("Error: Cannot divide by zero", self.get_result_text())

    def test_invalid_input(self):
        self.set_entries("abc", "5")
        self.app.perform_operation("add")
        self.assertIn("Error: Both inputs must be valid numbers.", self.get_result_text())

    def test_clear_fields(self):
        self.set_entries("9", "9")
        self.app.result_label.config(text="Result: 18.0")
        self.app.clear_fields()
        self.assertEqual(self.app.entry1.get(), "")
        self.assertEqual(self.app.entry2.get(), "")
        self.assertEqual(self.get_result_text(), "")


if __name__ == "__main__":
    unittest.main()