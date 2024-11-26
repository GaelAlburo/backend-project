from ast import alias
from marshmallow import fields, validates, ValidationError


class PaymentSchema:
    """Class to validate the payment data incoming"""

    alias = fields.String(required=True)
    name = fields.String(required=True)
    number = fields.String(required=True)
    month = fields.String(required=True)
    year = fields.String(required=True)
    cvv = fields.String(required=True)

    @validates("alias")
    def validates_alias(self, value):
        """Function to validate the alias field"""

        if len(value) < 4:
            raise ValidationError("Alias must have at least 4 characters")

    @validates("name")
    def validates_name(self, value):
        """Function to validate the name field"""

        if len(value) < 4:
            raise ValidationError("Name must have at least 4 characters")

    @validates("number")
    def validates_number(self, value):
        """Function to validate the number field"""

        if len(value) < 16:
            raise ValidationError("Number must have at least 16 characters")

    @validates("month")
    def validates_month(self, value):
        """Function to validate the month field"""

        if len(value) < 2:
            raise ValidationError("Month must have at least 2 characters")

    @validates("year")
    def validates_year(self, value):
        """Function to validate the year field"""

        if len(value) < 4:
            raise ValidationError("Year must have at least 4 characters")

    @validates("cvv")
    def validates_cvv(self, value):
        """Function to validate the cvv field"""

        if len(value) < 3:
            raise ValidationError("CVV must have at least 3 characters")
