import json
import tkinter as tk
from tkinter import filedialog

def get_data():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select JSON/Wind file",
        filetypes=[("JSON/Wind files", "*.json *.wind"), ("All files", "*.*")]
    )

    if not file_path:  
        print("No file selected.")
        return None, None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading file: {e}")
        return None, None

    return data, file_path
