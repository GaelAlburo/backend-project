from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from reviews_API.logger.logger_base import Logger


class ReviewRoute(Blueprint):
    """Class to handle the review routes"""

    def __init__(self, review_service, review_schema):
        super().__init__("review", __name__)
        self.logger = Logger()
        self.review_service = review_service
        self.review_schema = review_schema
        self.register_routes()

    def register_routes(self):
        """Function to register the routes for the review service"""

        self.route("/api/v1/reviews", methods=["GET"])(self.get_reviews)
        self.route("/api/v1/reviews", methods=["POST"])(self.add_review)
        self.route("/api/v1/reviews/<int:review_id>", methods=["PUT"])(
            self.update_review
        )
        self.route("/api/v1/reviews/<int:review_id>", methods=["DELETE"])(
            self.delete_review
        )
        self.route("/healthcheck", methods=["GET"])(self.healthcheck)

    # Swagger documentation for the GET request to /api/v1/reviews
    @swag_from(
        {
            "tags": ["reviews"],
            "responses": {
                200: {
                    "description": "GET all reviews",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "user": {"type": "String"},
                                "product": {"type": "String"},
                                "review": {"type": "String"},
                                "rating": {"type": "String"},
                            },
                        },
                    },
                }
            },
        }
    )
    def get_reviews(self):
        """Function to fetch all reviews"""
        reviews = self.review_service.get_all_reviews()
        return jsonify(reviews), 200

    def fetch_request_data(self):
        """Function to fetch the request data from the request body and validate it with the schema"""

        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            user = request_data.get("user")
            product = request_data.get("product")
            review = request_data.get("review")
            rating = request_data.get("rating")

            try:
                self.review_schema.validates_user(user)
                self.review_schema.validates_product(product)
                self.review_schema.validates_review(review)
                self.review_schema.validates_rating(rating)

            except ValidationError as e:
                self.logger.error(f"Invalid data: {e}")
                return jsonify({"error": f"Invalid data: {e}"}), 400

            return user, product, review, rating

        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return jsonify({"error": f"Error fetching the request data: {e}"}), 500

    # Swagger documentation for the POST request to /api/v1/reviews
    @swag_from(
        {
            "tags": ["reviews"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "user": {"type": "string"},
                            "product": {"type": "string"},
                            "review": {"type": "string"},
                            "rating": {"type": "string"},
                        },
                        "required": ["user", "product", "review", "rating"],
                    },
                }
            ],
            "responses": {
                201: {
                    "description": "Review added successfully",
                },
                400: {"description": "Invalid data"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def add_review(self):
        """Function to add a review to the database"""

        try:
            user, product, review, rating = self.fetch_request_data()

            new_review = {
                "user": user,
                "product": product,
                "review": review,
                "rating": rating,
            }

            created_review = self.review_service.add_review(new_review)
            self.logger.info(f"Review added: {created_review}")
            return jsonify(created_review), 201

        except Exception as e:
            self.logger.error(f"Error adding review: {e}")
            return jsonify({"error": f"Error adding review: {e}"}), 500

    # Swagger documentation for the PUT request to /api/v1/reviews/<review_id>
    @swag_from(
        {
            "tags": ["reviews"],
            "parameters": [
                {
                    "name": "review_id",
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
                            "user": {"type": "string"},
                            "product": {"type": "string"},
                            "review": {"type": "string"},
                            "rating": {"type": "string"},
                        },
                        "required": ["user", "product", "review", "rating"],
                    },
                },
            ],
            "responses": {
                200: {"description": "Review updated successfully"},
                400: {"description": "Invalid data"},
                404: {"description": "Review not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def update_review(self, review_id):
        """Function to update a review by its ID"""

        try:
            user, product, review, rating = self.fetch_request_data()

            update_review = {
                "_id": review_id,
                "user": user,
                "product": product,
                "review": review,
                "rating": rating,
            }

            updated_review = self.review_service.update_review(review_id, update_review)
            if updated_review:
                return jsonify(update_review), 200
            else:
                self.logger.error("Review not found")
                return jsonify({"error": "Review not found"}), 404

        except Exception as e:
            self.logger.error(f"Error updating review: {e}")
            return jsonify({"error": f"Error updating review: {e}"}), 500

    # Swagger documentation for the DELETE request to /api/v1/reviews/<review_id>
    @swag_from(
        {
            "tags": ["reviews"],
            "parameters": [
                {
                    "name": "review_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {"description": "Review deleted successfully"},
                404: {"description": "Review not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def delete_review(self, review_id):
        """Function to delete a review by its ID"""

        try:
            deleted_review = self.review_service.delete_review(review_id)
            if deleted_review:
                return jsonify(deleted_review), 200
            else:
                return jsonify({"error": "Review not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting review: {e}")
            return jsonify({"error": f"Error deleting review: {e}"}), 500

    def healthcheck(self):
        """Function to check the health of the docker container"""

        return jsonify({"status": "Up"}), 200
