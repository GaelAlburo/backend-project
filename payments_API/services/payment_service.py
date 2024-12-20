from flask import jsonify
from logger.logger_pay import Logger


class PaymentService:
    """Class to handle the payment services"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_payments(self):
        """Function to get all payments from the database"""

        try:
            payments = list(self.db_conn.db.payments.find())
            return payments
        except Exception as e:
            self.logger.error(f"Error fetching all payments from database: {e}")
            return (
                jsonify({"error": f"Error fetching all payments from database: {e}"}),
                500,
            )

    def get_payment_by_id(self, payment_id):
        """Function to get a payment by id from the database"""

        try:
            payment = self.db_conn.db.payments.find_one({"_id": payment_id})
            return payment
        except Exception as e:
            self.logger.error(f"Error fetching payment by id from database: {e}")
            return (
                jsonify({"error": f"Error fetching payment by id from database: {e}"}),
                500,
            )

    def add_payment(self, new_payment):
        """Function to add a payment to the database"""

        try:
            if self.db_conn.db.payments.count_documents({}) == 0:
                new_payment["_id"] = 1
            else:
                max_id = self.db_conn.db.payments.find_one(sort=[("_id", -1)])["_id"]
                next_id = max_id + 1
                new_payment["_id"] = next_id

            self.db_conn.db.payments.insert_one(new_payment)
            return new_payment
        except Exception as e:
            self.logger.error(f"Error adding payment to database: {e}")
            return jsonify({"error": f"Error adding payment to database: {e}"}), 500

    def update_payment(self, payment_id, payment):
        """Function to update a payment in the database"""

        try:
            update_payment = self.get_payment_by_id(payment_id)
            if update_payment:
                updated_payment = self.db_conn.db.payments.update_one(
                    {"_id": payment_id}, {"$set": payment}
                )
                return updated_payment
            else:
                return jsonify({"error": "Payment not found"}), 404
        except Exception as e:
            self.logger.error(f"Error updating payment in database: {e}")
            return jsonify({"error": f"Error updating payment in database: {e}"}), 500

    def delete_payment(self, payment_id):
        """Function to delete a payment from the database"""

        try:
            delete_payment = self.get_payment_by_id(payment_id)
            if delete_payment:
                self.db_conn.db.payments.delete_one({"_id": payment_id})
                return delete_payment
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error deleting payment in database: {e}")
            return jsonify({"error": f"Error deleting payment in database: {e}"}), 500
