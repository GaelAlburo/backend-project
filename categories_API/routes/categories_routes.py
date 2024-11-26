from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from logger.logger_categories import Logger


class CategoryRoute(Blueprint):
    """Class to handle the category routes"""

    def __init__(self, category_service, category_schema):
        super().__init__("category", __name__)
        self.logger = Logger()
        self.category_service = category_service
        self.category_schema = category_schema
        self.register_routes()

    def register_routes(self):
        """Function to register the routes for the category API"""

        self.route("/api/v1/categories", methods=["GET"])(self.get_categories)
        self.route("/api/v1/categories", methods=["POST"])(self.add_category)
        self.route("/api/v1/categories/<int:category_id>", methods=["PUT"])(
            self.update_category
        )
        self.route("/api/v1/categories/<int:category_id>", methods=["DELETE"])(
            self.delete_category
        )
        self.route("/healthcheck", methods=["GET"])(self.healthcheck)

    @swag_from(
        {
            "tags": ["categories"],
            "responses": {
                200: {
                    "description": "Fetches all categories",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                            },
                        },
                    },
                }
            },
        }
    )
    def get_categories(self):
        """Fetches all categories"""

        categories = self.category_service.get_all_categories()
        return jsonify(categories), 200

    @swag_from(
        {
            "tags": ["categories"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                        "required": ["name"],
                    },
                }
            ],
            "responses": {
                201: {"description": "Category added successfully"},
                400: {"description": "Invalid data"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def fetch_request_data(self):
        """Function to fetch the request data from the request body and validate it with the schema"""

        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            name = request_data.get("name")

            try:
                self.category_schema.validate_name(name)

            except ValidationError as e:
                self.logger.error(f"Invalid data: {e}")
                return jsonify({"error": f"Invalid data: {e}"}), 400

            return name

        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return jsonify({"error": f"Error fetching the request data: {e}"}), 500

    @swag_from(
        {
            "tags": ["categories"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                        "required": ["name"],
                    },
                },
            ],
            "responses": {
                201: {"description": "Category added successfully"},
                400: {"description": "Invalid data"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def add_category(self):
        """Adds a new category"""

        try:
            name = self.fetch_request_data()

            new_category = {"name": name}

            created_category = self.category_service.add_category(new_category)
            self.logger.info(f"Category added: {created_category}")
            return jsonify(created_category), 201

        except Exception as e:
            self.logger.error(f"Error adding category: {e}")
            return jsonify({"error": f"Error adding category: {e}"}), 500

    @swag_from(
        {
            "tags": ["categories"],
            "parameters": [
                {
                    "name": "category_id",
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
                        },
                        "required": ["name"],
                    },
                },
            ],
            "responses": {
                200: {"description": "Category name updated successfully"},
                400: {"description": "Invalid data"},
                404: {"description": "Category not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def update_category(self, category_id):
        """Updates the name of a category"""

        try:
            name = self.fetch_request_data()

            update_category = {"name": name}

            updated_category = self.category_service.update_category(
                category_id, update_category
            )
            if updated_category:
                self.logger.info(f"Category updated: {updated_category}")
                return jsonify(updated_category), 200
            else:
                self.logger.error("Category not found")
                return jsonify({"error": "Category not found"}), 404

        except Exception as e:
            self.logger.error(f"Error updating category: {e}")
            return jsonify({"error": f"Error updating category: {e}"}), 500

    @swag_from(
        {
            "tags": ["categories"],
            "parameters": [
                {
                    "name": "category_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {"description": "Category deleted successfully"},
                404: {"description": "Category not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def delete_category(self, category_id):
        """Deletes a category"""

        try:
            deleted_category = self.category_service.delete_category(category_id)
            if deleted_category:
                self.logger.info(f"Category deleted: {deleted_category}")
                return jsonify(deleted_category), 200
            else:
                self.logger.error("Category not found")
                return jsonify({"error": "Category not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting category: {e}")
            return jsonify({"error": f"Error deleting category: {e}"}), 500

    def healthcheck(self):
        """Healthcheck endpoint for the category API container"""

        return jsonify({"status": "Up"}), 200
