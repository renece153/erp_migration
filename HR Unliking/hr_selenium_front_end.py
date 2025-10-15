import tkinter as tk
import subprocess
import os
from pathlib import Path
import log_info as sl

def execute_script_function():
    home_dir = str(Path.home())
    script_path = "hr_selenium_automation.py"  # Change to your script's filename
    python_driver = os.path.join(home_dir, 'PycharmProjects', 'ERP_Migration', '.venv', 'Scripts', 'python.exe')
    param = selected_option.get()  # Get dropdown value
    try:
        subprocess.run([python_driver, script_path, param], capture_output=True, text=True)
    except Exception as e:
        sl.error(f"Failed to execute {script_path}\nError: {e}")

# Create the main window
root = tk.Tk()
root.title("HR Unlinking Tool - Version 1")
root.geometry("200x100")

# Dropdown Menu
options = ["Vanilla w/ Refresh", "Migration w/ Refresh", "Vanilla, No Refresh", "Migration, No Refresh"]
selected_option = tk.StringVar(value="Migration, No Refresh")
selected_option.set(options[0])  # Default selection
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack()


run_script_function_button = tk.Button(root, text="Execute Selenium", command=execute_script_function)
run_script_function_button.pack()

# Run the application
root.mainloop()
