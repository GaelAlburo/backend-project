from flask import jsonify
from logger.logger_categories import Logger


class CategoryService:
    """Service class to that implements the logic of the CRUD operations for categories"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_categories(self):

        try:
            categories = list(self.db_conn.db.categories.find())
            return categories
        except Exception as e:
            self.logger.error(f"Error fetching all categories from database: {e}")
            return (
                jsonify({"error": f"Error fetching all categories from database: {e}"}),
                500,
            )

    def get_categories_by_id(self, categories_id):
        """Function to fetch a categories by its id"""

        try:
            categories = self.db_conn.db.categories.find_one({"_id": categories_id})
            return categories
        except Exception as e:
            self.logger.error(f"Error fetching categories by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching categories by id from database: {e}"}),
                500,
            )

    def add_categories(self, new_categories):
        """Function to add a categories to the database"""

        try:
            # Gets the highest id
            max_id = self.db_conn.db.categories.find_one(sort=[("_id", -1)])["_id"]
            next_id = max_id + 1
            new_categories["_id"] = next_id

            self.db_conn.db.categories.insert_one(new_categories)
            return new_categories
        except Exception as e:
            self.logger.error(f"Error adding categories to database: {e}")
            return jsonify({"error": f"Error adding categories to database: {e}"}), 500

    def update_categories(self, categories_id, categories):
        """Function that updatse a categories in the database by its id"""

        try:
            update_categories = self.get_categories_by_id(categories_id)
            if update_categories:
                updated_categories = self.db_conn.db.categories.update_one(
                    {"_id": categories_id}, {"$set": categories}
                )
                if updated_categories.modified_count > 0:
                    return updated_categories
                else:
                    return "The categories is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating categories in database: {e}")
            return jsonify({"error": f"Error updating categories in database: {e}"}), 500

    def delete_categories(self, categories_id):
        """Function to delete a categories from the database by its id"""

        try:
            deleted_categories = self.get_categories_by_id(categories_id)
            if deleted_categories:
                self.db_conn.db.categories.delete_one({"_id": categories_id})
                return deleted_categories
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting categories from database: {e}")
            return jsonify({"error": f"Error deleting categories from database: {e}"}), 500
