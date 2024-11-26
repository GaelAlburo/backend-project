from flask import Flask
from models.users_model import UserModel
from services.users_services import UserService
from schemas.users_schemas import UserSchema
from routes.users_routes import UserRoute
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Swagger
swagger = Swagger(app)

# Model
db_conn = UserModel()
db_conn.connect_to_database()

# Service
user_service = UserService(db_conn)
# Schema
user_schema = UserSchema()
# Routes
user_routes = UserRoute(user_service, user_schema)

# Register the blueprint to make the routes available in the app
app.register_blueprint(user_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
