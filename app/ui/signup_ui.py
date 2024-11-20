import tkinter as tk
from tkinter import messagebox
from app.adapters.db.dao.user import User
from app.ui.login_ui import LoginUI
import os
from PIL import Image, ImageTk


class RegisterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("925x500+300+200")  # Adjusted size for single-column layout
        self.root.resizable(False, False)  # Disable resizing
        self.root.configure(bg="white")  # Set background color
        self.user = User()
        self.create_register_ui()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_register_ui(self):
        frame = tk.Frame(self.root, padx=20, pady=20, bg="white")
        frame.pack(expand=True)
        img_path = os.path.abspath(os.path.join("images", "signup.png"))

        # Open and resize the image using Pillow
        img = Image.open(img_path)
        img = img.resize((400, 350), Image.LANCZOS)  # Adjust the size as needed
        self.img = ImageTk.PhotoImage(img)  # Convert to PhotoImage

        # Create a sub-frame for centering the content
        sub_frame = tk.Frame(frame, bg="white")
        sub_frame.pack(expand=True)

        # Image on the left
        tk.Label(sub_frame, image=self.img, bg="white").grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="w")

        # Fonts
        font_label = ("Helvetica", 12)
        font_entry = ("Helvetica", 12)
        font_button = ("Helvetica", 12, "bold")

        heading = tk.Label(sub_frame, text="Sign up", fg="#57a1f8", bg="white",
                           font=("Microsoft YaHei UI Light", 23, "bold"))
        heading.grid(row=0, column=1, columnspan=2, pady=10, sticky="w")

        # Username
        tk.Label(sub_frame, text="Username: ", font=font_label, bg="white").grid(row=1, column=1, pady=10, sticky="e")
        self.username_entry = tk.Entry(sub_frame, font=font_entry, width=35)
        self.username_entry.grid(row=1, column=2, pady=10, ipady=8, sticky="we")

        # Email
        tk.Label(sub_frame, text="Email: ", font=font_label, bg="white").grid(row=2, column=1, pady=10, sticky="e")
        self.email_entry = tk.Entry(sub_frame, font=font_entry, width=35)
        self.email_entry.grid(row=2, column=2, pady=10, ipady=8, sticky="we")

        # Password
        tk.Label(sub_frame, text="Password: ", font=font_label, bg="white").grid(row=3, column=1, pady=10, sticky="e")
        self.password_entry = tk.Entry(sub_frame, font=font_entry, width=35, show="*")
        self.password_entry.grid(row=3, column=2, pady=10, ipady=8, sticky="we")

        # Buttons
        button_style = {"font": font_button, "bg": "#57a1f8", "fg": "white", "padx": 10, "pady": 5, "bd": 3,
                        "relief": "raised"}
        tk.Button(sub_frame, text="Register", command=self.register, width=35, **button_style).grid(row=4, column=2, pady=0,
                                                                                              sticky="e")

        tk.Label(sub_frame, text="Have an account?", fg='black', bg="white",
                 font=("Microsoft YaHei UI Light", 12)).grid(row=5, column=2, pady=0, sticky="w")
        tk.Button(sub_frame, text="Login", command=self.open_login_ui, **button_style).grid(row=5, column=2,
                                                                                                  pady=10, sticky="e")

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


    def open_login_ui(self):
        from app.ui.login_ui import LoginUI
        self.root.destroy()
        root = tk.Tk()
        LoginUI(root)
        root.mainloop()