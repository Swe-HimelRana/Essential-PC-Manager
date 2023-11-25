import ctypes

class MEMORYSTATUS(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("dwTotalPhys", ctypes.c_size_t),
                ("dwAvailPhys", ctypes.c_size_t),
                ("dwTotalPageFile", ctypes.c_size_t),
                ("dwAvailPageFile", ctypes.c_size_t),
                ("dwTotalVirtual", ctypes.c_size_t),
                ("dwAvailVirtual", ctypes.c_size_t),
                ]

def get_memory_speed():
    memory_status = MEMORYSTATUS()
    ctypes.windll.kernel32.GlobalMemoryStatus(ctypes.byref(memory_status))
    return memory_status.dwMemoryLoad, memory_status.dwTotalPhys

memory_load, total_physical_memory = get_memory_speed()
print(f"Memory Load: {memory_load}%")
print(f"Total Physical Memory: {total_physical_memory / (1024 ** 3):.2f} GB")
