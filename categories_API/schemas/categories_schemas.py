from marshmallow import Schema, fields, validates, ValidationError
from logger.logger_categories import Logger


class CategorySchema(Schema):
    """Class to validate the incoming category data"""

    name = fields.String(required=True)

    @validates("name")
    def validate_name(self, value):
        """Function to validate the name field between 3 and 50 characters"""
        if not value.strip():
            raise ValidationError("Category name cannot be empty.")
        if len(value) < 3:
            raise ValidationError("Category name must have at least 3 characters")
        if len(value) > 50:
            raise ValidationError("Category name must have at most 50 characters")
