from marshmallow import Schema, fields, validates, ValidationError
from logger.logger_categories import Logger

class CategorySchema(Schema):
    """REQUIRED"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)

    """VALIDATES"""
    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Category name cannot be empty.")
        if len(value) < 3:
            raise ValidationError("Category name must have at least 3 characters")
        if len(value) > 50:
            raise ValidationError("Category name must have at most 50 characters")


"""TEST"""
if __name__ == "__main__":
    from logger.logger_categories import Logger
    
    test_data = {
        "name": "Electronics"
    }
    
    schema = CategorySchema()
    logger = Logger()
    
    try:
        validated_data = schema.load(test_data)
        logger.info("All validations passed")
        logger.info(f"Validated data: {validated_data}")
    except ValidationError as e:
        logger.error(f"An error has occurred: {e}")