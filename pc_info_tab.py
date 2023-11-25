import tkinter as tk
from tkinter import ttk
import psutil
import cpuinfo
from tkinter import messagebox
from process_utils import bytes_to_gb
import wmi

class PcInfoTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        self.text_widget = tk.Text(self.frame, height=25, width=50, state=tk.DISABLED, font=('Arial', 10))
        self.text_widget.pack(pady=10, padx=10)

        self.refresh_button = tk.Button(self.frame, text="Refresh", command=self.update_pc_info_display, font=('Arial', 12))
        self.refresh_button.pack(pady=5)

        self.update_pc_info_display()

    def get_total_ram(self):
        try:
            return psutil.virtual_memory().total
        except psutil.Error as e:
            messagebox.showerror("Error", f"Error getting total RAM: {str(e)}")
            return 0

    def get_gpu_details(self):
        try:
            gpu_info = {}
            gpus = psutil.virtual_memory()
            gpu_info['total'] = gpus.total
            return gpu_info
        except psutil.Error as e:
            messagebox.showerror("Error", f"Error getting GPU details: {str(e)}")
            return {}

    def get_cpu_details(self):
        try:
            return cpuinfo.get_cpu_info()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting CPU details: {str(e)}")
            return {}
        
    def get_memory_slot_number(self):
        c = wmi.WMI()
        total_slot = 0
        for mem in c.Win32_PhysicalMemory():
            total_slot = total_slot + 1
        return total_slot
    
    def get_memory_slot_info(self, text_widget):
        c = wmi.WMI()

        # Get information about the first physical memory module
        memory_slot_capacity_info_list = []
        
        for mem in c.Win32_PhysicalMemory():
            memory_slot_capacity_info_list.append(mem.Capacity)
        
        for i in range(len(memory_slot_capacity_info_list)):
            capacity = float(memory_slot_capacity_info_list[i]) / (1024 ** 3)
            text_widget.insert(tk.END, f"   Slot {i+1}: Capacity {capacity} GB\n")
            print(f"Slot {i+1} Capacity: {capacity}  GB")
        
    def get_memory_clock_speed(self):
        c = wmi.WMI()
        memory = next(iter(c.Win32_PhysicalMemory()), None)
        
        if memory:
            return memory.Speed
        else:
            return None
    
    def get_memory_info(self):
        try:
            memory_info = psutil.virtual_memory()
            return {
                'total': memory_info.total,
                'available': memory_info.available,
                'used': memory_info.used,
                'percent': memory_info.percent,
                  # Use getattr to handle absence of 'maxclock' attribute
            }
        except psutil.Error as e:
            messagebox.showerror("Error", f"Error getting memory details: {str(e)}")
            return {}

    def update_pc_info_display(self):
        try:
            total_ram = self.get_total_ram()
            gpu_details = self.get_gpu_details()
            cpu_details = self.get_cpu_details()
            memory_info = self.get_memory_info()
            clock_speed = self.get_memory_clock_speed()
            memory_slot_number = self.get_memory_slot_number()

            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)

            #self.text_widget.insert(tk.END, f"Total RAM: {bytes_to_gb(total_ram):.2f} GB\n\n")
            self.text_widget.insert(tk.END, f"Memory/RAM Details:\n")
            self.text_widget.insert(tk.END, f"\n")
            self.text_widget.insert(tk.END, f"   Total Memory: {bytes_to_gb(memory_info['total']):.2f} GB\n")
            self.text_widget.insert(tk.END, f"   Available Memory: {bytes_to_gb(memory_info['available']):.2f} GB\n")
            self.text_widget.insert(tk.END, f"   Used Memory: {bytes_to_gb(memory_info['used']):.2f} GB\n")
            self.text_widget.insert(tk.END, f"   Memory Usage: {memory_info['percent']}%\n")
            self.text_widget.insert(tk.END, f"   Memory Slots: {memory_slot_number}\n")
            self.text_widget.insert(tk.END, f"   Clock Speed: {clock_speed} MHz\n")
            self.get_memory_slot_info(self.text_widget)
            self.text_widget.insert(tk.END, f"\n")
            
            self.text_widget.insert(tk.END, f"CPU Details:\n")
            self.text_widget.insert(tk.END, f"\n")
            self.text_widget.insert(tk.END, f"   Processor: {cpu_details['brand_raw']}\n")
            self.text_widget.insert(tk.END, f"   Architecture: {cpu_details['arch']}\n")
            self.text_widget.insert(tk.END, f"   Cores: {psutil.cpu_count(logical=False)}\n")
            self.text_widget.insert(tk.END, f"   Threads: {psutil.cpu_count(logical=True)}\n")
            
            self.text_widget.insert(tk.END, f"\n")
            self.text_widget.insert(tk.END, f"GPU Details:\n")
            self.text_widget.insert(tk.END, f"   Total GPU Memory: {bytes_to_gb(gpu_details['total']):.2f} GB\n\n")

            

        

            self.text_widget.config(state=tk.DISABLED)
        except psutil.Error as e:
            messagebox.showerror("Error", f"Error updating PC Info display: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while updating PC Info display: {str(e)}")
