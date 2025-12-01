# gui_main_with_calculator.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import math
import sys
import helper
import winder
import planner

# ---------------- Stdout redirector ----------------
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, s):
        if s.strip():  # ignore empty strings
            self.text_widget.insert(tk.END, s + "\n")
            self.text_widget.see(tk.END)
    def flush(self):
        pass

# ---------------- Main GUI Class ----------------
class WinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Swamp Launch Filament Winder Gcode Generator")
        self.schedule = []
        self.defaultFeedRate = 0.005
        self.gcode = []
        self.machine = None

        # Feed Rate Entry (at the top of gui window)
        tk.Label(root, text="Feed Rate:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.feed_rate_var = tk.StringVar(value=str(self.defaultFeedRate))
        tk.Entry(root, textvariable=self.feed_rate_var, width=10).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Button Setup (Editable for later)
        tk.Button(root, text="Load Schedule JSON", command=self.load_schedule).grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        tk.Button(root, text="Generate G-code", command=self.generate_gcode).grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(root, text="Save G-code", command=self.save_gcode).grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        tk.Button(root, text="Calculator", command=self.open_calculator).grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        tk.Button(root, text="Quit", command=self.quit_program).grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=2)

        # Output Text
        tk.Label(root, text="Output / Debug Log:").grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.log_text.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Grid Setup ()
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(5, weight=1) 

    # Logging 
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    # Old Commands 
    def load_schedule(self):
        try:
            old_stdout = sys.stdout
            sys.stdout = StdoutRedirector(self.log_text)
            self.schedule, self.defaultFeedRate = helper.loadWindFile()
            self.feed_rate_var.set(str(self.defaultFeedRate))
            self.log(f"Schedule loaded. Layers: {len(self.schedule)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            sys.stdout = old_stdout

    def generate_gcode(self):
        try:
            self.defaultFeedRate = float(self.feed_rate_var.get())
            self.machine = winder.Winder(self.defaultFeedRate)
            self.machine.setFeedRate(self.defaultFeedRate, force=True)
            self.gcode = planner.planWind(self.schedule, self.machine)
            self.log(f"G-code generated. Lines: {len(self.gcode)}")
            for i, layer in enumerate(self.schedule):
                self.log(f"\tLayer {i}: type {layer.getType()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_gcode(self):
        if not self.gcode:
            messagebox.showwarning("Warning", "No G-code generated yet!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".nc", filetypes=[("G-code files", "*.nc")])
        if file_path:
            with open(file_path, 'w') as f:
                for line in self.gcode:
                    f.write(line + "\n")
            self.log(f"G-code saved to {file_path}")


    def quit_program(self):
        if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit? Any unsaved data will be lost."):
            self.root.destroy()
            sys.exit(print("Program has closed!"))

    # ---------------- Calculator GUI ----------------
    def open_calculator(self):
        calc_win = tk.Toplevel(self.root)
        calc_win.title("Wind Parameter Calculator")

        tk.Label(calc_win, text="Mandrel diameter:").grid(row=0, column=0, sticky="w")
        mandrel_var = tk.StringVar()
        tk.Entry(calc_win, textvariable=mandrel_var).grid(row=0, column=1, sticky="ew")

        tk.Label(calc_win, text="Tow width:").grid(row=1, column=0, sticky="w")
        tow_var = tk.StringVar()
        tk.Entry(calc_win, textvariable=tow_var).grid(row=1, column=1, sticky="ew")

        tk.Label(calc_win, text="Wind angle [deg]:").grid(row=2, column=0, sticky="w")
        angle_var = tk.StringVar()
        tk.Entry(calc_win, textvariable=angle_var).grid(row=2, column=1, sticky="ew")

        output_text = scrolledtext.ScrolledText(calc_win, width=40, height=10)
        output_text.grid(row=4, column=0, columnspan=2, pady=5, sticky="nsew")

        # Make calculator window scalable
        calc_win.columnconfigure(0, weight=1)
        calc_win.columnconfigure(1, weight=1)
        calc_win.rowconfigure(4, weight=1)

        def compute():
            try:
                old_stdout = sys.stdout
                sys.stdout = StdoutRedirector(output_text)
                mandrel = float(mandrel_var.get())
                tow = float(tow_var.get())
                angle = float(angle_var.get())

                mandrelCircumference = math.pi * mandrel
                effectiveTowWidth = tow / math.cos(math.radians(angle))
                numCircuits = math.ceil(mandrelCircumference / effectiveTowWidth)

                print(f"Number of circuits: {numCircuits}")
                print("Valid start position quantities:")
                for i in range(1, numCircuits + 1):
                    if numCircuits % i == 0:
                        print(f"  {i}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                sys.stdout = sys.__stdout__

        tk.Button(calc_win, text="Compute", command=compute).grid(row=3, column=0, columnspan=2, sticky="ew", pady=2)

# ---------------- Run GUI ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = WinderGUI(root)
    root.mainloop()
