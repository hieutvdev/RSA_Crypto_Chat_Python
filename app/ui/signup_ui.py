import tkinter as tk
from tkinter import messagebox
from app.adapters.db.dao.user import User

class RegisterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.user = User()
        self.create_register_ui()

    def create_register_ui(self):
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Password:").grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        if self.user.register(username, password, email):
            messagebox.showinfo("Registration Successful", "You have registered successfully")
            self.root.destroy()
            root = tk.Tk()
            from app.ui.login_ui import LoginUI
            LoginUI(root)
            root.mainloop()
        else:
            messagebox.showerror("Registration Failed", "Registration failed. Please try again.")