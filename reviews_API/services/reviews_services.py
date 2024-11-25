from flask import jsonify
from reviews_API.logger.logger_base import Logger


class ReviewService:
    """Service class to that implements the logic of the CRUD operations for reviews"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_reviews(self):
        """Function to fetch all reviews from the database"""

        try:
            reviews = list(self.db_conn.db.reviews.find())
            return reviews
        except Exception as e:
            self.logger.error(f"Error fetching all reviews from database: {e}")
            return (
                jsonify({"error": f"Error fetching all reviews from database: {e}"}),
                500,
            )

    def get_review_by_id(self, review_id):
        """Function to fetch a review by its id"""

        try:
            review = self.db_conn.db.reviews.find_one({"_id": review_id})
            return review
        except Exception as e:
            self.logger.error(f"Error fetching review by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching review by id from database: {e}"}),
                500,
            )

    def add_review(self, new_review):
        """Function to add a review to the database"""

        try:
            # Gets the highest id
            max_id = self.db_conn.db.reviews.find_one(sort=[("_id", -1)])["_id"]
            next_id = max_id + 1
            new_review["_id"] = next_id

            self.db_conn.db.reviews.insert_one(new_review)
            return new_review
        except Exception as e:
            self.logger.error(f"Error adding review to database: {e}")
            return jsonify({"error": f"Error adding review to database: {e}"}), 500

    def update_review(self, review_id, review):
        """Function that updatse a review in the database by its id"""

        try:
            update_review = self.get_review_by_id(review_id)
            if update_review:
                updated_review = self.db_conn.db.reviews.update_one(
                    {"_id": review_id}, {"$set": review}
                )
                if updated_review.modified_count > 0:
                    return updated_review
                else:
                    return "The review is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating review in database: {e}")
            return jsonify({"error": f"Error updating review in database: {e}"}), 500

    def delete_review(self, review_id):
        """Function to delete a review from the database by its id"""

        try:
            deleted_review = self.get_review_by_id(review_id)
            if deleted_review:
                self.db_conn.db.reviews.delete_one({"_id": review_id})
                return deleted_review
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting review from database: {e}")
            return jsonify({"error": f"Error deleting review from database: {e}"}), 500


if __name__ == "__main__":
    from reviews_API.models.reviews_model import ReviewModel

    logger = Logger()
    db_conn = ReviewModel()
    product_service = ReviewService(db_conn)

    try:
        # Read all products
        db_conn.connect_to_database()
        reviews = product_service.get_all_reviews()
        logger.info(f"Reviews: {reviews}")

        # Read product by id
        review = product_service.get_review_by_id(3)
        logger.info(f"Review fetched by id: {review}")

        # Add product
        # new_review = product_service.add_review(
        #     {
        #         "user": "Robert",
        #         "product": "6",
        #         "review": "This product is bad",
        #         "rating": "2",
        #     }
        # )
        # logger.info(f"New review added: {new_review}")

        # Update product
        updated_review = product_service.update_review(
            4,
            {
                "user": "Simon",
                "product": "1",
                "review": "This product is bad",
                "rating": "2",
            },
        )
        logger.info(f"Review updated: {updated_review}")

        # Delete product
        # deleted_review = product_service.delete_review(5)
        # logger.info(f"Review deleted: {deleted_review}")

    except Exception as e:
        logger.critical(f"Error ocurred: {e}")
    finally:
        db_conn.close_connection()
        logger.info("Connection closed successfully")
