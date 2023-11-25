import tkinter as tk
from tkinter import ttk
from memory_tab import MemoryTab
from cpu_tab import CpuTab
from pc_info_tab import PcInfoTab
from about_tab import AboutTab
 
class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Essential PC Manager")

        self.notebook = ttk.Notebook(root)

        # Create tabs
        pc_info_tab = PcInfoTab(self.notebook)
        about_tab = AboutTab(self.notebook)  # Add the AboutTab
        memory_tab = MemoryTab(self.notebook)
        cpu_tab = CpuTab(self.notebook)
        
        # Add tabs to the notebook
        self.notebook.add(memory_tab.frame, text="Ram Using")
        self.notebook.add(cpu_tab.frame, text="CPU Using")
       
        self.notebook.add(pc_info_tab.frame, text="PC Info")
        self.notebook.add(about_tab.frame, text="About")  # Add the AboutTab

        self.notebook.pack(expand=1, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()