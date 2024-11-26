from flask import Flask
from flask_cors import CORS

# ORDERS API IMPORTS
from models.models_orders import OrdersModel
from service.services_orders import OrdersService
from schemas.schemas_orders import OrdersSchema
from routes.routes_orders import OrdersRoute

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)  # Init Swagger

db_conn = OrdersModel()
db_conn.connect_to_database()
orders_service = OrdersService(db_conn)
orders_schema = OrdersSchema()
orders_routes = OrdersRoute(orders_service, orders_schema)

app.register_blueprint(orders_routes)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
