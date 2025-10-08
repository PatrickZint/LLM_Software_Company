import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import json

import db
import encryption
import export_import
import user
import markdown

# Global variable to hold logged in user info
global_user = None

def login_window():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        usr = user.get_user(username)
        if usr is None:
            messagebox.showerror('Login Failed', 'User not found.')
            return
        if not user.check_password(password, usr['password_hash']):
            messagebox.showerror('Login Failed', 'Incorrect password.')
            return
        global global_user
        # Derive encryption key from user's password
        enc_key = encryption.derive_key(password)
        global_user = { 'id': usr['id'], 'username': username, 'encryption_key': enc_key }
        login.destroy()
        main_app()

    login = tk.Tk()
    login.title('Note-Taking App - Login')
    login.geometry('300x150')

    ttk.Label(login, text='Username:').pack(pady=5)
    username_entry = ttk.Entry(login)
    username_entry.pack()
    ttk.Label(login, text='Password:').pack(pady=5)
    password_entry = ttk.Entry(login, show='*')
    password_entry.pack()

    ttk.Button(login, text='Login', command=attempt_login).pack(pady=10)
    ttk.Button(login, text='Register', command=lambda: register_window(login)).pack()

    login.mainloop()


def register_window(parent):
    reg = tk.Toplevel(parent)
    reg.title('Register New User')
    reg.geometry('300x200')

    ttk.Label(reg, text='Username:').pack(pady=5)
    username_entry = ttk.Entry(reg)
    username_entry.pack()
    ttk.Label(reg, text='Password:').pack(pady=5)
    password_entry = ttk.Entry(reg, show='*')
    password_entry.pack()
    ttk.Label(reg, text='Confirm Password:').pack(pady=5)
    password2_entry = ttk.Entry(reg, show='*')
    password2_entry.pack()

    def register_action():
        username = username_entry.get()
        password = password_entry.get()
        password2 = password2_entry.get()
        if password != password2:
            messagebox.showerror('Error', 'Passwords do not match.')
            return
        if user.get_user(username) is not None:
            messagebox.showerror('Error', 'User already exists.')
            return
        user.register_user(username, password)
        messagebox.showinfo('Success', 'User registered successfully. You can now login.')
        reg.destroy()

    ttk.Button(reg, text='Register', command=register_action).pack(pady=10)


def main_app():
    app = tk.Tk()
    app.title('Note-Taking App')
    app.geometry('800x600')

    # Search Frame
    search_frame = ttk.Frame(app)
    search_frame.pack(fill=tk.X, padx=10, pady=5)
    ttk.Label(search_frame, text='Search:').pack(side=tk.LEFT, padx=5)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def refresh_note_list(query=""):
        for row in note_list.get_children():
            note_list.delete(row)
        notes = db.search_notes(global_user['id'], query)
        for note in notes:
            # Decrypt the note content for display if needed
            try:
                content = encryption.decrypt_data(global_user['encryption_key'], note['content'])
            except Exception as e:
                content = "<decryption error>"
            note_list.insert('', 'end', iid=note['id'], values=(note['title'], note['timestamp'], note['tags'], note['categories']))

    def on_search(*args):
        refresh_note_list(search_var.get())

    search_var.trace('w', on_search)

    # Note List Frame
    list_frame = ttk.Frame(app)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    columns = ('Title', 'Timestamp', 'Tags', 'Categories')
    note_list = ttk.Treeview(list_frame, columns=columns, show='headings')
    for col in columns:
        note_list.heading(col, text=col)
    note_list.pack(fill=tk.BOTH, expand=True)

    # Button Frame
    btn_frame = ttk.Frame(app)
    btn_frame.pack(fill=tk.X, padx=10, pady=5)
    ttk.Button(btn_frame, text='Create Note', command=lambda: open_note_editor()).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text='Edit Note', command=lambda: open_note_editor(edit=True)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text='Delete Note', command=lambda: delete_note()).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text='Preview Markdown', command=lambda: preview_note()).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text='Export Notes', command=lambda: export_import.export_notes(global_user['id'])).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text='Import Notes', command=lambda: import_notes()).pack(side=tk.LEFT, padx=5)

    def open_note_editor(edit=False):
        selected = None
        if edit:
            sel = note_list.selection()
            if not sel:
                messagebox.showwarning('Warning', 'No note selected.')
                return
            note_id = sel[0]
            selected = db.get_note_by_id(note_id)

        editor = tk.Toplevel(app)
        editor.title('Note Editor')
        editor.geometry('600x500')
        
        ttk.Label(editor, text='Title:').pack(pady=2)
        title_var = tk.StringVar()
        title_entry = ttk.Entry(editor, textvariable=title_var)
        title_entry.pack(fill=tk.X, padx=10)
        
        ttk.Label(editor, text='Tags (comma separated):').pack(pady=2)
        tags_var = tk.StringVar()
        tags_entry = ttk.Entry(editor, textvariable=tags_var)
        tags_entry.pack(fill=tk.X, padx=10)

        ttk.Label(editor, text='Categories (comma separated):').pack(pady=2)
        categories_var = tk.StringVar()
        categories_entry = ttk.Entry(editor, textvariable=categories_var)
        categories_entry.pack(fill=tk.X, padx=10)

        ttk.Label(editor, text='Markdown Content:').pack(pady=2)
        content_text = tk.Text(editor, height=15)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        if selected is not None:
            title_var.set(selected['title'])
            tags_var.set(selected['tags'])
            categories_var.set(selected['categories'])
            try:
                decrypted = encryption.decrypt_data(global_user['encryption_key'], selected['content'])
            except Exception as e:
                decrypted = ""
            content_text.insert('1.0', decrypted)

        def save_note():
            title = title_var.get()
            tags = tags_var.get()
            categories = categories_var.get()
            content = content_text.get('1.0', tk.END).strip()
            encrypted_content = encryption.encrypt_data(global_user['encryption_key'], content)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if edit and selected is not None:
                db.update_note(selected['id'], title, encrypted_content, timestamp, tags, categories)
            else:
                db.add_note(global_user['id'], title, encrypted_content, timestamp, tags, categories)
            refresh_note_list()
            editor.destroy()

        ttk.Button(editor, text='Save', command=save_note).pack(pady=5)

    def delete_note():
        sel = note_list.selection()
        if not sel:
            messagebox.showwarning('Warning', 'No note selected.')
            return
        note_id = sel[0]
        if messagebox.askyesno('Confirm', 'Are you sure you want to delete this note?'):
            db.delete_note(note_id)
            refresh_note_list()

    def preview_note():
        sel = note_list.selection()
        if not sel:
            messagebox.showwarning('Warning', 'No note selected.')
            return
        note_id = sel[0]
        note_data = db.get_note_by_id(note_id)
        try:
            decrypted = encryption.decrypt_data(global_user['encryption_key'], note_data['content'])
        except Exception as e:
            messagebox.showerror('Error', 'Could not decrypt note content.')
            return
        # Convert Markdown to HTML
        html_content = markdown.markdown(decrypted, extensions=['fenced_code'])

        preview = tk.Toplevel(app)
        preview.title('Markdown Preview')
        preview.geometry('600x500')
        text_widget = tk.Text(preview, wrap=tk.WORD)
        text_widget.insert('1.0', html_content)
        text_widget.pack(fill=tk.BOTH, expand=True)

    def import_notes():
        file_path = filedialog.askopenfilename(title='Select JSON file', filetypes=[('JSON Files', '*.json')])
        if file_path:
            result = export_import.import_notes(global_user['id'], file_path, global_user['encryption_key'])
            if result:
                messagebox.showinfo('Success', 'Notes imported successfully.')
                refresh_note_list()
            else:
                messagebox.showerror('Error', 'There was an error importing notes.')

    refresh_note_list()
    app.mainloop()


if __name__ == '__main__':
    db.initialize_db()
    login_window()