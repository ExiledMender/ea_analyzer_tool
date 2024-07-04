import os
import shutil
import tkinter as tk
from tkinter import filedialog

def collect_files(folder_path):
    collected_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file in ["Info.txt", "machine_info.json", "TestConnections.txt"]:
                file_path = os.path.join(root, file)
                collected_files.append(file_path)
    
    return collected_files

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path

def main():
    selected_folder = select_folder()
    if not selected_folder:
        print("No folder selected.")
        return
    
    files_to_collect = collect_files(selected_folder)

    logs_dir = os.path.join(os.getcwd(), "temp")
    
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    if files_to_collect:
        for file_path in files_to_collect:
            dest_path = os.path.join(logs_dir, os.path.basename(file_path))
            shutil.copy(file_path, dest_path)
            print(f"Copied {file_path} to {dest_path}")
    
    else:
        print("No files found to collect.")

if __name__ == "__main__":
    main()