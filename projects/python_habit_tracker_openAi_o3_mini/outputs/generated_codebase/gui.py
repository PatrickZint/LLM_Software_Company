import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
from db import add_habit, update_habit, delete_habit, get_all_habits, add_completion
from export import export_habit_to_csv
from charts import plot_habit_progress


class HabitTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Habit Tracker')
        self.geometry('800x600')
        self.create_widgets()
        self.refresh_habit_list()

    def create_widgets(self):
        # Habit List
        self.habit_list = ttk.Treeview(self, columns=('ID', 'Name', 'Schedule'), show='headings')
        self.habit_list.heading('ID', text='ID')
        self.habit_list.heading('Name', text='Name')
        self.habit_list.heading('Schedule', text='Schedule')
        self.habit_list.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X)

        add_btn = tk.Button(btn_frame, text='Add Habit', command=self.add_habit)
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)

        edit_btn = tk.Button(btn_frame, text='Edit Habit', command=self.edit_habit)
        edit_btn.pack(side=tk.LEFT, padx=5, pady=5)

        del_btn = tk.Button(btn_frame, text='Delete Habit', command=self.delete_habit)
        del_btn.pack(side=tk.LEFT, padx=5, pady=5)

        complete_btn = tk.Button(btn_frame, text='Mark as Completed', command=self.mark_completed)
        complete_btn.pack(side=tk.LEFT, padx=5, pady=5)

        export_btn = tk.Button(btn_frame, text='Export CSV', command=self.export_csv)
        export_btn.pack(side=tk.LEFT, padx=5, pady=5)

        chart_btn = tk.Button(btn_frame, text='View Chart', command=self.view_chart)
        chart_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def refresh_habit_list(self):
        for item in self.habit_list.get_children():
            self.habit_list.delete(item)
        habits = get_all_habits()
        for habit in habits:
            self.habit_list.insert('', tk.END, values=(habit['id'], habit['name'], habit['schedule_type']))
    
    def add_habit(self):
        name = simpledialog.askstring('Habit Name', 'Enter the habit name:')
        if not name:
            return
        description = simpledialog.askstring('Description', 'Enter description (optional):')
        schedule_type = simpledialog.askstring('Schedule Type', 'Enter schedule type (daily/weekly):')
        goal = simpledialog.askstring('Goal', 'Enter the goal:')
        expected_frequency = simpledialog.askinteger('Expected Frequency', 'Enter expected frequency:')
        start_date = simpledialog.askstring('Start Date', 'Enter start date (YYYY-MM-DD):')
        end_date = simpledialog.askstring('End Date', 'Enter end date (YYYY-MM-DD) or leave blank for ongoing:')
        if end_date == '':
            end_date = None
        habit_id = add_habit(name, description, schedule_type, goal, expected_frequency, start_date, end_date)
        messagebox.showinfo('Success', f'Habit added with ID: {habit_id}')
        self.refresh_habit_list()
    
    def edit_habit(self):
        selected = self.habit_list.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Select a habit to edit.')
            return
        item = self.habit_list.item(selected[0])
        habit_id = item['values'][0]
        name = simpledialog.askstring('Habit Name', 'Enter the new habit name:')
        if not name:
            return
        description = simpledialog.askstring('Description', 'Enter new description (optional):')
        schedule_type = simpledialog.askstring('Schedule Type', 'Enter schedule type (daily/weekly):')
        goal = simpledialog.askstring('Goal', 'Enter the new goal:')
        expected_frequency = simpledialog.askinteger('Expected Frequency', 'Enter expected frequency:')
        start_date = simpledialog.askstring('Start Date', 'Enter start date (YYYY-MM-DD):')
        end_date = simpledialog.askstring('End Date', 'Enter end date (YYYY-MM-DD) or leave blank for ongoing:')
        if end_date == '':
            end_date = None
        update_habit(habit_id, name, description, schedule_type, goal, expected_frequency, start_date, end_date)
        messagebox.showinfo('Success', 'Habit updated.')
        self.refresh_habit_list()
    
    def delete_habit(self):
        selected = self.habit_list.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Select a habit to delete.')
            return
        item = self.habit_list.item(selected[0])
        habit_id = item['values'][0]
        response = messagebox.askyesno('Confirm', 'Are you sure you want to delete this habit?')
        if response:
            delete_habit(habit_id)
            messagebox.showinfo('Deleted', 'Habit deleted.')
            self.refresh_habit_list()
    
    def mark_completed(self):
        selected = self.habit_list.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Select a habit to mark as completed.')
            return
        item = self.habit_list.item(selected[0])
        habit_id = item['values'][0]
        date = simpledialog.askstring('Date', 'Enter completion date (YYYY-MM-DD):',
                                        initialvalue=datetime.date.today().strftime('%Y-%m-%d'))
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        add_completion(habit_id, date, timestamp)
        messagebox.showinfo('Success', 'Habit marked as completed.')
    
    def export_csv(self):
        selected = self.habit_list.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Select a habit to export.')
            return
        item = self.habit_list.item(selected[0])
        habit_id = item['values'][0]
        filename = export_habit_to_csv(habit_id)
        messagebox.showinfo('CSV Exported', f'Data exported to {filename}')
    
    def view_chart(self):
        selected = self.habit_list.selection()
        if not selected:
            messagebox.showwarning('Warning', 'Select a habit to view chart.')
            return
        item = self.habit_list.item(selected[0])
        habit_id = item['values'][0]
        plot_habit_progress(habit_id)


if __name__ == '__main__':
    app = HabitTrackerGUI()
    app.mainloop()
