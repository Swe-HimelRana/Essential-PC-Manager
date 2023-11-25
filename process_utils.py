import tkinter as tk
from tkinter import messagebox
import psutil

def bytes_to_gb(bytes_size):
    return bytes_size / (1024.0 ** 3)

def get_top_processes_by_memory(exclude_system):
    try:
        processes = list(psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'cpu_percent']))
        if exclude_system:
            processes = [process for process in processes if process.info['name'] not in ('System', 'Idle')]
        return sorted(processes, key=lambda x: x.info['memory_info'].rss, reverse=True)[:20]
    except psutil.Error as e:
        messagebox.showerror("Error", f"Error getting memory processes: {str(e)}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while getting memory processes: {str(e)}")
        return []

def get_top_processes_by_cpu(exclude_system):
    try:
        processes = list(psutil.process_iter(attrs=['pid', 'name', 'memory_info', 'cpu_percent']))
        if exclude_system:
            processes = [process for process in processes if process.info['name'] not in ('System', 'Idle')]
        return sorted(processes, key=lambda x: x.info['cpu_percent'], reverse=True)[:20]
    except psutil.Error as e:
        messagebox.showerror("Error", f"Error getting CPU processes: {str(e)}")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while getting CPU processes: {str(e)}")
        return []

def kill_process(pid, exclude_system, update_display_func):
    try:
        process = psutil.Process(pid)
        process.terminate()
        update_display_func(exclude_system)
    except psutil.NoSuchProcess:
        messagebox.showinfo("Error", "Process not found.")
    except psutil.AccessDenied:
        messagebox.showerror("Error", "Access is denied. Try running the application with administrator privileges.")
    except psutil.Error as e:
        messagebox.showerror("Error", f"Error killing process: {str(e)}")
        
 
        
def update_display(tab, get_top_processes_func, exclude_system, resource_type="cpu/memory"):
    try:
        top_processes = get_top_processes_func(exclude_system)

        text_widget = tab.text_widget
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)

        for i, process in enumerate(top_processes, 1):
            pid = process.info['pid']
            name = process.info['name']
            memory_usage_bytes = process.info['memory_info'].rss
            memory_usage_mb = bytes_to_mb(memory_usage_bytes)  # Convert to MB
            cpu_usage = process.info['cpu_percent']

            text_widget.insert(tk.END, f"{i}. Process ID: {pid}, Name: {name}\n")
            text_widget.insert(tk.END, f"   Memory Usage: {memory_usage_mb:.2f} MB\n")
            text_widget.insert(tk.END, f"   CPU Usage: {cpu_usage:.2f}%\n")  # Display CPU usage in percentage

            kill_button = tk.Button(text_widget, text="Kill", command=lambda p=pid: kill_process(p, exclude_system, lambda x: update_display(tab, get_top_processes_func, x)))
           
            
            text_widget.window_create(tk.END, window=kill_button)
            text_widget.insert(tk.END, "\n" + "-" * 50 + "\n")

        text_widget.config(state=tk.DISABLED)
    except psutil.AccessDenied:
        messagebox.showerror("Error", "Access is denied. Try running the application with administrator privileges.")
    except psutil.Error as e:
        messagebox.showerror("Error", f"Error updating {resource_type} display: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while updating {resource_type} display: {str(e)}")

def bytes_to_mb(bytes_size):
    return bytes_size / (1024.0 ** 2)
