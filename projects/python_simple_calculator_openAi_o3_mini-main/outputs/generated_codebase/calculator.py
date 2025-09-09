import exception_handler


def validate_input(value):
    """Validate that the input can be converted to a float.

    Args:
        value (str): The input value from the GUI.

    Returns:
        float: The numeric value converted from the input.

    Raises:
        ValueError: If conversion fails with a formatted error message.
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(exception_handler.invalid_input_error())


def add(operand1, operand2):
    """Return the sum of two operands."""
    return operand1 + operand2


def subtract(operand1, operand2):
    """Return the difference between two operands."""
    return operand1 - operand2


def multiply(operand1, operand2):
    """Return the product of two operands."""
    return operand1 * operand2


def divide(operand1, operand2):
    """Return the quotient of two operands after checking for division by zero.

    Raises:
        ZeroDivisionError: If the second operand is zero, with a formatted error message.
    """
    if operand2 == 0:
        raise ZeroDivisionError(exception_handler.division_by_zero_error())
    return operand1 / operand2


def calculate(operation, op1_str, op2_str):
    """Handle input validation and perform the requested calculation.

    Args:
        operation (str): Operation to perform. Valid values: 'add', 'subtract', 'multiply', 'divide'.
        op1_str (str): The first operand as a string.
        op2_str (str): The second operand as a string.

    Returns:
        float: The result of the arithmetic operation.

    Raises:
        ValueError: For non-numeric inputs.
        ZeroDivisionError: For division by zero cases.
    """
    operand1 = validate_input(op1_str)
    operand2 = validate_input(op2_str)

    if operation == 'add':
        return add(operand1, operand2)
    elif operation == 'subtract':
        return subtract(operand1, operand2)
    elif operation == 'multiply':
        return multiply(operand1, operand2)
    elif operation == 'divide':
        return divide(operand1, operand2)
    else:
        raise ValueError('Unsupported operation.')
