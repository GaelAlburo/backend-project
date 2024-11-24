from flask import jsonify
from orders_APi.logger.logger_orders import Logger

class OrdersService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    """GET ALL"""
    def get_all_orders(self):
        try:
            orders = list(self.db_conn.db.orders.find())
            return orders
        except Exception as e:
            self.logger.error(f"Error fetching all orders from database: {e}")
            return (
                jsonify({"error": f"Error fetching all orders from database: {e}"}),
                500,
            )

    """GET SEARCH"""
    def get_orders_by_id(self, orders_id):
        try:
            orders = self.db_conn.db.orders.find_one({"_id": orders_id})
            return orders
        except Exception as e:
            self.logger.error(f"Error fetching orders by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching orders by id from database: {e}"}),
                500,
            )

    """POST"""
    def add_order(self, new_order):
        try:
            max_id = self.db_conn.db.orders.find_one(sort=[("_id", -1)])["_id"]
            next_id = max_id + 1
            new_order["_id"] = next_id

            self.db_conn.db.orders.insert_one(new_order)
            return new_order
        except Exception as e:
            self.logger.error(f"Error adding orders to database: {e}")
            return jsonify({"error": f"Error adding orders to database: {e}"}), 500

    """PUT"""
    def update_order(self, orders_id, orders):
        try:
            update_orders = self.get_orders_by_id(orders_id)
            if update_orders:
                updated_orders = self.db_conn.db.orders.update_one(
                    {"_id": orders_id}, {"$set": orders}
                )
                if updated_orders.modified_count > 0:
                    return updated_orders
                else:
                    return "The orders is already up to date"
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error updating orders in database: {e}")
            return jsonify({"error": f"Error updating orders in database: {e}"}), 500

    """PUT DELETE"""
    def delete_order(self, orders_id):
        try:
            deleted_orders = self.get_orders_by_id(orders_id)
            if deleted_orders:
                self.db_conn.db.orders.delete_one({"_id": orders_id})
                return deleted_orders
            else:
                return None

        except Exception as e:
            self.logger.error(f"Error deleting orders from database: {e}")
            return jsonify({"error": f"Error deleting orders from database: {e}"}), 500

"""TEST"""
if __name__ == "__main__":
    from orders_APi.models.models_orders import OrdersModel

    logger = Logger()
    db_conn = OrdersModel()
    product_service = OrdersService(db_conn)

    try:
        # Read all products
        db_conn.connect_to_database()
        orders = product_service.get_all_orders()
        logger.info(f"Orders: {orders}")

        # Read product by id
        orders = product_service.get_orders_by_id()
        logger.info(f"Orders fetched by id: {orders}")

        # Add product
        # new_review = product_service.add_review(
        #     {
        #         "user": "Robert",
        #         "product": "6",
        #         "review": "This product is bad",
        #         "rating": "2",
        #     }
        # )
        # logger.info(f"New review added: {new_review}")

        deleted_orders = product_service.delete_orders(2)
        logger.info(f"Orders deleted: {deleted_orders}")

    except Exception as e:
        logger.critical(f"Error ocurred: {e}")
    finally:
        db_conn.close_connection()
        logger.info("Connection closed successfully")
