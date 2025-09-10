import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

import config
import database
import report


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Organizer')
        self.config = config.get_config()
        
        self.create_widgets()
        self.refresh_logs()

    def create_widgets(self):
        # Directory selection frame
        dir_frame = ttk.LabelFrame(self.root, text='Monitored Directories')
        dir_frame.pack(fill='x', padx=10, pady=5)

        self.dir_listbox = tk.Listbox(dir_frame, height=5)
        self.dir_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = tk.Frame(dir_frame)
        btn_frame.pack(side='right', padx=5)
        add_btn = ttk.Button(btn_frame, text='Add', command=self.add_directory)
        add_btn.pack(fill='x', pady=2)
        remove_btn = ttk.Button(btn_frame, text='Remove', command=self.remove_directory)
        remove_btn.pack(fill='x', pady=2)

        # Logs frame
        logs_frame = ttk.LabelFrame(self.root, text='Operation Logs')
        logs_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.logs_text = tk.Text(logs_frame, wrap='none', height=15)
        self.logs_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Buttons for refresh logs and export CSV
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=10, pady=5)
        refresh_btn = ttk.Button(bottom_frame, text='Refresh Logs', command=self.refresh_logs)
        refresh_btn.pack(side='left')
        export_btn = ttk.Button(bottom_frame, text='Export CSV Report', command=self.export_csv)
        export_btn.pack(side='left', padx=10)
        
        # Load directories from config
        self.load_directories()

    def add_directory(self):
        directory = filedialog.askdirectory()
        if directory and directory not in self.config['monitored_directories']:
            self.config['monitored_directories'].append(directory)
            config.save_config(self.config)
            self.dir_listbox.insert(tk.END, directory)
        elif directory in self.config['monitored_directories']:
            messagebox.showinfo('Info', 'Directory already added.')

    def remove_directory(self):
        selection = self.dir_listbox.curselection()
        if selection:
            index = selection[0]
            directory = self.dir_listbox.get(index)
            self.config['monitored_directories'].remove(directory)
            config.save_config(self.config)
            self.dir_listbox.delete(index)
        else:
            messagebox.showwarning('Warning', 'No directory selected.')

    def load_directories(self):
        self.dir_listbox.delete(0, tk.END)
        for d in self.config.get('monitored_directories', []):
            self.dir_listbox.insert(tk.END, d)

    def refresh_logs(self):
        # Fetch logs from the database and display
        logs = database.get_all_logs()
        self.logs_text.delete('1.0', tk.END)
        for log in logs:
            # log is a tuple: (timestamp, src, dest, rule)
            self.logs_text.insert(tk.END, f"{log[0]} | From: {log[1]} | To: {log[2]} | Rule: {log[3]}\n")

    def export_csv(self):
        # Ask user where to save CSV report
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if file_path:
            logs = database.get_all_logs()
            try:
                report.export_csv(logs, file_path)
                messagebox.showinfo('Success', f'CSV report exported to {file_path}')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to export CSV: {e}')
