from marshmallow import fields, validates, ValidationError
from re import match


class UserSchema:

    user_email = fields.String(required=True)
    user_password = fields.String(required=True)
    type = fields.String(required=True)

    @validates("user_email")
    def validates_user(self, user_email):
        valid = match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_email)
        if valid == None : 
            raise ValidationError("The email address is not valid. User email must have email format (user_name@domain)")

    @validates("user_password")
    def validates_password(self, user_password):
        # User Password must have at least 8 characters and at most 25 characters
        if len(user_password) < 8:
            raise ValidationError("User password must have at least 8 characters")
        elif len(user_password) > 25:
            raise ValidationError("User password must have at most 25 characters")
        elif not any(char.isdigit() for char in user_password):
            raise ValidationError('Password should have at least one numeral')
        elif not any(char.isupper() for char in user_password):
            raise ValidationError('Password should have at least one uppercase letter')
        elif not any(char.islower() for char in user_password):
            raise ValidationError('Password should have at least one lowercase letter')
        
    @validates("type")
    def validates_type(self, user_type):
        if user_type != 'admin' and user_type != 'client':
            raise ValidationError("The user type is not valid")
