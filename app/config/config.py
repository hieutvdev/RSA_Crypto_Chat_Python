
class DatabaseConfig:
    """Configuration class for database-related environment variables"""

    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 4406
        self.USER = 'root'
        self.PASSWORD = 'root'
        self.DATABASE = 'rsa_chat'
        self.POOL_NAME = "rsa_chat_pool"
        self.POOL_SIZE = 5

class AppConfig:
    """Main configuration class that includes other configuration class"""
    def __init__(self):
        self.database = DatabaseConfig()
