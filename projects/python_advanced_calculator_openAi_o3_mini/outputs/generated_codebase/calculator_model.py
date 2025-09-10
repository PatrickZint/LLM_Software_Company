import ast
import operator
import math

class CalculatorEngine:
    def __init__(self):
        # Allowed functions available for the calculation
        self.allowed_funcs = {
            'sqrt': math.sqrt,
            'log': math.log,        # natural logarithm
            'log10': math.log10,    
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp
        }

    def evaluate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string safely using AST parsing.
        Supports basic arithmetic and a limited set of mathematical functions.

        :param expression: the mathematical expression in string format
        :return: evaluated result as float
        :raises: ValueError if the expression is malformed or contains errors
        """
        try:
            # Replace '^' with '**' for exponentiation if user enters caret
            expression = expression.replace('^', '**')
            # Parse the expression into an AST
            node = ast.parse(expression, mode='eval')
            return self._evaluate_ast(node.body)
        except Exception as e:
            raise ValueError(f"Error evaluating expression: {e}")

    def _evaluate_ast(self, node):
        if isinstance(node, ast.BinOp):
            left = self._evaluate_ast(node.left)
            right = self._evaluate_ast(node.right)
            return self._apply_operator(node.op, left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._evaluate_ast(node.operand)
            return self._apply_unary_operator(node.op, operand)
        elif isinstance(node, ast.Num):  # For Python < 3.8
            return node.n
        elif isinstance(node, ast.Constant):  # For Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Only int and float constants are allowed")
        elif isinstance(node, ast.Call):
            # Ensure that only allowed functions are called
            if isinstance(node.func, ast.Name) and node.func.id in self.allowed_funcs:
                args = [self._evaluate_ast(arg) for arg in node.args]
                return self.allowed_funcs[node.func.id](*args)
            else:
                raise ValueError(f"Function '{getattr(node.func, 'id', 'unknown')}' is not allowed")
        elif isinstance(node, ast.Expression):
            return self._evaluate_ast(node.body)
        else:
            raise ValueError("Unsupported expression")

    def _apply_operator(self, op, left, right):
        if isinstance(op, ast.Add):
            return operator.add(left, right)
        elif isinstance(op, ast.Sub):
            return operator.sub(left, right)
        elif isinstance(op, ast.Mult):
            return operator.mul(left, right)
        elif isinstance(op, ast.Div):
            if right == 0:
                raise ValueError("Division by zero")
            return operator.truediv(left, right)
        elif isinstance(op, ast.Pow):
            return operator.pow(left, right)
        else:
            raise ValueError("Unsupported operator")

    def _apply_unary_operator(self, op, operand):
        if isinstance(op, ast.UAdd):
            return +operand
        elif isinstance(op, ast.USub):
            return -operand
        else:
            raise ValueError("Unsupported unary operator")
