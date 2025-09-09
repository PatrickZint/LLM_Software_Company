import tkinter as tk
from tkinter import ttk
import calculator


class SimpleCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Simple Calculator')

        # Create and position input fields
        ttk.Label(root, text='Operand 1:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry1 = ttk.Entry(root, width=15)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text='Operand 2:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry2 = ttk.Entry(root, width=15)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)

        # Create Operation Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_add = ttk.Button(btn_frame, text='Add', command=lambda: self.perform_operation('add'))
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_subtract = ttk.Button(btn_frame, text='Subtract', command=lambda: self.perform_operation('subtract'))
        self.btn_subtract.grid(row=0, column=1, padx=5)

        self.btn_multiply = ttk.Button(btn_frame, text='Multiply', command=lambda: self.perform_operation('multiply'))
        self.btn_multiply.grid(row=0, column=2, padx=5)

        self.btn_divide = ttk.Button(btn_frame, text='Divide', command=lambda: self.perform_operation('divide'))
        self.btn_divide.grid(row=0, column=3, padx=5)

        self.btn_clear = ttk.Button(btn_frame, text='Clear', command=self.clear_fields)
        self.btn_clear.grid(row=0, column=4, padx=5)

        # Output label for displaying results or error messages
        self.result_label = ttk.Label(root, text='', font=('Arial', 12))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def perform_operation(self, operation):
        """Retrieve inputs, invoke the calculation, and update the display area with the result or error message."""
        op1 = self.entry1.get()
        op2 = self.entry2.get()

        try:
            result = calculator.calculate(operation, op1, op2)
            self.result_label.config(text=f'Result: {result}', foreground='black')
        except (ValueError, ZeroDivisionError) as e:
            self.result_label.config(text=str(e), foreground='red')

    def clear_fields(self):
        """Clear the input fields and the result label."""
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.result_label.config(text='')


def main():
    root = tk.Tk()
    app = SimpleCalculatorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
