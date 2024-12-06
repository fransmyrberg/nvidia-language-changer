import tkinter as tk
from tkinter import messagebox
import winreg
import logging
import os

# Configure logging
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def add_or_update_dword():
    key_path = r"SOFTWARE\NVIDIA Corporation\NVControlPanel2\Client"
    dword_name = "UserDefinedLocale"
    dword_value = 0x409  # Hexadecimal for English (United States)

    try:
        # Attempt to open the registry key with all access rights
        logging.info(f"Attempting to open registry key: {key_path}")
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)

        try:
            # Check if the value already exists
            existing_value, value_type = winreg.QueryValueEx(reg_key, dword_name)
            logging.info(f"Found existing value for '{dword_name}': {existing_value}")
            
            if existing_value == dword_value:
                logging.info(f"No action needed: '{dword_name}' already exists with value '0x{existing_value:X}'.")
                messagebox.showinfo("No Action Needed", f"'{dword_name}' already exists with the value '0x{existing_value:X}'.")
            else:
                # Update the value if it exists but is different
                winreg.SetValueEx(reg_key, dword_name, 0, winreg.REG_DWORD, dword_value)
                logging.info(f"Updated '{dword_name}' to '0x{dword_value:X}'.")
                messagebox.showinfo("Updated", f"'{dword_name}' updated to '0x{dword_value:X}'.")
        except FileNotFoundError:
            # Add the value if it does not exist
            winreg.SetValueEx(reg_key, dword_name, 0, winreg.REG_DWORD, dword_value)
            logging.info(f"Added '{dword_name}' with value '0x{dword_value:X}'.")
            messagebox.showinfo("Success", f"'{dword_name}' added with value '0x{dword_value:X}'.")
        
        # Close the registry key
        winreg.CloseKey(reg_key)
        
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        messagebox.showerror("Permission Error", "This application requires administrator privileges to modify the registry. Please ensure you're running as Administrator.")
    except FileNotFoundError as e:
        logging.error(f"Registry key not found: {e}")
        messagebox.showerror("Registry Key Not Found", f"Could not find the registry key: {key_path}")
    except Exception as e:
        logging.error(f"Failed to modify registry: {e}")
        messagebox.showerror("Error", f"Failed to modify registry: {e}")

# GUI Setup
root = tk.Tk()
root.title("NVIDIA Language Changer")

# Instruction Label
tk.Label(
    root,
    text="Changes language of nvidia control panel to english (The tool adds or updates the DWORD 'UserDefinedLocale' with value '0x409' in the registry.)",
    wraplength=350,
).pack(pady=10)

# Add Button
add_button = tk.Button(root, text="Apply Changes", command=add_or_update_dword)
add_button.pack(pady=10)

# Run the GUI
root.mainloop()
