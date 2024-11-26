from flask import jsonify
from logger.logger_base import Logger


class UserService:

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_users(self):
        try:
            users = list(self.db_conn.db.users.find())  # retry all documents
            return users
        except Exception as e:
            self.logger.error(f"Error fetching all users from database: {e}")
            return (
                jsonify({"error": f"Error fetching all users from database: {e}"}),
                500,
            )

    def get_users_by_user_email(self, user_email):

        try:
            user = self.db_conn.db.users.find_one(
                {"email": user_email}
            )  # filter by user email
            return user
        except Exception as e:
            self.logger.error(f"Error fetching user by email from database: {e}")
            return (
                jsonify({"error": f"Error fetching user by email from database: {e}"}),
                500,
            )

    def get_users_by_user_id(self, user_id):

        try:
            user = self.db_conn.db.users.find_one(
                {"_id": user_id}
            )  # filter by user email
            return user
        except Exception as e:
            self.logger.error(f"Error fetching user by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching user by id from database: {e}"}),
                500,
            )

    def create_new_user(self, new_user):

        try:
            existing_user = self.get_users_by_user_email(new_user["email"])
            if existing_user:
                self.logger.error(
                    f"Error adding new user to database: Email is already registered"
                )
                return "Email is already registered", 500

            if self.db_conn.db.users.count_documents({}) == 0:
                new_user["_id"] = 1
            else:
                max_id = self.db_conn.db.users.find_one(sort=[("_id", -1)])[
                    "_id"
                ]  # Gets the highest id
                next_id = max_id + 1
                new_user["_id"] = next_id

            self.db_conn.db.users.insert_one(new_user)
            return new_user, 201

        except Exception as e:
            self.logger.error(f"Error adding new user to database: {e}")
            return jsonify({"error": f"Error adding new user to database: {e}"}), 500

    def update_user(self, user_id, user):

        try:
            update_user = self.get_users_by_user_id(user_id)
            if update_user:
                updated_user = self.db_conn.db.users.update_one(
                    {"_id": user_id}, {"$set": user}
                )
                if updated_user.modified_count > 0:
                    return updated_user
                else:
                    return "The review is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating user in database: {e}")
            return jsonify({"error": f"Error updating user in database: {e}"}), 500

    def delete_user(self, user_id):

        try:
            deleted_user = self.get_users_by_user_id(user_id)
            if deleted_user:
                self.db_conn.db.users.delete_one({"_id": user_id})
                return deleted_user
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting review from database: {e}")
            return jsonify({"error": f"Error deleting review from database: {e}"}), 500
