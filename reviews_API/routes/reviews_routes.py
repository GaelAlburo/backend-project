from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from reviews_API.logger.logger_base import Logger


class ReviewRoute(Blueprint):
    def __init__(self, review_service, review_schema):
        super().__init__("review", __name__)
        self.logger = Logger()
        self.review_service = review_service
        self.review_schema = review_schema
        self.register_routes()

    def register_routes(self):
        self.route("/api/v1/reviews", methods=["GET"])(self.get_reviews)
        self.route("/api/v1/reviews", methods=["POST"])(self.add_review)
        self.route("/api/v1/reviews/<int:review_id>", methods=["PUT"])(
            self.update_review
        )
        self.route("/api/v1/reviews/<int:review_id>", methods=["DELETE"])(
            self.delete_review
        )

    def get_reviews(self):
        reviews = self.review_service.get_all_reviews()
        return jsonify(reviews), 200

    def fetch_request_data(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            user = request_data.get("user")
            product = request_data.get("product")
            review = request_data.get("review")
            rating = request_data.get("rating")

            return user, product, review, rating

        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return jsonify({"error": f"Error fetching the request data: {e}"}), 500

    def add_review(self):
        try:
            user, product, review, rating = self.fetch_request_data()

            try:
                self.review_schema.validates_user(user)
                self.review_schema.validates_product(product)
                self.review_schema.validates_review(review)
                self.review_schema.validates_rating(rating)
            except ValidationError as e:
                return jsonify({"error": f"Invalid data: {e}"}), 400

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

    def update_review(self, review_id):
        try:
            user, product, review, rating = self.fetch_request_data()

            try:
                self.review_schema.validates_user(user)
                self.review_schema.validates_product(product)
                self.review_schema.validates_review(review)
                self.review_schema.validates_rating(rating)
            except ValidationError as e:
                return jsonify({"error": f"Invalid data: {e}"}), 400

            update_review = {
                "_id": review_id,
                "user": user,
                "product": product,
                "review": review,
                "rating": rating,
            }

            updated_review = self.review_service.update_review(review_id, update_review)
            if updated_review:
                return jsonify(updated_review), 200
            else:
                return jsonify({"error": "Review not found"}), 404

        except Exception as e:
            self.logger.error(f"Error updating review: {e}")
            return jsonify({"error": f"Error updating review: {e}"}), 500

    def delete_review(self, review_id):
        try:
            deleted_review = self.review_service.delete_review(review_id)
            if deleted_review:
                return jsonify(deleted_review), 200
            else:
                return jsonify({"error": "Review not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting review: {e}")
            return jsonify({"error": f"Error deleting review: {e}"}), 500
