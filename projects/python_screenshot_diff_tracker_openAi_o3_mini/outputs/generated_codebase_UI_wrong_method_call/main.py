import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

from config import load_config
from image_comparator import ImageComparator
from database_manager import DatabaseManager


class ImageDiffApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load configuration
        try:
            self.config_data = load_config()
        except Exception as e:
            messagebox.showerror("Configuration Error", str(e))
            self.destroy()
            return

        self.title("Image Diff Comparator")
        self.geometry("800x600")

        # Initialize variables
        self.image1_path = None
        self.image2_path = None
        self.diff_image = None
        self.diff_photo = None
        self.db_manager = DatabaseManager(self.config_data.get('database', 'comparisons.db'))

        # Setup UI
        self.create_widgets()

    def create_widgets(self):
        # Frame for file selection
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=10, padx=10, fill='x')

        btn1 = ttk.Button(file_frame, text="Select Image 1", command=self.select_image1)
        btn1.grid(row=0, column=0, padx=5, pady=5)

        btn2 = ttk.Button(file_frame, text="Select Image 2", command=self.select_image2)
        btn2.grid(row=0, column=1, padx=5, pady=5)

        # Button to choose output directory
        btn_output = ttk.Button(file_frame, text="Select Output Directory", command=self.select_output_directory)
        btn_output.grid(row=0, column=2, padx=5, pady=5)

        # Label to show chosen directory
        self.output_dir = self.config_data.get('output_directory', os.getcwd())
        self.output_label = ttk.Label(file_frame, text=f"Output: {self.output_dir}")
        self.output_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Compare Button
        compare_btn = ttk.Button(self, text="Compare Images", command=self.compare_images)
        compare_btn.pack(pady=10)

        # Canvas to display diff image
        self.canvas = tk.Canvas(self, bg='gray', width=600, height=400)
        self.canvas.pack(pady=10)

    def select_image1(self):
        file_path = filedialog.askopenfilename(title="Select First Image",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image1_path = file_path
            messagebox.showinfo("Image Selected", f"Image 1 selected:\n{file_path}")

    def select_image2(self):
        file_path = filedialog.askopenfilename(title="Select Second Image",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image2_path = file_path
            messagebox.showinfo("Image Selected", f"Image 2 selected:\n{file_path}")

    def select_output_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"Output: {self.output_dir}")

    def compare_images(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showerror("Missing Images", "Please select both images before comparing.")
            return

        tolerance = self.config_data.get('tolerance', 10)
        highlight_color = tuple(self.config_data.get('highlight_color', [0, 0, 255]))
        resize_strategy = self.config_data.get('resize_strategy', 'error')

        try:
            diff_img, diff_score = ImageComparator.compare_images(
                self.image1_path,
                self.image2_path,
                tolerance=tolerance,
                highlight_color=highlight_color,
                resize_strategy=resize_strategy
            )
        except Exception as e:
            messagebox.showerror("Comparison Error", str(e))
            return

        # Save diff image to output directory with a descriptive name
        diff_filename = os.path.join(self.output_dir, f"diff_{os.path.basename(self.image1_path)}_{os.path.basename(self.image2_path)}")
        cv2.imwrite(diff_filename, diff_img)

        # Log comparison info in the database
        try:
            # Get image dimensions
            img1 = ImageComparator.load_image(self.image1_path)
            img2 = ImageComparator.load_image(self.image2_path)
            dims1 = img1.shape[:2]
            dims2 = img2.shape[:2]
            self.db_manager.log_comparison(self.image1_path, self.image2_path, dims1, dims2, tolerance, diff_score)
        except Exception as e:
            messagebox.showwarning("Database Warning", f"Comparison saved to file but failed to log in database: {e}")

        # Display diff image on canvas
        self.show_diff_image(diff_img)
        messagebox.showinfo("Comparison Complete", f"Diff image saved to: {diff_filename}\nDifference Score: {diff_score}")

    def show_diff_image(self, cv_img):
        # Convert from OpenCV BGR to PIL Image
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(cv_img)

        # Resize image to fit canvas if necessary
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        pil_img.thumbnail((canvas_width, canvas_height), Image.ANTIALIAS)

        self.diff_photo = ImageTk.PhotoImage(pil_img)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.diff_photo, anchor=tk.CENTER)

    def on_closing(self):
        self.db_manager.close()
        self.destroy()


if __name__ == '__main__':
    app = ImageDiffApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
