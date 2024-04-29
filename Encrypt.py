import os
import tkinter as tk
from tkinter import filedialog, messagebox, font
from cryptography.fernet import Fernet
import csv

KEY_FILE = 'encryption_key.key'

def save_key(key):
    """Save the encryption key to a file."""
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_or_create_key():
    """Load the encryption key from a file, or create it if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        save_key(key)
        messagebox.showinfo("Key Generated", "A new encryption key has been generated and saved.")
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    entry_key.delete(0, tk.END)
    entry_key.insert(0, key.decode())
    return key

def regenerate_key():
    """Regenerate and save a new encryption key."""
    if messagebox.askokcancel("Regenerate Key", "Are you sure you want to regenerate the encryption key? This cannot be undone."):
        key = Fernet.generate_key()
        save_key(key)
        load_or_create_key()
        messagebox.showinfo("Key Regenerated", "A new encryption key has been generated and saved.")

def show_key():
    """Show the current encryption key in a secure manner."""
    key = entry_key.get()
    messagebox.showinfo("Current Key", f"Current Key: {key}")

def encrypt_csv():
    """Encrypt a CSV file using Fernet encryption."""
    input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv")
        if output_file:
            key = load_or_create_key()
            cipher_suite = Fernet(key)
            with open(input_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                encrypted_data = [cipher_suite.encrypt(','.join(row).encode()) for row in reader]

            with open(output_file, 'wb') as encrypted_file:
                for data in encrypted_data:
                    encrypted_file.write(data + b'\n')

def decrypt_csv():
    """Decrypt a previously encrypted CSV file."""
    input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv")
        if output_file:
            key = load_or_create_key()
            cipher_suite = Fernet(key)
            try:
                with open(input_file, 'rb') as encrypted_file:
                    decrypted_data = [cipher_suite.decrypt(line).decode().split(',') for line in encrypted_file]

                with open(output_file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(decrypted_data)
            except Exception as e:
                label_status.config(text=f"Decryption failed: {str(e)}")
            else:
                label_status.config(text="Decryption successful!")

# Create the main window
root = tk.Tk()
root.title("CSV File Encryption Tool")
root.configure(bg="#6f42c1")

# Custom Fonts
custom_font = font.Font(family="Helvetica", size=10, weight="bold")

# Organize layout
frame_top = tk.Frame(root, bg="#6f42c1")
frame_top.pack(padx=10, pady=10)

frame_bottom = tk.Frame(root, bg="#6f42c1")
frame_bottom.pack(padx=10, pady=10)

# Load icons
encrypt_icon = tk.PhotoImage(file="lock.png")
decrypt_icon = tk.PhotoImage(file="unlock.png")
show_key_icon = tk.PhotoImage(file="eye.png")
regenerate_icon = tk.PhotoImage(file="refresh.png")

# Create widgets
label_key = tk.Label(frame_top, text="Encryption/Decryption Key:", bg="#6f42c1", font=custom_font)
label_key.pack(side=tk.LEFT, padx=5)

entry_key = tk.Entry(frame_top, width=47, font=custom_font)
entry_key.pack(side=tk.LEFT, padx=5)

button_show_key = tk.Button(frame_bottom, text="Show Key", command=show_key, image=show_key_icon, compound="left")
button_show_key.pack(side=tk.LEFT, padx=5)

button_regenerate = tk.Button(frame_bottom, text="Regenerate Key", command=regenerate_key, image=regenerate_icon, compound="left")
button_regenerate.pack(side=tk.LEFT, padx=5)

button_encrypt = tk.Button(frame_bottom, text="Encrypt CSV", command=encrypt_csv, image=encrypt_icon, compound="left")
button_encrypt.pack(side=tk.LEFT, padx=5)

button_decrypt = tk.Button(frame_bottom, text="Decrypt CSV", command=decrypt_csv, image=decrypt_icon, compound="left")
button_decrypt.pack(side=tk.LEFT, padx=5)

label_status = tk.Label(root, text="", bg="#6f42c1", font=custom_font)
label_status.pack(pady=5)

load_or_create_key()  # Load or create the key when the application starts

# Start the GUI event loop
root.mainloop()