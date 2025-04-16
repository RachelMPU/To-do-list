import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class TodoAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Set theme colors
        self.primary_color = "#4a6ea9"
        self.secondary_color = "#f0f0f0"
        self.accent_color = "#ff6b6b"
        
       # Priority colors
        self.priority_colors = {
            "High": "#ff6b6b",
            "Medium": "#ffb347",
            "Low": "#77dd77"
        }
        
        # Tag colors
        self.tag_colors = {
            "Work": "#4a6ea9",
            "Personal": "#9370db",
            "Study": "#3cb371",
            "Urgent": "#dc3545"
        }
        
        # Set application style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.secondary_color)
        self.style.configure('TButton', 
                             background=self.primary_color, 
                             foreground='white', 
                             font=('Arial', 10, 'bold'),
                             padding=5)
        self.style.map('TButton', 
                       background=[('active', self.accent_color)])
        self.style.configure('Treeview', 
                             rowheight=25,
                             font=('Arial', 10))
        self.style.configure('Treeview.Heading', 
                             font=('Arial', 11, 'bold'))
        
        # Task data
        self.tasks = []
        self.filename = "todo_data.json"
        self.load_tasks()
        
        # Filter and sort variables
        self.filter_status = tk.StringVar(value="All")
        self.filter_tag = tk.StringVar(value="All")
        self.sort_by = tk.StringVar(value="Creation Time")
        
        # Create interface
        self.create_widgets()
        
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
                    
                    # Ensure all tasks have the new fields
                    for task in self.tasks:
                        if "priority" not in task:
                            task["priority"] = "Medium"
                        if "due_date" not in task:
                            task["due_date"] = ""
                        if "tags" not in task:
                            task["tags"] = []
                        if "completed_at" not in task:
                            task["completed_at"] = ""
            except:
                self.tasks = []
        else:
            self.tasks = []
            
    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)
            
    def create_widgets(self):
        # Top title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="To-Do List Manager", 
                               font=('Arial', 18, 'bold'),
                               foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Operation buttons area
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_btn = ttk.Button(button_frame, text="Add Task", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(button_frame, text="Edit Task", command=self.edit_task)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        complete_btn = ttk.Button(button_frame, text="Mark Complete", command=self.complete_task)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Filter and sort area
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        status_combo = ttk.Combobox(filter_frame, textvariable=self.filter_status, 
                                   values=["All", "Incomplete", "Completed", "Due Today"], 
                                   width=10, state="readonly")
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        
        # Tag filter
        ttk.Label(filter_frame, text="Tag:").pack(side=tk.LEFT, padx=5)
        tag_combo = ttk.Combobox(filter_frame, textvariable=self.filter_tag, 
                                values=["All", "Work", "Personal", "Study", "Urgent"], 
                                width=10, state="readonly")
        tag_combo.pack(side=tk.LEFT, padx=5)
        tag_combo.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        
        # Sort options
        ttk.Label(filter_frame, text="Sort:").pack(side=tk.LEFT, padx=5)
        sort_combo = ttk.Combobox(filter_frame, textvariable=self.sort_by, 
                                 values=["Creation Time", "Due Date", "Priority", "Task Name"], 
                                 width=10, state="readonly")
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind("<<ComboboxSelected>>", lambda e: self.update_task_list())
        
        # Search bar
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        self.search_var.trace("w", lambda name, index, mode: self.update_task_list())
        
        # Task list
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ('id', 'status', 'priority', 'title', 'tags', 'due_date', 'created_at')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.task_tree.heading('id', text='ID')
        self.task_tree.heading('status', text='Status')
        self.task_tree.heading('priority', text='Priority')
        self.task_tree.heading('title', text='Task')
        self.task_tree.heading('tags', text='Tags')
        self.task_tree.heading('due_date', text='Due Date')
        self.task_tree.heading('created_at', text='Creation Time')
        
        # Set column width
        self.task_tree.column('id', width=50, anchor='center')
        self.task_tree.column('status', width=70, anchor='center')
        self.task_tree.column('priority', width=70, anchor='center')
        self.task_tree.column('title', width=300)
        self.task_tree.column('tags', width=100, anchor='center')
        self.task_tree.column('due_date', width=100, anchor='center')
        self.task_tree.column('created_at', width=150, anchor='center')
        
        # Bind double click event
        self.task_tree.bind('<Double-1>', self.view_task)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscroll=scrollbar.set)
        
        # Place Treeview and scrollbar
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure color tags for priority and tags
        for priority, color in self.priority_colors.items():
            self.task_tree.tag_configure(f'priority_{priority}', background=color)
        
        # Set tag for completed tasks
        self.task_tree.tag_configure('completed', foreground='gray')
        
        # Set tag for tasks due today
        self.task_tree.tag_configure('due_today', foreground='red')
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Load initial tasks
        self.update_task_list()
        
    def update_task_list(self):
        # Clear current list
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # Search filter
        search_text = self.search_var.get().lower()
        filtered_tasks = self.tasks.copy()
        
        # Text search filter
        if search_text:
            filtered_tasks = [
                task for task in filtered_tasks 
                if search_text in task['title'].lower() or 
                   (task['description'] and search_text in task['description'].lower())
            ]
            
        # Status filter
        status_filter = self.filter_status.get()
        if status_filter == "Incomplete":
            filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
        elif status_filter == "Completed":
            filtered_tasks = [task for task in filtered_tasks if task["completed"]]
        elif status_filter == "Due Today":
            today = datetime.now().strftime("%Y-%m-%d")
            filtered_tasks = [
                task for task in filtered_tasks 
                if task["due_date"] == today and not task["completed"]
            ]
            
        # Tag filter
        tag_filter = self.filter_tag.get()
        if tag_filter != "All":
            filtered_tasks = [
                task for task in filtered_tasks 
                if tag_filter in task.get("tags", [])
            ]
            
        # Sort
        sort_option = self.sort_by.get()
        if sort_option == "Creation Time":
            filtered_tasks.sort(key=lambda x: x["created_at"], reverse=True)
        elif sort_option == "Due Date":
            # Put the empty date last
            filtered_tasks.sort(
                key=lambda x: (x["due_date"] == "", x["due_date"]), 
                reverse=False
            )
        elif sort_option == "Priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            filtered_tasks.sort(
                key=lambda x: priority_order.get(x.get("priority", "Medium"), 1)
            )
        elif sort_option == "Task Name":
            filtered_tasks.sort(key=lambda x: x["title"].lower())
        
        # Repopulate list
        today = datetime.now().strftime("%Y-%m-%d")
        for task in filtered_tasks:
            status = "✓" if task["completed"] else "✗"
            priority = task.get("priority", "Medium")
            tags = ", ".join(task.get("tags", []))
            due_date = task.get("due_date", "")
            
            values = (
                task['id'], 
                status, 
                priority,
                task['title'], 
                tags,
                due_date,
                task['created_at']
            )
            
            item = self.task_tree.insert('', tk.END, values=values)
            
            # Apply tags to the task
            if task["completed"]:
                self.task_tree.item(item, tags=('completed',))
            elif due_date == today:
                self.task_tree.item(item, tags=('due_today',))
            else:
                self.task_tree.item(item, tags=(f'priority_{priority}',))
                
        # Update status bar
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        self.status_label.config(text=f"Total {total} tasks, {completed} completed")
        
    def add_task(self):
        # Create add task window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Task")
        add_window.geometry("500x450")
        add_window.grab_set() 
        
        # Task form
        form_frame = ttk.Frame(add_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(form_frame, text="Title:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.grid(row=0, column=1, sticky=tk.W, pady=5, columnspan=2)
        
        # Description
        ttk.Label(form_frame, text="Description:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, height=5, width=40, wrap=tk.WORD)
        desc_text.grid(row=1, column=1, sticky=tk.W, pady=5, columnspan=2)
        
        # Priority
        ttk.Label(form_frame, text="Priority:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=15, state="readonly")
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Due Date
        ttk.Label(form_frame, text="Due Date:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        due_date = DateEntry(form_frame, width=15, background=self.primary_color, foreground='white', borderwidth=2)
        due_date.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Tag selection
        ttk.Label(form_frame, text="Tags:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.NW, pady=5)
        
        # Create a frame to place all the label checkboxes
        tags_frame = ttk.Frame(form_frame)
        tags_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Use a vertical layout to place the label checkboxes
        tag_vars = {}
        for i, tag in enumerate(["Work", "Personal", "Study", "Urgent"]):
            tag_vars[tag] = tk.BooleanVar(value=False)
            ttk.Checkbutton(tags_frame, text=tag, variable=tag_vars[tag]).grid(
                row=i, column=0, sticky=tk.W, pady=2
            )
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side=tk.LEFT, padx=10)
        
        # Save button
        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Please enter a task title!")
                return
                
            description = desc_text.get("1.0", tk.END).strip()
            priority = priority_var.get()
            due_date_str = due_date.get_date().strftime("%Y-%m-%d")
            
            # Get selected tags
            selected_tags = [tag for tag, var in tag_vars.items() if var.get()]
            
            # Create new task
            task = {
                "id": max([task["id"] for task in self.tasks], default=0) + 1,
                "title": title,
                "description": description,
                "priority": priority,
                "due_date": due_date_str,
                "tags": selected_tags,
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed_at": ""
            }
            
            # Add to task list
            self.tasks.append(task)
            self.save_tasks()
            self.update_task_list()
            
            messagebox.showinfo("Success", f"Task '{title}' added!")
            add_window.destroy()
            
        ttk.Button(button_frame, text="Save", command=save_task).pack(side=tk.LEFT, padx=10)
        
    def edit_task(self):
        # Get selected task
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task first!")
            return
            
        item_id = self.task_tree.item(selected_item[0], 'values')[0]
        task_id = int(item_id)
        
        # Find corresponding task
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
            
        # Create edit task window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("500x450") 
        edit_window.grab_set() 
        
        # Task form
        form_frame = ttk.Frame(edit_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(form_frame, text="Title:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.insert(0, task["title"])
        title_entry.grid(row=0, column=1, sticky=tk.W, pady=5, columnspan=2)
        
        # Description
        ttk.Label(form_frame, text="Description:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(form_frame, height=5, width=40, wrap=tk.WORD)
        desc_text.insert(tk.END, task.get("description", ""))
        desc_text.grid(row=1, column=1, sticky=tk.W, pady=5, columnspan=2)
        
        # Priority
        ttk.Label(form_frame, text="Priority:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value=task.get("priority", "Medium"))
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=15, state="readonly")
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Due Date
        ttk.Label(form_frame, text="Due Date:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        due_date = DateEntry(form_frame, width=15, background=self.primary_color, foreground='white', borderwidth=2)
        if task.get("due_date"):
            due_date.set_date(datetime.strptime(task["due_date"], "%Y-%m-%d").date())
        due_date.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Tag selection 
        ttk.Label(form_frame, text="Tags:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.NW, pady=5)
        
        
        tags_frame = ttk.Frame(form_frame)
        tags_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        
        tag_vars = {}
        current_tags = task.get("tags", [])
        for i, tag in enumerate(["Work", "Personal", "Study", "Urgent"]):
            tag_vars[tag] = tk.BooleanVar(value=tag in current_tags)
            ttk.Checkbutton(tags_frame, text=tag, variable=tag_vars[tag]).grid(
                row=i, column=0, sticky=tk.W, pady=2
            )
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Cancel button
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=10)
        
        # Save button
        def save_edited_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showwarning("Warning", "Please enter a task title!")
                return
                
            description = desc_text.get("1.0", tk.END).strip()
            priority = priority_var.get()
            due_date_str = due_date.get_date().strftime("%Y-%m-%d")
            
            # Get selected tags
            selected_tags = [tag for tag, var in tag_vars.items() if var.get()]
            
            # Update task
            task["title"] = title
            task["description"] = description
            task["priority"] = priority
            task["due_date"] = due_date_str
            task["tags"] = selected_tags
            
            self.save_tasks()
            self.update_task_list()
            
            messagebox.showinfo("Success", f"Task '{title}' updated!")
            edit_window.destroy()
            
        ttk.Button(button_frame, text="Save", command=save_edited_task).pack(side=tk.LEFT, padx=10)
        
    def view_task(self, event):
        # Get selected task
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
            
        item_id = self.task_tree.item(selected_item[0], 'values')[0]
        task_id = int(item_id)
        
        # Find corresponding task
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
            
        # Create view task window
        view_window = tk.Toplevel(self.root)
        view_window.title("Task Details")
        view_window.geometry("500x400")
        view_window.resizable(False, False)
        
        # Task Details
        ttk.Label(view_window, text="Task Details", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Tag color indicators
        if task.get("tags"):
            tag_frame = ttk.Frame(view_window)
            tag_frame.pack(fill=tk.X, padx=20)
            
            for tag in task.get("tags", []):
                tag_label = ttk.Label(tag_frame, text=tag, background=self.tag_colors.get(tag, "#cccccc"),
                                     foreground="white", padding=(5, 2))
                tag_label.pack(side=tk.LEFT, padx=5)
        
        details_frame = ttk.Frame(view_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Task ID
        ttk.Label(details_frame, text="ID:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=str(task["id"])).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Task title
        ttk.Label(details_frame, text="Title:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=task["title"]).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Task Description
        ttk.Label(details_frame, text="Description:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(details_frame, height=5, width=40, wrap=tk.WORD)
        desc_text.insert(tk.END, task.get("description", "") or "(No Description)")
        desc_text.config(state=tk.DISABLED)
        desc_text.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Priority
        ttk.Label(details_frame, text="Priority:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        priority_label = ttk.Label(details_frame, text=task.get("priority", "Medium"), 
                                  background=self.priority_colors.get(task.get("priority", "Medium"), "#cccccc"),
                                  foreground="white", padding=(5, 2))
        priority_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Due Date
        ttk.Label(details_frame, text="Due Date:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=task.get("due_date", "None") or "None").grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Status
        status_text = "Completed" if task["completed"] else "Incomplete"
        ttk.Label(details_frame, text="Status:", font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=status_text).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Creation Time
        ttk.Label(details_frame, text="Creation Time:", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(details_frame, text=task["created_at"]).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Completion Time
        if task["completed"] and task.get("completed_at"):
            ttk.Label(details_frame, text="Completion Time:", font=('Arial', 10, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=task["completed_at"]).grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Button Area
        button_frame = ttk.Frame(view_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Edit", command=lambda: [view_window.destroy(), self.edit_task()]).pack(side=tk.LEFT, padx=5)
        
        if not task["completed"]:
            ttk.Button(button_frame, text="Mark Complete", 
                      command=lambda: [view_window.destroy(), self.complete_task()]).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Close", command=view_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def complete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task first!")
            return
            
        item_id = self.task_tree.item(selected_item[0], 'values')[0]
        task_id = int(item_id)
        
        # Find and mark the task
        for task in self.tasks:
            if task["id"] == task_id:
                if task["completed"]:
                    messagebox.showinfo("Info", "This task is already completed!")
                    return
                    
                task["completed"] = True
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_tasks()
                self.update_task_list()
                messagebox.showinfo("Success", f"Task '{task['title']}' marked as completed!")
                return
                
        messagebox.showerror("Error", f"Task with ID {task_id} not found!")
        
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task first!")
            return
            
        item_id = self.task_tree.item(selected_item[0], 'values')[0]
        task_id = int(item_id)
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
        if not confirm:
            return
            
        # Find and delete the task
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                deleted = self.tasks.pop(i)
                self.save_tasks()
                self.update_task_list()
                messagebox.showinfo("Success", f"Task '{deleted['title']}' deleted!")
                return
                
        messagebox.showerror("Error", f"Task with ID {task_id} not found!")
        
    def export_tasks(self):
        """Export tasks to a text file"""
        from tkinter import filedialog
        
        # Get save path
        filename = filedialog.asksaveasfilename(
            initialdir="./",
            title="Export Tasks",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        
        if not filename:
            return
            
        # Ensure the file has a .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
            
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("===== To-Do List =====\n\n")
                
                # Incomplete tasks
                file.write("--- Incomplete Tasks ---\n")
                for task in self.tasks:
                    if not task["completed"]:
                        file.write(f"[{task['id']}] {task['title']}\n")
                        file.write(f"  Priority: {task.get('priority', 'Medium')}\n")
                        
                        if task.get("due_date"):
                            file.write(f"  Due Date: {task['due_date']}\n")
                            
                        if task.get("tags"):
                            file.write(f"  Tags: {', '.join(task['tags'])}\n")
                            
                        if task.get("description"):
                            file.write(f"  Description: {task['description']}\n")
                            
                        file.write("\n")
                
                # Completed tasks
                file.write("\n--- Completed Tasks ---\n")
                for task in self.tasks:
                    if task["completed"]:
                        file.write(f"[{task['id']}] {task['title']} (Completed at: {task.get('completed_at', 'Unknown')})\n")
                
            messagebox.showinfo("Success", f"Tasks exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def add_menu(self):
        """Add menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Tasks", command=self.export_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Add Task", command=self.add_task)
        edit_menu.add_command(label="Edit Task", command=self.edit_task)
        edit_menu.add_command(label="Delete Task", command=self.delete_task)
        edit_menu.add_command(label="Mark Complete", command=self.complete_task)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="All Tasks", command=lambda: [self.filter_status.set("All"), self.update_task_list()])
        view_menu.add_command(label="Incomplete Tasks", command=lambda: [self.filter_status.set("Incomplete"), self.update_task_list()])
        view_menu.add_command(label="Completed Tasks", command=lambda: [self.filter_status.set("Completed"), self.update_task_list()])
        view_menu.add_command(label="Due Today", command=lambda: [self.filter_status.set("Due Today"), self.update_task_list()])
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")
        about_window.resizable(False, False)
        
        ttk.Label(about_window, 
                 text="To-Do List Manager",
                 font=('Arial', 14, 'bold'),
                 foreground=self.primary_color).pack(pady=10)
                 
        ttk.Label(about_window, 
                 text="A simple and powerful to-do list management tool",
                 wraplength=250).pack(pady=5)
                 
        ttk.Label(about_window, 
                 text="Version: 1.0.0").pack(pady=5)
                 
        ttk.Button(about_window, 
                  text="OK", 
                  command=about_window.destroy).pack(pady=20)
                  
    def show_task_statistics(self):
        """Show task statistics"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Task Statistics")
        stats_window.geometry("400x300")
        
        # Calculate statistics
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        
        # Statistics by priority
        priority_stats = {
            "High": sum(1 for task in self.tasks if task.get("priority") == "High"),
            "Medium": sum(1 for task in self.tasks if task.get("priority") == "Medium"),
            "Low": sum(1 for task in self.tasks if task.get("priority") == "Low"),
        }
        
        # Statistics by tag
        tag_stats = {}
        for task in self.tasks:
            for tag in task.get("tags", []):
                if tag in tag_stats:
                    tag_stats[tag] += 1
                else:
                    tag_stats[tag] = 1
        
        # Display statistics
        ttk.Label(stats_window, text="Task Statistics", font=('Arial', 14, 'bold')).pack(pady=10)
        
        stats_frame = ttk.Frame(stats_window)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Basic statistics
        ttk.Label(stats_frame, text="Total Tasks:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=str(total)).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(stats_frame, text="Completed:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=f"{completed} ({completed/total*100:.1f}% )" if total else "0 (0%)").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(stats_frame, text="Uncompleted:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(stats_frame, text=f"{pending} ({pending/total*100:.1f}% )" if total else "0 (0%)").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Statistics by priority
        ttk.Label(stats_frame, text="By Priority:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=10)
        
        row = 4
        for priority, count in priority_stats.items():
            ttk.Label(stats_frame, text=f"{priority}:").grid(row=row, column=0, sticky=tk.W, padx=(20, 0), pady=2)
            ttk.Label(stats_frame, text=str(count)).grid(row=row, column=1, sticky=tk.W, pady=2)
            row += 1
        
        # Statistics by tag
        ttk.Label(stats_frame, text="By Tag:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=10)
        row += 1
        
        if not tag_stats:
            ttk.Label(stats_frame, text="No tags used").grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=(20, 0), pady=2)
        else:
            for tag, count in tag_stats.items():
                ttk.Label(stats_frame, text=f"{tag}:").grid(row=row, column=0, sticky=tk.W, padx=(20, 0), pady=2)
                ttk.Label(stats_frame, text=str(count)).grid(row=row, column=1, sticky=tk.W, pady=2)
                row += 1
        
        # Close button
        ttk.Button(stats_window, text="Close", command=stats_window.destroy).pack(pady=10)

def main():
    root = tk.Tk()
    app = TodoAppGUI(root)
    
    # Add menu bar
    app.add_menu()
    
    # Add statistics button
    stats_btn = ttk.Button(root, text="Task Statistics", command=app.show_task_statistics)
    stats_btn.pack(side=tk.BOTTOM, padx=10, pady=5, anchor=tk.SE)
    
    root.mainloop()

if __name__ == "__main__":
    main()
