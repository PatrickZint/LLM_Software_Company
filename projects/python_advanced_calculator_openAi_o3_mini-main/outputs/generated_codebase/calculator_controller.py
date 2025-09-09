import logging
from calculator_model import CalculatorEngine
from calculator_view import CalculatorGUI

class CalculatorController:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        self.engine = CalculatorEngine()
        self.view = CalculatorGUI(self)

    def process_expression(self, expression: str):
        try:
            # Process the expression using the CalculatorEngine
            result = self.engine.evaluate(expression)
            self.view.update_display(str(result))
        except Exception as e:
            self.logger.error(f"Error processing expression '{expression}': {e}")
            self.view.show_error(str(e))
