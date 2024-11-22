from marshmallow import fields, validates, ValidationError


class ReviewSchema:
    user = fields.String(required=True)
    product = fields.String(required=True)
    review = fields.String(required=True)
    rating = fields.String(required=True)

    # This validation on user may not be used, since inside login user name is validated
    @validates("user")
    def validates_user(self, value):
        if len(value) < 4:
            raise ValidationError("User must have at least 5 characters")

    @validates("review")
    def validates_review(self, value):
        if len(value) < 10:
            raise ValidationError("Review must have at least 10 characters")
        elif len(value) > 280:
            raise ValidationError("Review must have at most 280 characters")

    @validates("product")
    def validates_product(self, value):
        if int(value) < 1:
            raise ValidationError("Product ID must be greater than 0")

    @validates("rating")
    def validates_rating(self, value):
        if int(value) < 1 or int(value) > 5:
            raise ValidationError("Rating must be between 1 and 5")


if __name__ == "__main__":
    from reviews_API.logger.logger_base import Logger

    logger = Logger()
    schema = ReviewSchema()
    try:
        schema.validates_user("Menta")
        schema.validates_review(
            "This is a review that has more than 10 characters and less than 280 characters"
        )
        schema.validates_product("2")
        schema.validates_rating("5")
        logger.info("All validations passed")
    except ValidationError as e:
        logger.error(f"An error has ocurred: {e}")
