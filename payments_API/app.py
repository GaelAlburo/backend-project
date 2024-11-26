from flask import Flask, app
from models.payment_model import PaymentModel
from services.payment_service import PaymentService
from schemas.payment_schema import PaymentSchema
from routes.payment_route import PaymentRoute
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)

db_conn = PaymentModel()
db_conn.connect_to_database()

payment_service = PaymentService(db_conn)

payment_schema = PaymentSchema()

payment_routes = PaymentRoute(payment_service, payment_schema)

app.register_blueprint(payment_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
