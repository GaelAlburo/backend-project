import os
from logger.logger_orders import Logger
from pymongo import MongoClient


class OrdersModel:
    def __init__(self):
        self.client = None
        self.db = None
        self.logger = Logger()

    """ENVIROMENT VARIABLES"""

    def connect_to_database(self):
        mongodb_user = os.environ.get("MONGODB_USER")
        mongodb_pass = os.environ.get("MONGODB_PASS")
        mongodb_host = os.environ.get("MONGODB_HOST")

        if not mongodb_user or not mongodb_pass or not mongodb_host:
            self.logger.critical("MongoDB environment variables are required")
            raise ValueError(
                "Set environment variables: MONGODB_USER, MONGODB_PASS, MONGODB_HOST"
            )

        """CONECTION TO DATABASE"""
        try:
            self.client = MongoClient(
                host=mongodb_host,
                port=27017,
                username=mongodb_user,
                password=mongodb_pass,
                authSource="admin",
                authMechanism="SCRAM-SHA-256",
                serverSelectionTimeoutMS=5000,
            )
            self.db = self.client["project"]

            if self.db.list_collection_names():
                self.logger.info("Connected to MongoDB successfully")

        except Exception as e:
            self.logger.critical(f"Error connecting to MongoDB: {e}")
            raise

    def close_connection(self):
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")


"""TEST"""
if __name__ == "__main__":
    db_conn = OrdersModel()
    logger = Logger()
    try:
        db_conn.connect_to_database()
    except Exception as e:
        logger.critical(f"Error ocurred: {e}")
    finally:
        db_conn.close_connection()
        logger.info("Connection closed successfully")
