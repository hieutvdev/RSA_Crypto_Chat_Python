
from mysql.connector import pooling
from app.config.config import AppConfig


class MySQLPool:
    """
    MySQL Connection Pool class
    """

    def __init__(self):
        db_config = AppConfig().database
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name=db_config.POOL_NAME,
                pool_size=db_config.POOL_SIZE,
                pool_reset_session=True,
                host=db_config.HOST,
                port=db_config.PORT,
                user=db_config.USER,
                password=db_config.PASSWORD,
                database=db_config.DATABASE,
                connection_timeout=30
            )
            print("MySQL Connection Pool created successfully")
        except Exception as e:
            print(f"Error creating MySQL Connection Pool: {e}")
            raise

    def get_connection(self):
        try:
            connection = self.pool.get_connection()
            print("Database connection established successfully.")
            return connection
        except Exception as e:
            print(f"Error getting database connection: {e}")
            raise