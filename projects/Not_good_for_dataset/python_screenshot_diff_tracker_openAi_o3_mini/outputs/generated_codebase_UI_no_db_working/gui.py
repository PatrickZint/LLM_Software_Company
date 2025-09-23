import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import image_comparator
import config


class ImageDiffGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image Diff Tool')
        self.geometry('1000x600')

        # Instance variables for image paths and images
        self.image1_path = None
        self.image2_path = None
        self.diff_image = None
        self.tk_diff_image = None  # Tkinter compatible image for display

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, pady=10)

        btn_load1 = tk.Button(button_frame, text='Load Image 1', command=self.load_image1)
        btn_load1.pack(side=tk.LEFT, padx=5)

        btn_load2 = tk.Button(button_frame, text='Load Image 2', command=self.load_image2)
        btn_load2.pack(side=tk.LEFT, padx=5)

        btn_compare = tk.Button(button_frame, text='Compare Images', command=self.compare_images)
        btn_compare.pack(side=tk.LEFT, padx=5)

        btn_export = tk.Button(button_frame, text='Export Diff Image', command=self.export_diff)
        btn_export.pack(side=tk.LEFT, padx=5)

        # Canvas to display images
        self.image_canvas = tk.Canvas(self, bg='gray', width=800, height=500)
        self.image_canvas.pack(pady=10)

        # Label for status and messages
        self.status_label = tk.Label(self, text='Please load two images to compare.', fg='blue')
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def load_image1(self):
        path = filedialog.askopenfilename(initialdir=config.DEFAULT_INPUT_DIR,
                                          title='Select First Image',
                                          filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if path:
            self.image1_path = path
            self.status_label['text'] = f'Loaded Image 1: {path}'

    def load_image2(self):
        path = filedialog.askopenfilename(initialdir=config.DEFAULT_INPUT_DIR,
                                          title='Select Second Image',
                                          filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if path:
            self.image2_path = path
            self.status_label['text'] = f'Loaded Image 2: {path}'

    def compare_images(self):
        if not self.image1_path or not self.image2_path:
            messagebox.showerror('Error', 'Please load both images before comparing.')
            return
        try:
            self.diff_image = image_comparator.compare_images(self.image1_path, self.image2_path)
            # Resize the image for display in canvas if needed
            disp_image = self.diff_image.copy()
            disp_image.thumbnail((800, 500))
            self.tk_diff_image = ImageTk.PhotoImage(disp_image)
            self.image_canvas.delete('all')
            self.image_canvas.create_image(400, 250, image=self.tk_diff_image)
            self.status_label['text'] = 'Comparison complete. Differences highlighted.'
        except Exception as e:
            messagebox.showerror('Error', f'Error during comparison: {e}')
            self.status_label['text'] = 'Comparison failed.'

    def export_diff(self):
        if self.diff_image is None:
            messagebox.showerror('Error', 'No diff image to export. Please perform a comparison first.')
            return
        directory = filedialog.askdirectory(initialdir=config.DEFAULT_OUTPUT_DIR, title='Select Output Directory')
        if directory:
            save_path = os.path.join(directory, 'diff_image.png')
            try:
                self.diff_image.save(save_path)
                messagebox.showinfo('Success', f'Diff image saved to {save_path}')
                self.status_label['text'] = f'Diff image exported to {save_path}'
            except Exception as e:
                messagebox.showerror('Error', f'Error saving diff image: {e}')
                self.status_label['text'] = 'Export failed.'


if __name__ == '__main__':
    app = ImageDiffGUI()
    app.mainloop()
