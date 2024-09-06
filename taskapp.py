import tkinter as tk
from tkinter import ttk
import calendar
import datetime
import json

def add_task():
    task_name = task_entry.get()
    due_date_str = due_date_entry.get()

    try:
        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
    except ValueError:
        return

    tasks.append({"name": task_name, "due_date": due_date_str})
    save_tasks()
    update_task_list()
    task_entry.delete(0, tk.END) 
    due_date_entry.delete(0, tk.END)

def delete_task():
    try:
        selected_task_index = task_list.curselection()[0]
        del tasks[selected_task_index]
        save_tasks()
        update_task_list()
    except IndexError:
        pass 

def edit_task():
    try:
        selected_task_index = task_list.curselection()[0]
        task = tasks[selected_task_index]

        def save_edit():
            task["name"] = edit_name_entry.get()
            task["due_date"] = edit_due_date_entry.get()
            save_tasks()
            update_task_list()
            edit_window.destroy()

        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Task")

        edit_name_label = ttk.Label(edit_window, text="Task:")
        edit_name_label.grid(row=0, column=0)
        edit_name_entry = ttk.Entry(edit_window)
        edit_name_entry.insert(0, task["name"])
        edit_name_entry.grid(row=0, column=1)

        edit_due_date_label = ttk.Label(edit_window, text="Due Date:")
        edit_due_date_label.grid(row=1, column=0)
        edit_due_date_entry = ttk.Entry(edit_window)
        edit_due_date_entry.insert(0, task["due_date"])
        edit_due_date_entry.grid(row=1, column=1)

        save_button = ttk.Button(edit_window, text="Save", command=save_edit)
        save_button.grid(row=2, column=0, columnspan=2)

    except IndexError:
        pass

def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, f"{task['name']} - Due: {task['due_date']}")

def show_calendar():
    year = datetime.date.today().year
    month = datetime.date.today().month
    cal_str = calendar.month(year, month)

    calendar_window = tk.Toplevel(window)
    calendar_window.title("Calendar View")
    calendar_label = ttk.Label(calendar_window, text=cal_str)
    calendar_label.pack()


def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)


window = tk.Tk()
window.title("Task Manager")


task_label = ttk.Label(window, text="Task:")
task_label.grid(row=0, column=0, padx=5, pady=5)
task_entry = ttk.Entry(window)
task_entry.grid(row=0, column=1, padx=5, pady=5)

due_date_label = ttk.Label(window, text="Due Date (YYYY-MM-DD):")
due_date_label.grid(row=1, column=0, padx=5, pady=5)
due_date_entry = ttk.Entry(window) 
due_date_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = ttk.Button(window, text="Add Task", command=add_task)
add_button.grid(row=2, column=0, columnspan=2, pady=5)


task_list = tk.Listbox(window)
task_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

delete_button = ttk.Button(window, text="Delete Task", command=delete_task)
delete_button.grid(row=4, column=0, pady=5)

edit_button = ttk.Button(window, text="Edit Task", command=edit_task)
edit_button.grid(row=4, column=1, pady=5)

calendar_button = ttk.Button(window, text="Calendar View", command=show_calendar)
calendar_button.grid(row=5, column=0, columnspan=2, pady=5)

tasks = load_tasks()
update_task_list()

window.mainloop()