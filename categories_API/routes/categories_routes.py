from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from logger.logger_categories import Logger

class CategoryRoute(Blueprint):
    def __init__(self, category_service, category_schema):
        super().__init__("category", __name__)
        self.logger = Logger()
        self.category_service = category_service
        self.category_schema = category_schema
        self.register_routes()

    def register_routes(self):
        self.route("/api/v1/categories", methods=["GET"])(self.get_categories)
        self.route("/api/v1/categories", methods=["POST"])(self.add_category)
        self.route("/api/v1/categories/<int:category_id>", methods=["PUT"])(self.update_category)
        self.route("/api/v1/categories/<int:category_id>", methods=["DELETE"])(self.delete_category)

    @swag_from(
        {
            "tags": ["categories"],
            "responses": {
                200: {
                    "description": "GET all categories",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"}
                            },
                        },
                    },
                }
            },
        }
    )
    def get_categories(self):
        try:
            categories = self.category_service.get_all_categories()
            return jsonify(categories), 200
        except Exception as e:
            self.logger.error(f"Error fetching all categories: {e}")
            return jsonify({"error": f"Error fetching all categories: {e}"}), 500

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
    def add_category(self):
        try:
            request_data = request.json
            if not request_data or 'name' not in request_data:
                return jsonify({"error": "Name is required"}), 400

            validated_data = self.category_schema.load(request_data)
            created_category = self.category_service.add_category(validated_data)
            
            self.logger.info(f"Category added: {created_category}")
            return jsonify(created_category), 201

        except ValidationError as e:
            self.logger.error(f"Validation error: {e.messages}")
            return jsonify({"error": e.messages}), 400
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
        try:
            request_data = request.json
            if not request_data or 'name' not in request_data:
                return jsonify({"error": "Name is required"}), 400

            validated_data = self.category_schema.load(request_data)
            updated_category = self.category_service.update_category_name(
                category_id, 
                validated_data["name"]
            )
            
            if updated_category:
                self.logger.info(f"Category name updated: {updated_category}")
                return jsonify(updated_category), 200
            else:
                return jsonify({"error": "Category not found"}), 404

        except ValidationError as e:
            self.logger.error(f"Validation error: {e.messages}")
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            self.logger.error(f"Error updating category name: {e}")
            return jsonify({"error": f"Error updating category name: {e}"}), 500

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
        try:
            deleted_category = self.category_service.delete_category(category_id)
            if deleted_category:
                self.logger.info(f"Category deleted: {deleted_category}")
                return jsonify(deleted_category), 200
            else:
                return jsonify({"error": "Category not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting category: {e}")
            return jsonify({"error": f"Error deleting category: {e}"}), 500