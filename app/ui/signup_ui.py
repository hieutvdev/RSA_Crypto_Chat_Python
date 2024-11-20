import tkinter as tk
from tkinter import messagebox
from app.adapters.db.dao.user import User
from app.ui.login_ui import LoginUI
import os

class RegisterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("350x500")
        self.center_window(350, 500)  # Center the window

        self.user = User()
        self.create_register_ui()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_register_ui(self):
        frame = tk.Frame(self.root, padx=5, pady=0)
        frame.pack(expand=True)
        tk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e")
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=1, column=1)

        tk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e")
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Button(frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.user.register(username, password, email):
            messagebox.showinfo("Registration Successful", "You have registered successfully")
            self.root.destroy()
            root = tk.Tk()
            LoginUI(root)
            root.mainloop()
        else:
            messagebox.showerror("Registration Failed", "Registration failed. Please try again.")