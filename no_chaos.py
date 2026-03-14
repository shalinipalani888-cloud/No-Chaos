import tkinter as tk
from tkinter import filedialog
import os
import shutil
import hashlib

selected_folder = ""

# Select folder
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    status_label.config(text=f"Selected: {selected_folder}")

# Organize files into folders
def organize_files():
    if not selected_folder:
        status_label.config(text="Please select a folder first")
        return

    file_types = {
        "Images": [".jpg", ".png", ".jpeg", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Music": [".mp3", ".wav"],
        "Videos": [".mp4", ".mkv", ".mov"],
        "Programs": [".exe", ".msi"],
        "Archives": [".zip", ".rar"],
        "Code": [".py", ".html", ".css", ".js"]
    }

    moved_files = 0

    for file in os.listdir(selected_folder):
        file_path = os.path.join(selected_folder, file)

        if os.path.isfile(file_path):
            for folder, extensions in file_types.items():
                if file.lower().endswith(tuple(extensions)):
                    new_folder = os.path.join(selected_folder, folder)

                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)

                    shutil.move(file_path, os.path.join(new_folder, file))
                    moved_files += 1
                    break

    status_label.config(text=f"Organized {moved_files} files")

# Create hash for duplicate detection
def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buffer = f.read()
        hasher.update(buffer)
    return hasher.hexdigest()

# Remove duplicate files
def remove_duplicates():
    if not selected_folder:
        status_label.config(text="Please select a folder first")
        return

    hashes = {}
    removed = 0

    for file in os.listdir(selected_folder):
        file_path = os.path.join(selected_folder, file)

        if os.path.isfile(file_path):
            filehash = file_hash(file_path)

            if filehash in hashes:
                os.remove(file_path)
                removed += 1
            else:
                hashes[filehash] = file_path

    status_label.config(text=f"Removed {removed} duplicate files")

# Create window
window = tk.Tk()
window.title("No Chaos")
window.geometry("400x300")

title = tk.Label(window, text="No Chaos - File Organizer", font=("Arial", 14))
title.pack(pady=10)

browse_button = tk.Button(window, text="Select Folder", command=select_folder)
browse_button.pack(pady=10)

organize_button = tk.Button(window, text="Organize Files", command=organize_files)
organize_button.pack(pady=10)

duplicate_button = tk.Button(window, text="Remove Duplicates", command=remove_duplicates)
duplicate_button.pack(pady=10)

status_label = tk.Label(window, text="Status: Waiting")
status_label.pack(pady=20)

window.mainloop()


