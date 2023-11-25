import tkinter as tk
from tkinter import ttk

class AboutTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
    

        self.info_text = """
        Essential PC-Manager\n
        Version: 1.0.0\n
        Created by Himel\n
        contact@himelrana.com\n
        https://himelrana.com\n
        
        """

        self.text_widget = tk.Text(self.frame, width=40, state=tk.DISABLED, font=('Arial', 10))
        self.text_widget.pack(pady=5, padx=1)  # Add padx to give some space on the sides
        self.text_widget.config(state=tk.NORMAL)  # Set the state to NORMAL before inserting content
        self.text_widget.insert(tk.END, self.info_text)
        self.text_widget.config(state=tk.DISABLED)  # Set the state back to DISABLED

    def get_frame(self):
        return self.frame
