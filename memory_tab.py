import tkinter as tk
from tkinter import ttk
import psutil
from tkinter import messagebox
from process_utils import get_top_processes_by_memory, kill_process, update_display

class MemoryTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        self.text_widget = tk.Text(self.frame, height=23, width=50, state=tk.DISABLED, font=('Arial', 10))
        self.text_widget.pack(pady=10, padx=10)

        self.exclude_system_var = tk.BooleanVar()
        self.exclude_system_var.set(False)
        self.exclude_system_checkbox = tk.Checkbutton(self.frame, text="Exclude System Processes", variable=self.exclude_system_var, command=self.update_memory_display)
        self.exclude_system_checkbox.pack(pady=5)

        self.refresh_button = tk.Button(self.frame, text="Refresh", command=self.update_memory_display, font=('Arial', 12))
        self.refresh_button.pack(pady=5)

        self.update_memory_display()

    def update_memory_display(self):
        update_display(self, get_top_processes_by_memory, self.exclude_system_var.get(), "Memory")
