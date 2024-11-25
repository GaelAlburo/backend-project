from flask import Flask
from reviews_API.models.reviews_model import ReviewModel
from reviews_API.services.reviews_services import ReviewService
from reviews_API.schemas.reviews_schemas import ReviewSchema
from reviews_API.routes.reviews_routes import ReviewRoute
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# Swagger
swagger = Swagger(app)

# Model
db_conn = ReviewModel()
db_conn.connect_to_database()

# Service
review_service = ReviewService(db_conn)

# Schema
review_schema = ReviewSchema()

# Routes
review_routes = ReviewRoute(review_service, review_schema)

# Register the blueprint to make the routes available in the app
app.register_blueprint(review_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
