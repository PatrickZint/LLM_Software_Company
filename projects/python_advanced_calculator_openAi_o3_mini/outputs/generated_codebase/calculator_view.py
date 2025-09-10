import tkinter as tk
from tkinter import messagebox

class CalculatorGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Advanced Calculator")
        
        # Create the display entry
        self.display = tk.Entry(self.root, font=("Arial", 20), borderwidth=2, relief="ridge")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")
        
        self.build_buttons()
        self.bind_keys()

    def build_buttons(self):
        # Define buttons as tuples of (label, row, column)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('(', 4, 2), (')', 4, 3),
            ('C', 5, 0), ('⌫', 5, 1), ('=', 5, 2), ('+', 5, 3),
            ('sqrt', 6, 0), ('log', 6, 1), ('sin', 6, 2), ('cos', 6, 3),
            ('tan', 7, 0), ('exp', 7, 1), ('log10', 7, 2), ('^', 7, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self.root, text=text, font=("Arial", 16), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Ensure that each button expands properly
            self.root.grid_rowconfigure(row, weight=1)
            self.root.grid_columnconfigure(col, weight=1)

    def bind_keys(self):
        # Bind Enter to evaluate the expression
        self.root.bind("<Return>", lambda event: self.on_button_click('='))
        # Bind Backspace for delete
        self.root.bind("<BackSpace>", lambda event: self.on_button_click('⌫'))
        # Bind numeric and operator keys
        for char in "0123456789.+-*/()":
            self.root.bind(char, lambda event, c=char: self.on_button_click(c))

    def on_button_click(self, char):
        if char == 'C':
            self.clear_display()
        elif char == '⌫':
            current_text = self.display.get()
            # Delete last character
            self.display.delete(0, tk.END)
            self.display.insert(0, current_text[:-1])
        elif char == '=':
            expr = self.display.get()
            self.controller.process_expression(expr)
        elif char == '^':
            # Convert caret to exponentiation operator
            self.display.insert(tk.END, '**')
        else:
            # Append the pressed button's label to the display
            self.display.insert(tk.END, char)

    def update_display(self, text):
        self.clear_display()
        self.display.insert(0, text)

    def clear_display(self):
        self.display.delete(0, tk.END)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def start(self):
        self.root.mainloop()
