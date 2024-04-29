import tkinter as tk
from tkinter import filedialog
import csv
import random

def encrypt_csv():
    input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv")
        if output_file:
            encryption_key = entry_key.get()
            with open(input_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)

            encrypted_data = []
            for row in data:
                encrypted_row = []
                for field in row:
                    encrypted_field = ''.join(random.sample(field, len(field)))
                    encrypted_row.append(encrypted_field)
                encrypted_data.append(encrypted_row)

            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(encrypted_data)

def decrypt_csv():
    input_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if input_file:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv")
        if output_file:
            decryption_key = entry_key.get()
            with open(input_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                encrypted_data = list(reader)

            if decryption_key == '1234567890123456':  # This should match the encryption key
                decrypted_data = []
                for row in encrypted_data:
                    decrypted_row = []
                    for field in row:
                        decrypted_field = ''.join(sorted(field))
                        decrypted_row.append(decrypted_field)
                    decrypted_data.append(decrypted_row)

                with open(output_file, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(decrypted_data)
            else:
                label_status.config(text="Invalid decryption key!")

# Create the main window
root = tk.Tk()
root.title("CSV File Encryption Tool")
root.configure(bg="#6f42c1")

# Create widgets
label_key = tk.Label(root, text="Enter Encryption/Decryption Key:")
label_key.pack()

entry_key = tk.Entry(root)
entry_key.pack()

button_encrypt = tk.Button(root, text="Encrypt CSV", command=encrypt_csv)
button_encrypt.pack()

button_decrypt = tk.Button(root, text="Decrypt CSV", command=decrypt_csv)
button_decrypt.pack()

label_status = tk.Label(root, text="")
label_status.pack()

# Start the GUI event loop
root.mainloop()