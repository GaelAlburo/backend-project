from flask import Flask
from models.products_model import ProductModel
from services.products_services import ProductService
from schemas.products_schemas import ProductSchema
from routes.products_routes import ProductRoute
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Swagger
swagger = Swagger(app)

# Model
db_conn = ProductModel()
db_conn.connect_to_database()

# Service
product_service = ProductService(db_conn)

# Schema
product_schema = ProductSchema()

# Routes
product_routes = ProductRoute(product_service, product_schema)

# Register the blueprint to make the routes available in the app
app.register_blueprint(product_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
