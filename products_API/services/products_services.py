from flask import jsonify
from logger.logger_products import Logger


class ProductService:
    """Service class to that implements the logic of the CRUD operations for products"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_products(self):
        """Function to fetch all products from the database"""

        try:
            products = list(self.db_conn.db.products.find())
            return products
        except Exception as e:
            self.logger.error(f"Error fetching all products from database: {e}")
            return (
                jsonify({"error": f"Error fetching all products from database: {e}"}),
                500,
            )

    def get_product_by_id(self, product_id):
        """Function to fetch a product by its id"""

        try:
            product = self.db_conn.db.products.find_one({"_id": product_id})
            return product
        except Exception as e:
            self.logger.error(f"Error fetching product by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching product by id from database: {e}"}),
                500,
            )

    def add_product(self, new_product):
        """Function to add a product to the database"""

        try:
            max_id = self.db_conn.db.products.find_one(sort=[("_id", -1)])["_id"]
            next_id = max_id + 1
            new_product["_id"] = next_id

            self.db_conn.db.products.insert_one(new_product)
            return new_product
        except Exception as e:
            self.logger.error(f"Error adding product to database: {e}")
            return jsonify({"error": f"Error adding product to database: {e}"}), 500

    def update_product(self, product_id, product):
        """Function that updates a product in the database by its id"""

        try:
            update_product = self.get_product_by_id(product_id)
            if update_product:
                updated_product = self.db_conn.db.products.update_one(
                    {"_id": product_id}, {"$set": product}
                )
                if updated_product.modified_count > 0:
                    return updated_product
                else:
                    return "The product is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating product in database: {e}")
            return jsonify({"error": f"Error updating product in database: {e}"}), 500

    def delete_product(self, product_id):
        """Function that deletes a product from the database by its id"""

        try:
            deleted_product = self.get_product_by_id(product_id)
            if deleted_product:
                self.db_conn.db.products.delete_one({"_id": product_id})
                return deleted_product
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting product from database: {e}")
            return jsonify({"error": f"Error deleting product from database: {e}"}), 500
