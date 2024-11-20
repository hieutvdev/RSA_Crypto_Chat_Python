from app.adapters.db.db import MySQLPool
from app.core.rsa import generate_keypair


class User:
    def __init__(self):
        self.connection = MySQLPool().get_connection()
        self.cursor = self.connection.cursor()
        self.logged_in_user = None

    def login(self, username, password):
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            if result:
                self.logged_in_user = result
            return result
        except Exception as e:
            print(f"Error logging in: {e}")
            return None

    def register(self, username, password, email):
        try:
            public_key, private_key = generate_keypair()
            query = "INSERT INTO users (username, email, password, public_key, private_key) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (username, email, password, str(public_key), str(private_key)))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error registering user: {e}")
            return None

    def get_group_user(self, username):
        try:
            query = "SELECT * FROM users WHERE username != %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error getting group user: {e}")
            return None

    def save_message(self, chat_id, user_id, message_text, is_file=False, file_path=None):
        try:
            query = """
                    INSERT INTO Messages (chat_id, user_id, message_text, is_file, file_path)
                    VALUES (%s, %s, %s, %s, %s)
                    """
            self.cursor.execute(query, (chat_id, user_id, message_text, is_file, file_path))
            print("Message saved successfully", chat_id, user_id)
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print("Error saving message: ", e)

    def get_messages(self, chat_id):

        try:
            query = """
                SELECT message_id, chat_id, user_id, message_text, is_file, file_path, sent_at
                FROM Messages
                WHERE chat_id = %s
                ORDER BY sent_at ASC
                """
            self.cursor.execute(query, (chat_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return []
    def encrypt_message(self, message, public_key):
        # Implement encryption logic here
        return message