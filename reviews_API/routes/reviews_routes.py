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
        # self.route("/api/v1/reviews", methods=["POST"])(self.add_review)

    def get_reviews(self):
        reviews = self.review_service.get_all_reviews()
        return jsonify(reviews), 200
