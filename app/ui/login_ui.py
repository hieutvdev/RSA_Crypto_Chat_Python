import tkinter as tk
from tkinter import messagebox
from app.adapters.db.dao.user import User
from tkinter import ttk
class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x500")  # Adjusted size for single-column layout
        self.center_window(350, 500)  # Center the window
        self.user = User()
        self.create_login_ui()

    def center_window(self, width, height):

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_login_ui(self):
        frame = tk.Frame(self.root, padx=5, pady=0)
        frame.pack(expand=True)

        # Fonts
        font_label = ("Helvetica", 10)
        font_entry = ("Helvetica", 10)
        font_button = ("Helvetica", 10, "bold")

        # Username
        tk.Label(frame, text="Username:", font=font_label).pack(anchor="w", pady=1)
        self.username_entry = ttk.Entry(frame, font=font_entry, width=35)
        self.username_entry.pack(fill="x", pady=0, ipady=8)

        # Add Canvas for underline effect
        canvas = tk.Canvas(frame, height=1, bg='gray', bd=0, highlightthickness=0)
        canvas.pack(fill='x', pady=0)

        # Password
        tk.Label(frame, text="Password:", font=font_label).pack(anchor="w", pady=5)
        self.password_entry = ttk.Entry(frame, font=font_entry, width=35, show="*")
        self.password_entry.pack(fill="x", pady=0, ipady=8)

        # Add Canvas for underline effect
        canvas = tk.Canvas(frame, height=1, bg='gray', bd=0, highlightthickness=0)
        canvas.pack(fill='x', pady=0)

        # Buttons
        tk.Button(frame, text="Login", command=self.login, font=font_button, width=15).pack(pady=5)
        tk.Button(frame, text="Register", command=self.open_register_ui, font=font_button, width=15).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user.login(username, password):
            messagebox.showinfo("Login Successful", "You have logged in successfully")
            self.open_chat_ui(username, password)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_register_ui(self):
        from app.ui.signup_ui import RegisterUI
        self.root.destroy()
        root = tk.Tk()
        RegisterUI(root)
        root.mainloop()

    def open_chat_ui(self, username, password):
        from app.ui.chat_ui import ChatUI
        self.root.destroy()
        root = tk.Tk()
        ChatUI(root, self.user.login(username, password))
        root.mainloop()