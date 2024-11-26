from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from logger.logger_pay import Logger

class PaymentRoute(Blueprint):
    def __init__(self, payment_service, payment_schema):
        super().__init__("payment", __name__)
        self.logger = Logger()
        self.payment_service = payment_service
        self.payment_schema = payment_schema
        self.register_routes()

    def register_routes(self):
        self.route("/api/v1/payments", methods=["GET"])(self.get_payments)
        self.route("/api/v1/payments", methods=["POST"])(self.add_payment)
        self.route("/api/v1/payments/<int:payment_id>", methods=["PUT"])(self.update_payment)
        self.route("/api/v1/payments/<int:payment_id>", methods=["DELETE"])(self.delete_payment)
    
    @swag_from(
        {
            "tags": ["payments"],
            "responses": {
                200: {
                    "description": "GET all payments",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "String"},
                                "alias": {"type": "String"},
                                "name": {"type": "String"},
                                "number": {"type": "String"},
                                "month": {"type": "String"},
                                "year": {"type": "String"},
                                "cvv": {"type": "String"},
                            },
                        },
                    },
                }
            },
        }
    )

    def get_payments(self):
        payments = self.payment_service.get_all_payments()
        return jsonify(payments), 200
    
    def fetch_request_data(self):
        """Function to fetch the request data from the request body and validate it with the schema"""

        try:
            request_data = request.json
            if not request_data:
                return jsonify({"error": "Invalid data"}), 400

            id = request_data.get("id")
            alias = request_data.get("alias")
            name = request_data.get("name")
            number = request_data.get("number")
            month = request_data.get("month")
            year = request_data.get("year")
            cvv = request_data.get("cvv")

            try:
                self.review_schema.validates_id(id)
                self.review_schema.validates_alias(alias)
                self.review_schema.validates_name(name)
                self.review_schema.validates_number(number)
                self.review_schema.validates_month(month)
                self.review_schema.validates_year(year)
                self.review_schema.validates_cvv(cvv)
                

            except ValidationError as e:
                self.logger.error(f"Invalid data: {e}")
                return jsonify({"error": f"Invalid data: {e}"}), 400

            return id, alias, name, number, month, year, cvv
        
        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return jsonify({"error": f"Error fetching the request data: {e}"}), 500

    @swag_from(
        {
            "tags": ["payments"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "String"},
                            "alias": {"type": "String"},
                            "name": {"type": "String"},
                            "number": {"type": "String"},
                            "month": {"type": "String"},
                            "year": {"type": "String"},
                            "cvv": {"type": "String"},
                        },
                        "required": ["id", "alias", "name", "number", "month", "year", "cvv"],
                    },
                },
            ],
            "responses": {
                201: {
                    "description": "Card added successfully",
                },
                400: {"description": "Invalid data"},
                500: {"description": "Internal server error"},
            },
        }
    )

    def add_payment(self):
        """Function to add a payment to the database"""
        try:
            id, alias, name, number, month, year, cvv = self.fetch_request_data()
            new_payment = {
                "id": id,
                "alias": alias,
                "name": name,
                "number": number,
                "month": month,
                "year": year,
                "cvv": cvv,
            }
            created_payment = self.payment_service.add_payment(new_payment)
            self.logger.info(f"Payment added: {created_payment}")
            return jsonify(created_payment), 201
        except Exception as e:
            self.logger.error(f"Error adding payment: {e}")
            return jsonify({"error": f"Error adding payment: {e}"}), 500
    
    @swag_from(
        {
            "tags": ["payments"],
            "parameters": [
                {
                    "name": "payment_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                },
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "String"},
                            "alias": {"type": "String"},
                            "name": {"type": "String"},
                            "number": {"type": "String"},
                            "month": {"type": "String"},
                            "year": {"type": "String"},
                            "cvv": {"type": "String"},
                        },
                        "required": ["id", "alias", "name", "number", "month", "year", "cvv"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Payment updated successfully",},
                400: {"description": "Invalid data"},
                404: {"description": "Payment not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def update_payment(self, payment_id):
        try:
            id, alias, name, number, month, year, cvv = self.fetch_request_data()
            updated_payment = {
                "_id": payment_id,
                "id": id,
                "alias": alias,
                "name": name,
                "number": number,
                "month": month,
                "year": year,
                "cvv": cvv,
            }
            updated_payment = self.payment_service.update_payment(updated_payment)
            if updated_payment:
                self.logger.info(f"Payment updated: {updated_payment}")
                return jsonify(updated_payment), 200
            else:
                self.logger.error("Payment not found")
                return jsonify({"error": "Payment not found"}), 404
        except Exception as e:
            self.logger.error(f"Error updating payment: {e}")
            return jsonify({"error": f"Error updating payment: {e}"}), 500
    @swag_from(
        {
            "tags": ["payments"],
            "parameters": [
                {
                    "name": "payment_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {"description": "Payment deleted successfully",},
                404: {"description": "Payment not found"},
                500: {"description": "Internal server error"},
            },
        }
    )
    def delete_payment(self, payment_id):
        try:
            deleted_payment = self.payment_service.delete_payment(payment_id)
            if deleted_payment:
                self.logger.info(f"Payment deleted: {deleted_payment}")
                return jsonify(deleted_payment), 200
            else:
                self.logger.error("Payment not found")
                return jsonify({"error": "Payment not found"}), 404
        except Exception as e:
            self.logger.error(f"Error deleting payment: {e}")
            return jsonify({"error": f"Error deleting payment: {e}"}), 500