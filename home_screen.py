import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
#from tkinter import simpledialog
from json.decoder import JSONDecodeError

# Global list to store tasks
TASKS_FILE = "tasks.json"

# Function to load tasks from file
def load():
    global tasks
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        tasks = []

# Function to save tasks to file
def save():
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file)
    except IOError:
        print("Error: Unable to save tasks to file.")

# Call load function when the application starts
load()

def add_task():
    # Create a new window for adding tasks
    add_task_window = tk.Toplevel()
    add_task_window.title("Create Task")

    # Label and entry for task name
    lbl_task_name = tk.Label(add_task_window, text="Task:")
    lbl_task_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_task_name = tk.Entry(add_task_window)
    entry_task_name.grid(row=0, column=1, padx=10, pady=5)

    # Calendar for selecting due date
    lbl_due_date = tk.Label(add_task_window, text="Set Date:")
    lbl_due_date.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    cal_due_date = Calendar(add_task_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal_due_date.grid(row=1, column=1, padx=10, pady=5)

    # Combobox for selecting due time
    lbl_due_time = tk.Label(add_task_window, text="Set Time:")
    lbl_due_time.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    combo_due_time = ttk.Combobox(add_task_window, values=[f"{h:02}:{m:02}" for h in range(24) for m in range(0, 60, 15)])
    combo_due_time.current(0)  # Default to the first time slot
    combo_due_time.grid(row=2, column=1, padx=10, pady=5)

    # Function to save the task with name, due date, and time
    def save_task():
        task_name = entry_task_name.get()
        due_date = cal_due_date.get_date()
        due_time = combo_due_time.get()
        due_datetime = f"{due_date} {due_time}"
        # Save the task to the global list
        tasks.append({"name": task_name, "due_datetime": due_datetime, "notes": ""})  # Initialize notes as empty string
        save()
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()

    # Button to save the task
    btn_save = tk.Button(add_task_window, text="Save", command=save_task)
    btn_save.grid(row=3, column=0, columnspan=2, pady=10)

def delete_task(tree):
    # Function to delete selected task
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

def check_due_dates():
    # Get the current date
    current_datetime = datetime.now()

    # List to store tasks with matching deadlines
    matching_tasks = []
    date_due = []

    # Iterate through tasks
    for task in tasks:
        # Parse the due date and time from the due_datetime string
        due_datetime = datetime.strptime(task["due_datetime"], "%Y-%m-%d %H:%M")
        #str_due_date = str(due_datetime)
        # Check if the due date is within one day from now
        if current_datetime < due_datetime <= current_datetime + timedelta(days=1):
            matching_tasks.append(task["name"])
            date_due.append(task["due_datetime"])

    # If there are matching tasks, display them in a single messagebox
    if matching_tasks:
        tasks_info = '\n'.join(f'• {task} @ {date_due}' for task, date_due in zip(matching_tasks, date_due))
        messagebox.showinfo("Reminder", f"The following tasks are due within the next 24 hours:\n\n{tasks_info}")
    else:
        messagebox.showinfo("No Tasks", "No tasks are due within the next 24 hours.")

def view_tasks():
    # Create a new window for viewing tasks
    view_tasks_window = tk.Toplevel()
    view_tasks_window.title("View Tasks")

    # Create a label to display instructions
    lbl_instructions = tk.Label(view_tasks_window, text="List of Tasks:")
    lbl_instructions.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    # Create a treeview widget to display tasks
    tree = ttk.Treeview(view_tasks_window, columns=("Task Name", "Due Date"), show="headings")
    tree.heading("Task Name", text="Task Name")
    tree.heading("Due Date", text="Due Date")
    tree.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # Add tasks to the treeview
    for task in tasks:
        task_name = task.get("name", "")
        due_datetime = task.get("due_datetime", "")
        tree.insert("", "end", values=(task_name, due_datetime))

    # Add scrollbar to the treeview
    scrollbar = ttk.Scrollbar(view_tasks_window, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # Create a text widget for notepad
    txt_notepad = tk.Text(view_tasks_window, wrap="word")
    txt_notepad.grid(row=1, column=2, rowspan=4, padx=10, pady=5, sticky="nsew")  # Adjust rowspan as needed

    def edit_task_due_date(tree, parent_window):
        selected_item = tree.selection()
        if not selected_item:
            show_error("Please select a task to edit.")
            return

        # Assuming the task name is in the first column
        task_name = tree.item(selected_item[0], "values")[0]

        # Create a new window for editing the due date
        edit_due_date_window = tk.Toplevel(parent_window)
        edit_due_date_window.title("Edit Due Date")

        # Calendar for selecting new due date
        cal_new_due_date = Calendar(edit_due_date_window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal_new_due_date.grid(row=0, column=0, padx=10, pady=5)

        # Combobox for selecting new due time
        times = [f"{hour:02d}:00" for hour in range(24)]  # Generates "00:00", "01:00", ..., "23:00"
        combo_new_due_time = ttk.Combobox(edit_due_date_window, values=times)
        combo_new_due_time.current(0)
        combo_new_due_time.grid(row=1, column=0, padx=10, pady=5)

        # Function to update the due date in real-time
        def update_due_date():
            new_due_date = cal_new_due_date.get_date()
            new_due_time = combo_new_due_time.get()
            new_due_datetime = f"{new_due_date} {new_due_time}"
            # Update the task in the global tasks list
            for task in tasks:
                if task["name"] == task_name:
                    task["due_datetime"] = new_due_datetime
                    tree.item(selected_item, values=(task["name"], task["due_datetime"])) #Update the due datetime in the treeview
                    save()
                    messagebox.showinfo("Success", "Due date updated successfully!")
                    edit_due_date_window.destroy()
                    return

        # Button to save the new due date
        btn_save_new_due_date = tk.Button(edit_due_date_window, text="Save", command=update_due_date)
        btn_save_new_due_date.grid(row=2, column=0, pady=10)

    # Function to load notes for selected task
    def load_notes():
        selected_item = tree.selection()
        if selected_item:
            task_name = tree.item(selected_item, "values")[0]
            for task in tasks:
                if task.get("name") == task_name:
                    notes = task.get("notes", "")
                    txt_notepad.delete("1.0", tk.END)  # Clear existing notes
                    txt_notepad.insert(tk.END, notes)  # Load notes for selected task
                    return  # Exit function if notes are found
        # Clear text widget if no notes found
        txt_notepad.delete("1.0", tk.END)

    # Bind treeview selection to load notes
    tree.bind("<<TreeviewSelect>>", lambda event: load_notes())

    # Button to delete selected task
    btn_delete_task = tk.Button(view_tasks_window, text="Delete Task", command=lambda: delete_task(tree))
    btn_delete_task.grid(row=2, column=0, pady=5, sticky="ew")

    # Button to edit due date of selected task
    btn_edit_due_date = tk.Button(view_tasks_window, text="Edit Due Date", command=lambda: edit_task_due_date(tree, view_tasks_window))
    btn_edit_due_date.grid(row=3, column=0, pady=5, sticky="ew")

    # Function to save notes for selected task
    def save_notes():
        selected_item = tree.selection()
        if selected_item:
            task_name = tree.item(selected_item, "values")[0]
            for task in tasks:
                if task.get("name") == task_name:
                    task["notes"] = txt_notepad.get("1.0", tk.END).strip()  # Update notes for selected task
                    save()
                    messagebox.showinfo("Success", "Notes saved successfully!")
                    return

    # Add a button to save notes
    btn_save_notes = tk.Button(view_tasks_window, text="Save Notes", command=save_notes)
    btn_save_notes.grid(row=5, column=2, pady=10, sticky="e")

    center_window(view_tasks_window)
    # Function to delete selected task
def show_error(message):
    messagebox.showerror("Error", message)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def logout(home_window, login_window):
    save()
    home_window.destroy()
    login_window.deiconify()

def show_home_screen(username, login_window):
    home_window = tk.Tk()
    home_window.title("Trails")

    # Set the dimensions of the home window to be the same as the login window
    width_pixels = int(login_window.winfo_width())
    height_pixels = int(login_window.winfo_height())
    home_window.geometry(f"{width_pixels}x{height_pixels}")

    # Center the window
    center_window(home_window)

    # Create a header frame
    header_frame = tk.Frame(home_window, bg="#e21818")  # Set background color to empty string for transparency
    header_frame.pack(fill="x")

    # Make the row and column expandable
    home_window.rowconfigure(0, weight=0)
    home_window.columnconfigure(0, weight=1)

    # Create a label to display the username in the header
    lbl_username = tk.Label(header_frame, text=f"{username}'s Trails!", font=("yu gothic ui", 12, "bold"), bg="#e21818", fg="white", padx=10, pady=5)
    lbl_username.pack(side="left")

    # Function to toggle the menu
    def toggle_menu():
        if menu.winfo_ismapped():
            menu.unpost()
        else:
            menu.post(btn_hamburger.winfo_rootx(), btn_hamburger.winfo_rooty() + btn_hamburger.winfo_height())

    # Create a menu
    menu = tk.Menu(home_window, tearoff=0)
    menu.add_command(label="Tasks", command=view_tasks)
    menu.add_command(label="Notifications", command=check_due_dates)
    menu.add_command(label="Logout", command=lambda: logout(home_window, login_window))
    menu.add_separator()
    menu.add_command(label="Close", command=home_window.quit)

    # Create a hamburger button
    btn_hamburger = tk.Button(header_frame, text="\u2630", command=toggle_menu, font=("Arial", 12), bg="#e21818", fg="white", bd=0)
    btn_hamburger.pack(side="right", padx=10, pady=5)

    # Create a main frame for content
    main_frame = tk.Frame(home_window)
    main_frame.pack(expand=True, fill="both")

    # Make the row and column expandable
    home_window.rowconfigure(1, weight=1)
    home_window.columnconfigure(0, weight=1)

    # Add Calendar widget
    cal = Calendar(main_frame, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(padx=10, pady=10)

    # Create a function to update and display tasks based on selected date
    def update_tasks_for_date():
        selected_date = cal.get_date()
        matching_tasks = [(task["name"], task["due_datetime"].split()[1]) for task in tasks if task.get("due_datetime", "").startswith(selected_date)]
        if matching_tasks:
            tasks_info = '\n'.join(f'{task[0]} @ {task[1]}' for task in matching_tasks)
            messagebox.showinfo("Tasks for Selected Date", f"Tasks for {selected_date}:\n\n{tasks_info}")
        else:
            messagebox.showinfo("No Tasks", f"No tasks for {selected_date}.")

    # Bind the update function to the calendar's date click event
    cal.bind("<<CalendarSelected>>", lambda event: update_tasks_for_date())

    # Button to add task
    btn_add_task = tk.Button(main_frame, text="+", font=("Helvetica", 24), command=add_task, bg="red", fg="white")
    btn_add_task.place(relx=1, rely=1, anchor="se", x=-20, y=-20)  # Placing the button at the bottom right with some padding

    home_window.mainloop()

# For testing purposes
# show_home_screen("John", None)
