from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from orders_APi.logger.logger_orders import Logger

class OrdersRoute(Blueprint):
    def __init__(self, orders_service, orders_schema):
        super().__init__("orders", __name__)
        self.logger = Logger()
        self.orders_service = orders_service
        self.orders_schema = orders_schema
        self.register_routes()

    """ROUTES"""
    def register_routes(self):
        self.route("/api/v1/orders", methods=["GET"])(self.get_orders)
        self.route("/api/v1/orders", methods=["POST"])(self.add_order)
        self.route("/api/v1/orders/<int:order_id>", methods=["PUT"])(self.update_order)
        self.route("/api/v1/orders/<int:order_id>", methods=["DELETE"])(self.delete_order)
    
    """GET"""
    def get_orders(self):
        try:
            orders = self.orders_service.get_all_orders()
            return jsonify(orders), 200
        except Exception as e:
            self.logger.error(f"Error fetching all orders: {e}")
            return jsonify({"error": f"Error fetching all orders: {e}"}), 500
        
    """POST"""
    def add_order(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            validated_data = self.orders_schema.load(request_data)
            created_order = self.orders_service.add_order(validated_data)
            self.logger.info(f"Order added: {created_order}")
            return jsonify(created_order), 201
        
        except ValidationError as e:
            self.logger.error(f"Validation error: {e.messages}")
            return jsonify({"error": e.messages}), 400
        
        except Exception as e:
            self.logger.error(f"Error adding order: {e}")
            return jsonify({"error": f"Error adding order: {e}"}), 500

    """PUT"""
    def update_order(self, order_id):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            validated_data = self.orders_schema.load(request_data)
            updated_order = self.orders_service.update_order(order_id, validated_data)
            if updated_order:
                self.logger.info(f"Order updated: {updated_order}")
                return jsonify(updated_order), 200
            else:
                return jsonify({"error": "Order not found"}), 404

        except ValidationError as e:
            self.logger.error(f"Validation error: {e.messages}")
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            self.logger.error(f"Error updating order: {e}")
            return jsonify({"error": f"Error updating order: {e}"}), 500
    
    """PUT DELETE"""
    def delete_order(self, order_id):
        try:
            deleted_order = self.orders_service.delete_order(order_id)
            if deleted_order:
                self.logger.info(f"Order deleted: {deleted_order}")
                return jsonify(deleted_order), 200
            else:
                return jsonify({"error": "Order not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting order: {e}")
            return jsonify({"error": f"Error deleting order: {e}"}), 500