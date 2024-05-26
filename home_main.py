import tkinter as tk
from tkinter import messagebox, ttk, Text, Toplevel
from tkcalendar import Calendar
from datetime import datetime , date
from json.decoder import JSONDecodeError
import json
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap import Style



# Global list to store tasks
TASKS_FILE = "tasks.json"
tasks = []


# Function to load tasks from file
def load():
    global tasks
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        tasks = []

def save():
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file)
    except IOError:
        print("Error: Unable to save tasks to file.")


# Call load function when the application starts
load()
def add_task():
    win = Toplevel()
    win.title("Create Task")

    lbl_task_name = tk.Label(win, text="Task:")
    lbl_task_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_task_name = tk.Entry(win)
    entry_task_name.grid(row=0, column=1, padx=10, pady=5)

    lbl_due_date = tk.Label(win, text="Set Date:")
    lbl_due_date.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    cal_due_date = ttkb.DateEntry(win,bootstyle = "primary",dateformat='%Y-%m-%d')
    cal_due_date.grid(row=1, column=1, padx=10, pady=5)

    lbl_due_time = tk.Label(win, text="Set Time (HH:MM):")
    lbl_due_time.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_due_time = ttkb.Entry(win)
    entry_due_time.grid(row=2, column=1, padx=10, pady=5)

    lbl_priority = tk.Label(win, text="Priority:")
    lbl_priority.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    priority_values = ["High Priority", "Mid Priority", "Low Priority"]
    combo_priority = ttkb.Combobox(win,bootstyle = "primary", values=priority_values)
    combo_priority.current(0)
    combo_priority.grid(row=3, column=1, padx=10, pady=5)

    def save_task():
        task_name = entry_task_name.get()
        due_date = cal_due_date.entry.get()
        due_time = entry_due_time.get()
        due_datetime = f"{due_date} {due_time}"
        priority = combo_priority.get()

        tasks.append({"name": task_name, "due_datetime": due_datetime, "priority": priority, "status": "To Do", "notes": ""})
        save()
        messagebox.showinfo("Success", "Task added successfully!")
        win.destroy()
        update_kanban_board()

    def save_n_check():
        save_task()

    btn_save = tk.Button(win, text="Save", command=save_n_check)
    btn_save.grid(row=4, column=0, columnspan=2, pady=10)


def update_kanban_board():
    global trees
    for column, tree in trees.items():
        for item in tree.get_children():
            tree.delete(item)
        for task in tasks:
            if task.get("status") == column:
                task_name = task.get("name", "")
                due_datetime = task.get("due_datetime", "")
                priority = task.get("priority", "")
                tree.insert("", "end", values=(task_name, due_datetime, priority))


def delete_task(tree, column_name):
    selected_item = tree.selection()
    if not selected_item:
        show_error("Please select a task to delete.")
        return

    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected task?")
    if not confirmed:
        return

    for item in selected_item:
        task_name = tree.item(item, "values")[0]
        for task in tasks:
            if task["name"] == task_name:
                tasks.remove(task)
                save()
                tree.delete(item)
                update_kanban_board()

def check_due_dates():
    current_datetime = datetime.now()
    matching_tasks = []

    for task in tasks:
        due_datetime = current_datetime.strptime(task["due_datetime"], "%Y-%m-%d %H:%M")
        time_difference_hours = (due_datetime - current_datetime).total_seconds() / 3600
        if 0 < time_difference_hours <= 24:
            matching_tasks.append((task["name"], task["due_datetime"]))


    if matching_tasks:
        tasks_info = '\n'.join(f'• {task[0]} @ {task[1]}' for task in matching_tasks)
        messagebox.showinfo("Reminder", f"The following tasks are due within the next 24 hours:\n\n{tasks_info}")
    else:
        messagebox.showinfo("No Tasks", "No tasks are due within the next 24 hours.")


def show_error(message):
    messagebox.showerror("Error", message)


def show_home_screen():
        
        home_window = ttkb.Window(themename="spmain")
        home_window.title("Trails")

        style = ttkb.Style()
        style.configure("TLabel", font=("Yu gothic",40))  # Set font size to 20 for all labels
        style.configure("TButton", font=("Yu gothic", 14))

        # Get screen width and height
        screen_width = home_window.winfo_screenwidth()
        screen_height = home_window.winfo_screenheight()


        # Set window size to match screen size
        home_window.geometry(f"{screen_width}x{screen_height}")

        header_frame = ttkb.Label(home_window, background = "#d90000")
        header_frame.pack(fill="x", padx = 20,pady =(10,2))

        lbl_username = ttkb.Label(header_frame, text="Welcome to Trails!", font=("Yu gothic", 16), foreground = "white",background = "#d90000")
        lbl_username.pack(fill = "y",side="left", padx = 10, pady = 5)

        nav_frame = ttkb.Labelframe(home_window, bootstyle = "primary")
        nav_frame.pack(side="left", fill="both", pady = (5,25), padx = (20,5))

        btn_add_task_nav = ttkb.Button(nav_frame,bootstyle ="primary", text="Add Task",width=25,command = add_task)
        btn_add_task_nav.pack(padx=10, pady=5, fill = "x")

        
        def move_task_nav():
            move_task_window = Toplevel()
            move_task_window.title("Move Task")

            lbl_select_task = tk.Label(move_task_window, text="Select Task:")
            lbl_select_task.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            task_names = [task["name"] for task in tasks]
            combo_task_names = ttk.Combobox(move_task_window, values=task_names)
            combo_task_names.grid(row=0, column=1, padx=10, pady=5)

            lbl_select_status = tk.Label(move_task_window, text="Move to Status:")
            lbl_select_status.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            
            status_values = ["To Do", "In Progress", "Done"]
            combo_status_values = ttk.Combobox(move_task_window, values=status_values)
            combo_status_values.grid(row=1, column=1, padx=10, pady=5)

            def move_task():
                selected_task_name = combo_task_names.get()
                selected_status = combo_status_values.get()
                for task in tasks:
                    if task["name"] == selected_task_name:
                        task["status"] = selected_status
                        save()
                        update_kanban_board()
                        messagebox.showinfo("Success", "Task moved successfully!")
                        move_task_window.destroy()
                        break

            btn_move_task = tk.Button(move_task_window, text="Move", command=move_task)
            btn_move_task.grid(row=2, column=0, columnspan=2, pady=10)

        btn_move_task_nav = ttkb.Button(nav_frame,bootstyle ="secondary", text="Move Task", width = 25, command=move_task_nav)
        btn_move_task_nav.pack(padx=10, pady=5, fill = "x")

        def archive_task_nav():
            archive_task_window = Toplevel()
            archive_task_window.title("Archive Task")

            lbl_select_task = tk.Label(archive_task_window, text="Select Task:")
            lbl_select_task.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            task_names = [task["name"] for task in tasks]
            combo_task_names = ttk.Combobox(archive_task_window, values=task_names)
            combo_task_names.grid(row=0, column=1, padx=10, pady=5)

            def archive_task():
                selected_task_name = combo_task_names.get()
                for task in tasks:
                    if task["name"] == selected_task_name:
                        task["status"] = "Archived"
                        save()
                        update_kanban_board()
                        messagebox.showinfo("Success", "Task archived successfully!")
                        archive_task_window.destroy()
                        break

            btn_archive_task = tk.Button(archive_task_window, text="Archive", command=archive_task)
            btn_archive_task.grid(row=1, column=0, columnspan=2, pady=10)

        btn_archive_task_nav = ttkb.Button(nav_frame,bootstyle = "warning", text="Archive Task", command=archive_task_nav)
        btn_archive_task_nav.pack(padx=10, pady=5, fill = "x")
        def edit_task_nav():
            edit_task_window = Toplevel()
            edit_task_window.title("Edit Task")

            lbl_select_task = ttkb.Label(edit_task_window, text="Select Task:")
            lbl_select_task.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            task_names = [task["name"] for task in tasks]
            combo_task_names = ttk.Combobox(edit_task_window, values=task_names)
            combo_task_names.grid(row=0, column=1, padx=10, pady=5)

            def load_task_details():
                selected_task_name = combo_task_names.get()
                for task in tasks:
                    if task["name"] == selected_task_name:
                        entry_task_name.delete(0, tk.END)
                        entry_task_name.insert(0, task["name"])
                        #cal_due_date.set_date(["due_datetime"].split()[0])
                        entry_due_time.delete(0, tk.END)
                        entry_due_time.insert(0, task["due_datetime"].split()[1])
                        combo_priority.set(task["priority"])
                        break

            btn_load_task = tk.Button(edit_task_window, text="Load", command=load_task_details)
            btn_load_task.grid(row=1, column=0, columnspan=2, pady=10)

            lbl_task_name = tk.Label(edit_task_window, text="Task:")
            lbl_task_name.grid(row=2, column=0, padx=10, pady=5, sticky="e")
            entry_task_name = tk.Entry(edit_task_window)
            entry_task_name.grid(row=2, column=1, padx=10, pady=5)

            lbl_due_date = tk.Label(edit_task_window, text="Set Date:")
            lbl_due_date.grid(row=3, column=0, padx=10, pady=5, sticky="e")
            cal_due_date = ttkb.DateEntry(edit_task_window, bootstyle = "primary",dateformat='%Y-%m-%d')
            cal_due_date.grid(row=3, column=1, padx=10, pady=5)

            lbl_due_time = tk.Label(edit_task_window, text="Set Time (HH:MM):")
            lbl_due_time.grid(row=4, column=0, padx=10, pady=5, sticky="e")
            entry_due_time = tk.Entry(edit_task_window)
            entry_due_time.grid(row=4, column=1, padx=10, pady=5)

            lbl_priority = tk.Label(edit_task_window, text="Priority:")
            lbl_priority.grid(row=5, column=0, padx=10, pady=5, sticky="e")
            priority_values = ["High Priority", "Mid Priority", "Low Priority"]
            combo_priority = ttk.Combobox(edit_task_window, values=priority_values)
            combo_priority.current(0)
            combo_priority.grid(row=5, column=1, padx=10, pady=5)

            def save_edited_task():
                selected_task_name = combo_task_names.get()
                for task in tasks:
                    if task["name"] == selected_task_name:
                        task["name"] = entry_task_name.get()
                        due_date = cal_due_date.entry.get()
                        due_time = entry_due_time.get()
                        task["due_datetime"] = f"{due_date} {due_time}"
                        task["priority"] = combo_priority.get()
                        save()
                        update_kanban_board()
                        messagebox.showinfo("Success", "Task updated successfully!")
                        edit_task_window.destroy()
                        break

            btn_save_edited_task = tk.Button(edit_task_window, text="Save", command=save_edited_task)
            btn_save_edited_task.grid(row=6, column=0, columnspan=2, pady=10)

        btn_edit_task_nav = ttkb.Button(nav_frame,bootstyle = "danger", text="Edit Task", command=edit_task_nav)
        btn_edit_task_nav.pack(fill="x", padx=10, pady=5)

        def create_kanban_column(parent, column_name):
            frame = ttkb.Labelframe(home_window, bootstyle = "selectbg")
            frame.pack(side="left", fill="y", expand=True, padx=10, pady=(5,25))

            label = tk.Label(frame, text=column_name, font=("Helvetica", 14), bg="#f0f0f0")
            label.pack(pady=5)

            tree = ttkb.Treeview(frame,bootstyle ="secondary", columns=("Task Name", "Due Date", "Priority"), show="headings")
            tree.heading("Task Name", text="Task Name", command=lambda: sort_column(tree, "Task Name"))
            tree.heading("Due Date", text="Due Date", command=lambda: sort_column(tree, "Due Date"))
            tree.heading("Priority", text="Priority", command=lambda: sort_column(tree, "Priority"))
            tree.pack(fill="both", expand=True)
            
            

            def on_tree_select(event):
                show_notes(event, tree)

            tree.bind("<ButtonRelease-1>", on_tree_select)

            delete_button = ttkb.Button(frame, text="Delete Task",width = 25, command=lambda: delete_task(tree, column_name))
            delete_button.pack(pady=5)

            return tree

        def show_notes(event, tree):
            selected_item = tree.selection()
            if not selected_item:
                return

            task_name = tree.item(selected_item[0], "values")[0]
            for task in tasks:
                if task["name"] == task_name:
                    notes = task.get("notes", "")
                    break
            else:
                notes = ""

            notes_window = Toplevel()
            notes_window.title("Task Notes")
            notes_text = Text(notes_window, width=40, height=20)
            notes_text.pack(padx=10, pady=10)
            notes_text.insert("1.0", notes)

            def save_notes():
                task["notes"] = notes_text.get("1.0", "end-1c")
                save()
                notes_window.destroy()

            btn_save_notes = tk.Button(notes_window, text="Save Notes", command=save_notes)
            btn_save_notes.pack(pady=10)

        def sort_column(tree, col):
            l = [(tree.set(k, col), k) for k in tree.get_children("")]
            l.sort(reverse=True)

            for index, (val, k) in enumerate(l):
                tree.move(k, "", index)

            tree.heading(col, command=lambda: sort_column(tree, col))

        main_frame = tk.Frame(home_window)
        main_frame.pack(side="left", expand=True, fill="both")

        global trees
        columns = ["To Do", "In Progress", "Done"]
        trees = {}
        for column in columns:
            trees[column] = create_kanban_column(main_frame, column)
            trees[column].pack(expand = True)

        def toggle_menu():
            if menu.winfo_ismapped():
                menu.unpost()
            else:
                menu.post(btn_hamburger.winfo_rootx(), btn_hamburger.winfo_rooty() + btn_hamburger.winfo_height())

        menu = tk.Menu(home_window, tearoff=0)
        menu.add_separator()
        menu.add_command(label="Close", command=home_window.quit)

        btn_hamburger = ttkb.Button(header_frame,bootstyle = "primary.outline", text="\u2630", command=toggle_menu)
        btn_hamburger.pack(side="right", padx=10, pady=5)

        update_kanban_board()
        check_due_dates()
        home_window.mainloop()

show_home_screen()