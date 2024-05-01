import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar

# Global list to store tasks
tasks = []

def add_task():
    # Create a new window for adding tasks
    add_task_window = tk.Toplevel()
    add_task_window.title("Add New Task")

    # Label and entry for task name
    lbl_task_name = tk.Label(add_task_window, text="Task Name:")
    lbl_task_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_task_name = tk.Entry(add_task_window)
    entry_task_name.grid(row=0, column=1, padx=10, pady=5)

    # Calendar for selecting due date
    lbl_due_date = tk.Label(add_task_window, text="Due Date:")
    lbl_due_date.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    cal_due_date = Calendar(add_task_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal_due_date.grid(row=1, column=1, padx=10, pady=5)

    # Function to save the task with name and due date
    def save_task():
        task_name = entry_task_name.get()
        due_date = cal_due_date.get_date()
        # Save the task to the global list
        tasks.append({"name": task_name, "due_date": due_date})
        messagebox.showinfo("Success", "Task added successfully!")
        add_task_window.destroy()

    # Button to save the task
    btn_save = tk.Button(add_task_window, text="Save Task", command=save_task)
    btn_save.grid(row=2, column=0, columnspan=2, pady=10)

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
        tree.insert("", "end", values=(task["name"], task["due_date"]))

    # Add scrollbar to the treeview
    scrollbar = ttk.Scrollbar(view_tasks_window, orient="vertical", command=tree.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

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

    # Create a label to display the welcome message
    welcome_label = tk.Label(home_window, text=f"Welcome, {username}!")
    welcome_label.pack(pady=20)

    # Add a button to open the add task window
    btn_open_add_task = tk.Button(home_window, text="Add Task", command=add_task)
    btn_open_add_task.pack()

    # Add a button to view tasks
    btn_view_tasks = tk.Button(home_window, text="View Tasks", command=view_tasks)
    btn_view_tasks.pack()

    # Create a logout button
    btn_logout = tk.Button(home_window, text="Logout", command=lambda: logout(home_window, login_window))
    btn_logout.pack(side=tk.BOTTOM, pady=10)

    home_window.mainloop()

    # Sample usage:
    # Replace "User123" with the actual username when integrating with your authentication system
    # Assume login_window is your login screen Tk window
    show_home_screen("User123", login_window)
