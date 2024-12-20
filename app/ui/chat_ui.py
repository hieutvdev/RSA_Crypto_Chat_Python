import tkinter as tk
from tkinter import messagebox, filedialog
from app.adapters.db.dao.user import User
import os
from app.core.rsa import encrypt, decrypt
from PIL import Image, ImageTk

class ChatUI:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.user = User()
        self.create_chat_ui()

    def create_chat_ui(self):
        self.root.title(f"Chat - {self.logged_in_user[1]}")
        font_button = ("Helvetica", 12, "bold")

        # Create frames
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configure grid weights for resizing
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Fetch users
        self.users = self.user.get_group_user(self.logged_in_user[1])

        # Tạo Frame chứa Listbox
        user_list_frame = tk.Frame(left_frame, bg="#f5f5f5", padx=10, pady=10)
        user_list_frame.grid(row=0, column=0, sticky="ns")

        # create button logout
        logout_button = tk.Button(left_frame, text="Logout", font=font_button, bg="#0084ff", fg="white",
                                  command=self.open_login_ui)
        logout_button.grid(row=1, column=0, pady=10)
        user_list_label = tk.Label(
            user_list_frame,
            text="Users list",
            font=("Helvetica", 14, "bold"),
            bg="#f5f5f5",
            fg="#333"
        )
        user_list_label.pack(anchor="w", pady=(10))

        # Create Scrollbar and Listbox
        listbox_frame = tk.Frame(user_list_frame, bg="#f5f5f5", padx=5, pady=5)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.user_listbox = tk.Listbox(
            listbox_frame,
            height=20,
            width=30,
            font=("Helvetica", 12),
            bg="white",
            fg="black",
            selectbackground="#57a1f8",
            selectforeground="white",
            yscrollcommand=scrollbar.set,
            borderwidth=2,
            relief=tk.GROOVE,
            justify=tk.CENTER,
        )
        scrollbar.config(command=self.user_listbox.yview)

        # Add users to Listbox
        for user in self.users:
            self.user_listbox.insert(tk.END, f"User: {user[1]}")

        # Display Listbox and Scrollbar
        self.user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind event for selecting user in Listbox
        self.user_listbox.bind("<<ListboxSelect>>", self.load_chat)

        # Message entry and buttons

        # Load and resize icons
        img_path_send = os.path.abspath(os.path.join("images", "send.png"))
        img_path_file = os.path.abspath(os.path.join("images", "file.png"))

        send_image = Image.open(img_path_send)
        send_image = send_image.resize((30, 30), Image.LANCZOS)
        self.send_icon = ImageTk.PhotoImage(send_image)

        file_image = Image.open(img_path_file)
        file_image = file_image.resize((30, 30), Image.LANCZOS)
        self.file_icon = ImageTk.PhotoImage(file_image)

        self.message_entry = tk.Entry(right_frame,
                                      fg="black",
                                      border=2,
                                      relief=tk.FLAT,
                                      highlightcolor="blue",
                                      width=50, font=("Arial", 12))

        self.chat_display = tk.Text(right_frame, height=20, width=60, font=("Arial", 12), wrap=tk.WORD)
        self.chat_display.grid(row=0, columnspan=3, pady=(0, 10))
        self.message_entry.grid(row=1, column=0, pady=(10, 5), padx=(5, 5), sticky="ew")

        send_button = tk.Button(right_frame, command=self.send_message, bg="#fff", fg="white",
                                font=("Arial", 12, "bold"), bd=0, padx=10, pady=5, image=self.send_icon)
        send_button.grid(row=1, column=1, pady=(10, 5), padx=(5, 5))

        file_button = tk.Button(right_frame, command=self.send_file, bg="#0084ff", fg="white",
                                font=("Arial", 12, "bold"), bd=0, padx=10, pady=5, image=self.file_icon)
        file_button.grid(row=1, column=2, pady=(10, 5), padx=(5, 5))


        # Configure tags for styling messages
        self.chat_display.tag_configure("file", foreground="blue", underline=True)
        self.chat_display.tag_bind("file", "<Button-1>", self.download_and_decrypt_file)

    def load_chat(self, event):
        selected_user_index = self.user_listbox.curselection()
        if not selected_user_index:
            return

        selected_user = self.users[selected_user_index[0]]
        chat_id = self.get_chat_id(self.logged_in_user[0], selected_user[0])

        self.chat_display.delete(1.0, tk.END)
        messages = self.user.get_messages(chat_id)
        for message in messages:
            sender = "You" if message[2] == self.logged_in_user[0] else selected_user[1]
            if message[4]:  # is_file
                self.chat_display.insert(tk.END, f"{sender}: Sent a file: {os.path.basename(message[5])}\n", "file")
            else:
                self.chat_display.insert(tk.END, f"{sender}: {message[3]}\n", "user_message" if sender == "You" else "other_message")

    def send_message(self):
        selected_user_index = self.user_listbox.curselection()
        if not selected_user_index:
            messagebox.showerror("Error", "Please select a user to chat with")
            return

        selected_user = self.users[selected_user_index[0]]
        message = self.message_entry.get()

        if message:
            chat_id = self.get_chat_id(self.logged_in_user[0], selected_user[0])
            self.user.save_message(chat_id, self.logged_in_user[0], message, is_file=False, file_path=None)
            self.chat_display.insert(tk.END, f"You: {message}\n")
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Message cannot be empty")

    def send_file(self):
        selected_user_index = self.user_listbox.curselection()
        if not selected_user_index:
            messagebox.showerror("Error", "Please select a user to send the file to")
            return

        selected_user = self.users[selected_user_index[0]]
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                public_key = tuple(map(int, selected_user[5].strip('()').split(
                    ', ')))  # Assuming public_key is the sixth element in the tuple
                print(public_key)
                # Encrypt the file data using the recipient's public key
                encrypted_file_data = encrypt(public_key, file_data.decode('utf-8'))
                encrypted_file_data = ' '.join(map(str, encrypted_file_data)).encode('utf-8')

            # Ensure the data directory exists
            data_directory = 'D:/HK7/InformationSecurity/BTL/RSA_Crypto_PyThon/app/data'
            if not os.path.exists(data_directory):
                os.makedirs(data_directory)

            # Save the encrypted file in the data directory
            encrypted_file_path = os.path.join(data_directory, os.path.basename(file_path))
            with open(encrypted_file_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_file_data)

            # Save the file message in the database
            chat_id = self.get_chat_id(self.logged_in_user[0], selected_user[0])
            self.user.save_message(chat_id, self.logged_in_user[0], f"Sent a file: {os.path.basename(file_path)}",
                                   is_file=True, file_path=encrypted_file_path)

            self.chat_display.insert(tk.END,
                                     f"You (to {selected_user[1]}): Sent a file: {os.path.basename(file_path)}\n",
                                     "file")
        else:
            messagebox.showerror("Error", "No file selected")

    def download_and_decrypt_file(self, event):
        # Get the line where the file name is mentioned
        line_index = self.chat_display.index("@%s,%s linestart" % (event.x, event.y))
        line_text = self.chat_display.get(line_index, "%s lineend" % line_index)

        # Extract the file name from the line text
        file_name = line_text.split(": ")[-1].strip()
        encrypted_file_path = os.path.join('D:/HK7/InformationSecurity/BTL/RSA_Crypto_PyThon/app/data', file_name)

        if os.path.exists(encrypted_file_path):
            with open(encrypted_file_path, 'rb') as file:
                encrypted_file_data = file.read()
                encrypted_file_data = list(map(int, encrypted_file_data.decode('utf-8').split()))
                private_key = tuple(map(int, self.logged_in_user[6].strip('()').split(', ')))
                print(private_key)
                decrypted_file_data = decrypt(private_key, encrypted_file_data).encode('utf-8')

            data_directory = 'D:/HK7/InformationSecurity/BTL/RSA_Crypto_PyThon/app/data'
            if not os.path.exists(data_directory):
                os.makedirs(data_directory)

            # Save the decrypted file in the data directory
            decrypted_file_path = os.path.join(data_directory, 'decrypted_' + file_name)
            with open(decrypted_file_path, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_file_data)

            messagebox.showinfo("File Decrypted", f"Decrypted file saved at: {decrypted_file_path}")
            os.startfile(decrypted_file_path)
        else:
            messagebox.showerror("Error", "Encrypted file not found")

    def get_chat_id(self, user1_id, user2_id):
        try:
            query = """
            SELECT chat_id FROM ChatMembers
            WHERE chat_id IN (
                SELECT chat_id FROM ChatMembers WHERE user_id = %s
            ) AND user_id = %s
            """
            self.user.cursor.execute(query, (user1_id, user2_id))
            result = self.user.cursor.fetchone()
            if result:
                return result[0]

            # If no chat exists, create a new chat
            query = "INSERT INTO Chats (chat_name, is_group) VALUES (%s, %s)"
            self.user.cursor.execute(query, (f"Chat between {user1_id} and {user2_id}", False))
            chat_id = self.user.cursor.lastrowid

            # Add both users to the new chat
            query = "INSERT INTO ChatMembers (chat_id, user_id) VALUES (%s, %s)"
            self.user.cursor.execute(query, (chat_id, user1_id))
            self.user.cursor.execute(query, (chat_id, user2_id))
            self.user.connection.commit()

            return chat_id
        except Exception as e:
            print(f"Error getting or creating chat_id: {e}")
            return None

    def open_login_ui(self):
        from app.ui.login_ui import LoginUI
        self.root.destroy()
        root = tk.Tk()
        LoginUI(root)
        root.mainloop()