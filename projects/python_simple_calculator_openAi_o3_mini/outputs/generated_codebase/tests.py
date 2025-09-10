import unittest
from calculator import add, subtract, multiply, divide, validate_input, calculate
import exception_handler


class TestCalculatorOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)

    def test_multiply(self):
        self.assertEqual(multiply(4, 3), 12)
        self.assertEqual(multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        with self.assertRaises(ZeroDivisionError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), exception_handler.division_by_zero_error())

    def test_validate_input_success(self):
        self.assertEqual(validate_input('3.14'), 3.14)
        self.assertEqual(validate_input('10'), 10.0)

    def test_validate_input_failure(self):
        with self.assertRaises(ValueError) as context:
            validate_input('abc')
        self.assertEqual(str(context.exception), exception_handler.invalid_input_error())

    def test_calculate_add(self):
        result = calculate('add', '2', '3')
        self.assertEqual(result, 5)

    def test_calculate_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate('divide', '10', '0')

    def test_calculate_invalid_operation(self):
        with self.assertRaises(ValueError):
            calculate('mod', '10', '3')


if __name__ == '__main__':
    unittest.main()