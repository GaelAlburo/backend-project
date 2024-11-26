from marshmallow import fields, validates, ValidationError
import re


class ProductSchema:
    """Schema class for the product API to validate the data"""

    name = fields.String(required=True)
    price = fields.String(required=True)
    category = fields.String(required=True)

    @validates("name")
    def validate_name(self, value):
        """Function to validate the name of a product"""
        if len(value) < 4:
            raise ValidationError(
                "The name of the product must have at least 4 characters."
            )

    @validates("price")
    def validate_price(self, value):
        """Function to validate the price of a product"""

        cleaned_value = re.sub(r"[^\d.]", "", value)
        cleaned_value = cleaned_value.replace(",", "")

        if float(cleaned_value) < 0:
            raise ValidationError("The price must be a non-negative number.")

    @validates("category")
    def validate_category(self, value):
        """Function to validate the category of a product"""
        if len(value) < 3:
            raise ValidationError(
                "The category of the product must have at least 3 characters."
            )
