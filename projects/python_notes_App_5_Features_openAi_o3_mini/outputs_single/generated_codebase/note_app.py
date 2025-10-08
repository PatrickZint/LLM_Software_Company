import tkinter as tk
from tkinter import messagebox, filedialog
from database import create_note, update_note, delete_note, get_notes_by_user, search_notes
from encryption_helper import encrypt_text, decrypt_text
import json
from datetime import datetime


class NoteApp(tk.Tk):
    def __init__(self, user, encryption_key):
        super().__init__()
        self.title("Note App")
        self.geometry("800x600")
        self.user = user
        self.encryption_key = encryption_key

        # Search bar
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_notes).pack(side=tk.LEFT, padx=5)

        # Notes list
        self.notes_listbox = tk.Listbox(self, width=80)
        self.notes_listbox.pack(pady=10)
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_note)

        # Note details
        details_frame = tk.Frame(self)
        details_frame.pack(pady=5)

        tk.Label(details_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(details_frame, textvariable=self.title_var, width=80)
        self.title_entry.grid(row=0, column=1, pady=5)

        tk.Label(details_frame, text="Content:").grid(row=1, column=0, sticky=tk.NW)
        self.content_text = tk.Text(details_frame, width=60, height=15)
        self.content_text.grid(row=1, column=1, pady=5)

        tk.Label(details_frame, text="Tags (comma separated):").grid(row=2, column=0, sticky=tk.W)
        self.tags_entry = tk.Entry(details_frame, width=80)
        self.tags_entry.grid(row=2, column=1, pady=5)

        tk.Label(details_frame, text="Category:").grid(row=3, column=0, sticky=tk.W)
        self.category_entry = tk.Entry(details_frame, width=80)
        self.category_entry.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add Note", command=self.add_note).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Note", command=self.update_note).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Note", command=self.delete_note).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Export Notes", command=self.export_notes).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Import Notes", command=self.import_notes).grid(row=0, column=4, padx=5)

        self.selected_note = None
        self.refresh_notes()

    def refresh_notes(self, notes=None):
        self.notes_listbox.delete(0, tk.END)
        if notes is None:
            notes = get_notes_by_user(self.user['id'])
        self.notes = notes
        for note in notes:
            # Display the note title and timestamp
            display = f"{note['title']} - {note['timestamp']}"
            self.notes_listbox.insert(tk.END, display)

    def load_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            note = self.notes[index]
            self.selected_note = note
            self.title_var.set(note['title'])
            try:
                content = decrypt_text(self.encryption_key, note['content'])
            except Exception:
                content = "[Decryption Error]"
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, content)
            self.tags_entry.delete(0, tk.END)
            self.tags_entry.insert(0, note['tags'] if note['tags'] else "")
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, note['category'] if note['category'] else "")

    def add_note(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        tags = self.tags_entry.get()
        category = self.category_entry.get()
        if not title or not content:
            messagebox.showerror("Error", "Title and content cannot be empty")
            return
        
        encrypted_content = encrypt_text(self.encryption_key, content)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_note(self.user['id'], title, encrypted_content, timestamp, tags, category)
        messagebox.showinfo("Success", "Note added successfully!")
        self.refresh_notes()

    def update_note(self):
        if not self.selected_note:
            messagebox.showerror("Error", "No note selected")
            return
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END).strip()
        tags = self.tags_entry.get()
        category = self.category_entry.get()
        if not title or not content:
            messagebox.showerror("Error", "Title and content cannot be empty")
            return
        
        encrypted_content = encrypt_text(self.encryption_key, content)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_note(self.selected_note['id'], title, encrypted_content, timestamp, tags, category)
        messagebox.showinfo("Success", "Note updated successfully!")
        self.refresh_notes()

    def delete_note(self):
        if not self.selected_note:
            messagebox.showerror("Error", "No note selected")
            return
        delete_note(self.selected_note['id'])
        messagebox.showinfo("Success", "Note deleted successfully!")
        self.refresh_notes()

    def search_notes(self):
        query = self.search_var.get()
        if query.strip() == "":
            self.refresh_notes()
        else:
            notes = search_notes(self.user['id'], query)
            self.refresh_notes(notes)

    def export_notes(self):
        notes = get_notes_by_user(self.user['id'])
        export_data = []
        for note in notes:
            try:
                content = decrypt_text(self.encryption_key, note['content'])
            except Exception:
                content = "[Decryption Error]"
            export_data.append({
                "title": note['title'],
                "content": content,
                "timestamp": note['timestamp'],
                "tags": note['tags'],
                "category": note['category']
            })
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=4)
            messagebox.showinfo("Success", "Notes exported successfully!")

    def import_notes(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                imported_notes = json.load(f)
            for note in imported_notes:
                encrypted_content = encrypt_text(self.encryption_key, note["content"])
                create_note(self.user['id'], note["title"], encrypted_content, note["timestamp"], note.get("tags", ""), note.get("category", ""))
            messagebox.showinfo("Success", "Notes imported successfully!")
            self.refresh_notes()
