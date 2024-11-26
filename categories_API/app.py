from flask import Flask
from models.categories_models import CategoryModel
from services.categories_services import CategoryService
from schemas.categories_schemas import CategorySchema
from routes.categories_routes import CategoryRoute
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Swagger
swagger = Swagger(app)

# Model
db_conn = CategoryModel()
db_conn.connect_to_database()

# Service
category_service = CategoryService(db_conn)

# Schema
category_schema = CategorySchema()

# Routes
category_routes = CategoryRoute(category_service, category_schema)

# Register the blueprint to make the routes available in the app
app.register_blueprint(category_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()


