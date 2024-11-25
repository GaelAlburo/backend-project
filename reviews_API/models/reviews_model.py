import os
from reviews_API.logger.logger_base import Logger
from pymongo import MongoClient


# Model class for reviews that allows to connect to MongoDB
class ReviewModel:
    """Model class for reviews that allows to connect to MongoDB"""

    def __init__(self):
        self.client = None
        self.db = None
        self.logger = Logger()

    # Function to connect to MongoDB
    def connect_to_database(self):
        """Function to connect to MongoDB"""
        mongodb_user = os.environ.get("MONGODB_USER")
        mongodb_pass = os.environ.get("MONGODB_PASS")
        mongodb_host = os.environ.get("MONGODB_HOST")

        if not mongodb_user or not mongodb_pass or not mongodb_host:
            self.logger.critical("MongoDB environment variables are required")
            raise ValueError(
                "Set environment variables: MONGODB_USER, MONGODB_PASS, MONGODB_HOST"
            )

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

    # Function to close the connection to MongoDB
    def close_connection(self):
        """Function to close the connection to MongoDB"""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")


if __name__ == "__main__":
    db_conn = ReviewModel()
    logger = Logger()

    try:
        db_conn.connect_to_database()
    except Exception as e:
        logger.critical(f"Error ocurred: {e}")
    finally:
        db_conn.close_connection()
        logger.info("Connection closed successfully")
