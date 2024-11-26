from flask import jsonify
from logger.logger_categories import Logger


class CategoryService:
    """Service class to that implements the logic of the CRUD operations for categories"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_categories(self):
        """Function to fetch all categories from the database"""

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
                jsonify(
                    {"error": f"Error fetching categories by id from database: {e}"}
                ),
                500,
            )

    def add_category(self, new_category):
        """Function to add a category to the database"""

        try:
            # Gets the highest id
            if self.db_conn.db.categories.count_documents({}) == 0:
                new_category["_id"] = 1
            else:
                max_id = self.db_conn.db.categories.find_one(sort=[("_id", -1)])["_id"]
                next_id = max_id + 1
                new_category["_id"] = next_id

            self.db_conn.db.categories.insert_one(new_category)
            return new_category
        except Exception as e:
            self.logger.error(f"Error adding category to database: {e}")
            return jsonify({"error": f"Error adding category to database: {e}"}), 500

    def update_category(self, category_id, categories):
        """Function that updatse a category in the database by its id"""

        try:
            update_category = self.get_categories_by_id(category_id)
            if update_category:
                updated_category = self.db_conn.db.categories.update_one(
                    {"_id": category_id}, {"$set": categories}
                )
                if updated_category.modified_count > 0:
                    return update_category
                else:
                    return "The categories is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating the category in database: {e}")
            return (
                jsonify({"error": f"Error updating the category in database: {e}"}),
                500,
            )

    def delete_category(self, category_id):
        """Function to delete a categories from the database by its id"""

        try:
            deleted_category = self.get_categories_by_id(category_id)
            if deleted_category:
                self.db_conn.db.categories.delete_one({"_id": category_id})
                return deleted_category
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting the category from database: {e}")
            return (
                jsonify({"error": f"Error deleting the category from database: {e}"}),
                500,
            )
