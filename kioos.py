import cv2
import os
import string
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class SteganographyGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Open stego clone by Priyansh")

        # Variables
        self.file_path_var = tk.StringVar()
        self.decrypt_password_var = tk.StringVar()
        self.file_path_var2 = tk.StringVar()
        self.secret_message_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Create a Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)

        # Page for Encryption
        self.encrypt_page = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypt_page, text="Encrypt")

        # Encrypt Button
        self.encrypt_button = tk.Button(self.encrypt_page, text="Browse for Cover Image", command=self.browse_file_encrypt)
        self.encrypt_button.pack(pady=10)

        # Form Tab for Encrypt
        self.encrypt_form_label = tk.Label(self.encrypt_page, text="Or manually type file path:")
        self.encrypt_form_label.pack()
        self.encrypt_entry = tk.Entry(self.encrypt_page, textvariable=self.file_path_var)
        self.encrypt_entry.pack()

        # Secret Message Form
        self.secret_message_label = tk.Label(self.encrypt_page, text="Secret Message:")
        self.secret_message_label.pack()
        self.secret_message_entry = tk.Entry(self.encrypt_page, textvariable=self.secret_message_var)
        self.secret_message_entry.pack()

        # Password Form
        self.password_label = tk.Label(self.encrypt_page, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.encrypt_page, show="*", textvariable=self.password_var)
        self.password_entry.pack()

        # Start Encryption Button
        self.start_encryption_button = tk.Button(self.encrypt_page, text="Start Encryption", command=self.start_encryption)
        self.start_encryption_button.pack(pady=10)

        # Page for Decryption
        self.decrypt_page = ttk.Frame(self.notebook)
        self.notebook.add(self.decrypt_page, text="Decrypt")

        # Decrypt Button
        self.decrypt_button = tk.Button(self.decrypt_page, text="Browse for Encrypted Image", command=self.browse_file_decrypt)
        self.decrypt_button.pack(pady=10)

        # Form Tab for Decrypt
        self.decrypt_form_label = tk.Label(self.decrypt_page, text="Or manually input file path:")
        self.decrypt_form_label.pack()
        self.decrypt_entry = tk.Entry(self.decrypt_page, textvariable=self.file_path_var2)
        self.decrypt_entry.pack()

        # Password Form for Decryption
        self.decrypt_password_label = tk.Label(self.decrypt_page, text="Password:")
        self.decrypt_password_label.pack()
        self.decrypt_password_entry = tk.Entry(self.decrypt_page, show="*", textvariable=self.decrypt_password_var)
        self.decrypt_password_entry.pack()

        # Decrypt Image Button
        self.decrypt_image_button = tk.Button(self.decrypt_page, text="Decrypt", command=self.decrypt_image)
        self.decrypt_image_button.pack(pady=10)

        # Switch Page Buttons
        self.encrypt_page_button = tk.Button(master, text="Encryption Page", command=lambda: self.notebook.select(self.encrypt_page))
        self.encrypt_page_button.pack(side="left", padx=10)

        self.decrypt_page_button = tk.Button(master, text="Decryption Page", command=lambda: self.notebook.select(self.decrypt_page))
        self.decrypt_page_button.pack(side="left", padx=10)

        # Center the GUI on the screen
        self.center_window()

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        width = int(screen_width * 0.5)
        height = int(screen_height * 0.5)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def browse_file_encrypt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.file_path_var.set(file_path)
            print("Selected Cover Image:", file_path)

    def browse_file_decrypt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.file_path_var2.set(file_path)
            print("Selected Encrypted Image:", file_path)

    def start_encryption(self):
        # Implement encryption logic here
        file_path = self.file_path_var.get()
        secret_message = self.secret_message_var.get()
        password = self.password_var.get()

        if not (file_path and secret_message and password):
            tk.messagebox.showinfo("Error", "Please enter complete information.")
            return

        img = cv2.imread(file_path)

        d = {}
        c = {}

        for i in range(255):
            d[chr(i)] = i
            c[i] = chr(i)

        m = 0
        n = 0
        z = 0

        for i in range(len(secret_message)):
            img[n, m, z] = d[secret_message[i]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3

        cv2.imwrite("Encryptedmsg.jpg", img)
        os.system("start Encryptedmsg.jpg")

    def decrypt_image(self):
        file_path = self.file_path_var2.get()
        password = self.decrypt_password_var.get()

        if not (file_path and password):
            tk.messagebox.showinfo("Error", "Please enter complete information.")
            return

        # Implement decryption logic here
        img = cv2.imread(file_path)

        d = {}
        c = {}

        for i in range(255):
            d[chr(i)] = i
            c[i] = chr(i)

        message = ""

        n = 0
        m = 0
        z = 0

        for i in range(len(self.secret_message_var.get())):
            message = message + c[int(img[n, m, z])]%3
            n = n + 1
            m = m + 1
            z = (z + 1) % 3

        print("Decrypting", message)

def main():
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
