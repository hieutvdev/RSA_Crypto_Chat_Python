import tkinter as tk

from app.ui.login_ui import LoginUI


class Root:
    def __init__(self):
        root = tk.Tk()
        root.title("RSA Chat")
        LoginUI(root)
        root.mainloop()





