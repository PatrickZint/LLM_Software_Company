import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from csv_exporter import export_logs_to_csv
from database import get_db_connection
from database import log_file_movement
import os

# UI for the file organizer

def start_ui(config, monitor, db_path):
    root = tk.Tk()
    root.title("Automated File Organizer")

    # Frame for controls
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Button to manually trigger file organization
    def manual_organize():
        threading.Thread(target=monitor.manual_trigger, daemon=True).start()
        messagebox.showinfo("Manual Trigger", "File organization triggered.")

    organize_button = ttk.Button(frame, text="Organize Files", command=manual_organize)
    organize_button.grid(row=0, column=0, padx=5, pady=5)

    # Button to export CSV logs
    def csv_export():
        # For simplicity, using the export path from config
        export_path = config.get('csv_export', {}).get('export_path', 'logs_export.csv')
        # Optionally, you could add UI elements for filtering
        export_logs_to_csv(db_path, export_path)
        messagebox.showinfo("CSV Export", f"CSV logs exported to {export_path}")

    export_button = ttk.Button(frame, text="Export CSV Logs", command=csv_export)
    export_button.grid(row=0, column=1, padx=5, pady=5)

    # Frame for log display
    log_frame = ttk.Frame(root, padding=10)
    log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    log_text = tk.Text(log_frame, width=80, height=20)
    log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=log_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y')
    log_text['yscrollcommand'] = scrollbar.set

    # Function to update log display from the database
    def update_logs():
        try:
            conn = get_db_connection(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT original_path, destination_path, timestamp, sorting_rule FROM file_logs ORDER BY id DESC LIMIT 50")
            rows = cursor.fetchall()
            conn.close()
            log_text.delete(1.0, tk.END)
            for row in rows:
                log_text.insert(tk.END, f"{row}\n")
        except Exception as e:
            log_text.insert(tk.END, f"Error fetching logs: {e}\n")
        # Schedule next update after 5 seconds
        root.after(5000, update_logs)

    update_logs()

    root.mainloop()
