from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

"""PRODUCTS"""
class ProductSchema(Schema):
    """REQUIRED"""
    id = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)
        
    """VALIDATES"""
    @validates("price")
    def validate_price(self, value):
        if value < 0:
            raise ValidationError("The price must be a non-negative number.")

    @validates("quantity")
    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("The quantity must be greater than zero.")
        
"""ORDERS"""
class OrdersSchema(Schema):
    """REQUIRED"""
    order_id = fields.String(dump_only=True)
    customer_email = fields.Email(required=True)
    products = fields.List(fields.Nested(ProductSchema), required=True)
    total_price = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    """VALIDATES"""
    @validates("products")
    def validate_products(self, value):
        if not value:
            raise ValidationError("The order must include at least one product.")

"""TEST"""
if __name__ == "__main__":
    from orders_APi.logger.logger_orders import Logger

    test_data = {
        "customer_email": "customer@example.com",
        "products": [
            {"id": "1", "name": "Product 1", "price": 10.5, "quantity": 2},
            {"id": "2", "name": "Product 2", "price": 20.0, "quantity": 1}
        ]
    }

    schema = OrdersSchema()
    logger = Logger()

    try:
        validated_data = schema.load(test_data)
        logger.info("All validations passed.")
    except ValidationError as e:
        logger.error(f'An error has ocurred: {e}')
