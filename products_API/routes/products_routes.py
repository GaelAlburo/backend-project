from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from logger.logger_products import Logger


class ProductRoute(Blueprint):
    """Class that handles the product routes in the API"""

    def __init__(self, product_service, product_schema):
        super().__init__("product", __name__)
        self.logger = Logger()
        self.product_service = product_service
        self.product_schema = product_schema
        self.register_routes()

    def register_routes(self):
        self.route("/api/v1/products", methods=["GET"])(self.get_products)
        self.route("/api/v1/products", methods=["POST"])(self.add_product)
        self.route("/api/v1/products/<int:product_id>", methods=["PUT"])(
            self.update_product
        )
        self.route("/api/v1/products/<int:product_id>", methods=["DELETE"])(
            self.delete_product
        )
        self.route("/healthcheck", methods=["GET"])(self.healthcheck)

    @swag_from(
        {
            "tags": ["products"],
            "responses": {
                200: {
                    "description": "GET all products",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "String"},
                                "price": {"type": "String"},
                                "category": {"type": "String"},
                            },
                        },
                    },
                }
            },
        }
    )
    def get_products(self):
        """Fetches all the products"""

        products = self.product_service.get_all_products()
        return jsonify(products), 200

    def fetch_request_data(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "No input data provided"}), 400

            name = request_data["name"]
            price = request_data["price"]
            category = request_data["category"]

            try:
                self.product_schema.validate_name(name)
                self.product_schema.validate_price(price)
                self.product_schema.validate_category(category)
            except ValidationError as e:
                self.logger.error(f"Invalid data: {e}")
                return jsonify({"error": f"Invalid data: {e}"}), 400

            return name, price, category

        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return jsonify({"error": f"Error fetching the request data: {e}"}), 400

    @swag_from(
        {
            "tags": ["products"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "string"},
                            "category": {"type": "string"},
                        },
                        "required": ["name", "price", "category"],
                    },
                }
            ],
            "responses": {
                201: {
                    "description": "Product added successfully",
                },
                400: {"description": "Invalid data"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def add_product(self):
        """Add a new product to the database"""

        try:
            name, price, category = self.fetch_request_data()

            new_product = {
                "name": name,
                "price": price,
                "category": category,
                "image": "/shirt-test.jpeg",
            }

            created_product = self.product_service.add_product(new_product)
            self.logger.info(f"Product added: {created_product}")
            return jsonify(created_product), 201

        except Exception as e:
            self.logger.error(f"Error adding the product: {e}")
            return jsonify({"error": f"Error adding the product: {e}"}), 500

    @swag_from(
        {
            "tags": ["products"],
            "parameters": [
                {
                    "name": "product_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                },
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "string"},
                            "category": {"type": "string"},
                        },
                        "required": ["name", "price", "category"],
                    },
                },
            ],
            "responses": {
                200: {"description": "Product updated successfully"},
                400: {"description": "Invalid data"},
                404: {"description": "Product not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def update_product(self, product_id):
        """Update a product in the database by its ID"""

        try:
            name, price, category = self.fetch_request_data()

            update_product = {
                "name": name,
                "price": price,
                "category": category,
            }

            updated_product = self.product_service.update_product(
                product_id, update_product
            )

            if updated_product:
                self.logger.info(f"Product updated: {updated_product}")
                return jsonify(update_product), 200
            else:
                self.logger.error(f"Product not found")
                return jsonify({"error": "Product not found"}), 404

        except Exception as e:
            self.logger.error(f"Error updating the product: {e}")
            return jsonify({"error": f"Error updating the product: {e}"}), 500

    @swag_from(
        {
            "tags": ["products"],
            "parameters": [
                {
                    "name": "product_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {"description": "Product deleted successfully"},
                404: {"description": "Product not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def delete_product(self, product_id):
        """Deletes a product from the database"""

        try:
            deleted_product = self.product_service.delete_product(product_id)
            if deleted_product:
                self.logger.info(f"Product deleted: {deleted_product}")
                return jsonify(deleted_product), 200
            else:
                self.logger.error(f"Product not found")
                return jsonify({"error": "Product not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting the product: {e}")
            return jsonify({"error": f"Error deleting the product: {e}"}), 500

    def healthcheck(self):
        """Function to check the health of the API in the docker container"""

        return jsonify({"status": "Up"}), 200
