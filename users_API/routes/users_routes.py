from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flasgger import swag_from
from logger.logger_base import Logger
import hashlib


class UserRoute(Blueprint):

    def __init__(self, user_service, users_schema):
        super().__init__("user", __name__)
        self.logger = Logger()
        self.user_service = user_service
        self.users_schema = users_schema
        self.register_routes()

    def register_routes(self):

        self.route("/api/v1/users", methods=["GET"])(self.get_users)
        self.route("/api/v1/is-users", methods=["POST"])(self.is_user)
        self.route("/api/v1/users", methods=["POST"])(self.create_user)
        self.route("/api/v1/users/<int:user_id>", methods=["PUT"])(self.update_user_info)
        self.route("/api/v1/users/<int:user_id>", methods=["DELETE"])(self.delete_user)
        self.route("/healthcheck", methods=["GET"])(self.healthcheck)

    # Swagger documentation for the GET request to /api/v1/users
    @swag_from(
        {
            "tags": ["users"],
            "responses": {
                200: {
                    "description": "Get all registered users",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "_id": {
                                    "type": "number"
                                },
                                'email': {
                                    'type': 'string'
                                },
                                'password': {
                                    'type': 'string'
                                },
                                'status': {
                                    'type': 'string'
                                },
                                'type':{
                                    'type': 'string'
                                }
                            },
                        },
                    },
                }
            },
        }
    )
    def get_users(self):
        users = self.user_service.get_all_users()
        return jsonify(users), 200
    

    def fetch_request_data(self):

        try:
            request_data = request.json
            if not request_data:
                return 500, jsonify({
                    "status": "error",
                    "message": "Invalid data format, Json body is required"
                    }), None, None, None
            
            user_email = request_data.get("email")
            if not user_email:
                self.logger.error(f"Error: email param is required")
                return 500, "email param is required", None, None, None
            
            user_password = request_data.get("password")
            if not user_password:
                self.logger.error(f"Error: password param is required")
                return 500, "password param is required", None, None, None
            
            user_type = request_data.get("type")
            if not user_type:
                self.logger.error(f"Error: type param is required")
                return 500, "type param is required", None, None, None
            
            try:
                self.users_schema.validates_user(user_email)
                self.users_schema.validates_password(user_password)
                self.users_schema.validates_type(user_type)
            except ValidationError as e:
                self.logger.error(f"Invalid user data: {e}")
                return 400, f"Invalid user data: {e}", None, None, None

            return 200, None, user_email, user_password, user_type
        
        except Exception as e:
            self.logger.error(f"Error fetching the request data: {e}")
            return 500, f"Error fetching the request data: {e}", None, None, None
    
    # Swagger documentation for the POST request to /api/v1/is-user
    @swag_from(
        {
            "tags": ["users"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "password": {"type": "string"},
                            "type": {"type": "string"},
                        },
                        "required": ["email", "password", "type"]
                    },
                }
            ],
            "responses": {
                200: {
                    "description": "Entered user info was correctly",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"}
                        }
                    }
                },
                400: {
                    "description": "Invalid data",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                500: {
                    "description": "Internal server error",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
            },
        }
    )
    def is_user(self):
        try:
            code, message, user_email, user_password, user_type = self.fetch_request_data()
            
            if code != 200: 
                self.logger.error(f"Error: {message}")
                return jsonify({"Error": f"{message}"}), code

            # Create a SHA-256 hash object
            hash_object = hashlib.sha256()
            # Convert the password to bytes and hash it
            hash_object.update(user_password.encode())
            # Get the hex digest of the hash
            hash_password = hash_object.hexdigest()

            user = {
                "email": user_email,
                "password": hash_password,
                "type": user_type,
                "status": "active"
            }

            user = self.user_service.get_users_by_user_email(user_email)

            if user == None:
                self.logger.error("Error: No user with the entered data was found.")
                return jsonify({"Error":"No user with the entered data was found."}), 500
            if user['password'] != hash_password:
                self.logger.error("Error: Please verify the data entered (email and password)")
                return jsonify({"Error":"Please verify the data entered (email and password)."}), 500

            self.logger.info(f"Login user: {user}")
            return jsonify({"status": "success"}), 201

        except Exception as e:
            self.logger.error(f"Error creating new user: {e}")
            return jsonify({"error": f"Error creating new user: {e}"}), 500

    # Swagger documentation for the POST request to /api/v1/user
    @swag_from(
        {
            "tags": ["users"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "password": {"type": "string"},
                            "type": {"type": "string"},
                        },
                        "required": ["email", "password", "type"]
                    },
                }
            ],
            "responses": {
                201: {
                    "description": "New user was created correctly",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "New User created": {"type": "object",
                                                 "properties":{
                                                    "_id": {"type": "integer"},
                                                    "email": {"type": "string"},
                                                    "password": {"type": "string"},
                                                    "status": {"type": "string"},
                                                    "type": {"type": "string"},
                                                 }}
                        }
                    }
                },
                400: {
                    "description": "Invalid data",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                500: {
                    "description": "Internal server error",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
            },
        }
    )
    def create_user(self):

        try:
            code, message, user_email, user_password, user_type = self.fetch_request_data()
            
            if code != 200: 
                self.logger.error(f"Error creating new user: {message}")
                return jsonify({"error": f"Error creating new user: {message}"}), code

            # Create a SHA-256 hash object
            hash_object = hashlib.sha256()
            # Convert the password to bytes and hash it
            hash_object.update(user_password.encode())
            # Get the hex digest of the hash
            hash_password = hash_object.hexdigest()

            new_user = {
                "email": user_email,
                "password": hash_password,
                "type": user_type,
                "status": "active"
            }

            response, code = self.user_service.create_new_user(new_user)
            
            if code != 201:
                return jsonify({"error": f"Error creating new user: {response}"}), code

            response['password'] = user_password
            self.logger.info(f"New User created: {response}")
            return jsonify({"New User created": response}), 201

        except Exception as e:
            self.logger.error(f"Error creating new user: {e}")
            return jsonify({"error": f"Error creating new user: {e}"}), 500

    # Swagger documentation for the PUT request to /api/v1/user
    @swag_from(
        {
            "tags": ["users"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "password": {"type": "string"},
                            "type": {"type": "string"},
                        },
                        "required": ["email", "password", "type"]
                    },
                },
                {
                    "name": "user_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {
                    "description": "Updated user info correctly",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "User updated": {"type": "object",
                                                 "properties":{
                                                    "_id": {"type": "integer"},
                                                    "email": {"type": "string"},
                                                    "password": {"type": "string"},
                                                    "type": {"type": "string"},
                                                 }}
                        }
                    }
                },
                400: {
                    "description": "Invalid data",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                404: {
                    "description": "User not found",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                500: {
                    "description": "Internal server error",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
            },
        }
    )
    def update_user_info(self, user_id):

        try:
            code, message, user_email, user_password, user_type = self.fetch_request_data()

            if code != 200: 
                self.logger.error(f"Error updating user: {message}")
                return jsonify({"error": f"Error updating user: {message}"}), code
            
            # Create a SHA-256 hash object
            hash_object = hashlib.sha256()
            # Convert the password to bytes and hash it
            hash_object.update(user_password.encode())
            # Get the hex digest of the hash
            hash_password = hash_object.hexdigest()

            update_user = {
                "_id": user_id,
                "email": user_email,
                "password": hash_password,
                "type": user_type,
            }

            updated_user = self.user_service.update_user(user_id, update_user)
            if updated_user:
                update_user['password'] = user_password
                self.logger.info(f"User updated: {update_user}")
                return jsonify({"User updated": update_user}), 200
            else:
                self.logger.error("User not found")
                return jsonify({"error": "User not found"}), 404

        except Exception as e:
            self.logger.error(f"Error updating review: {e}")
            return jsonify({"error": f"Error updating review: {e}"}), 500


    # Swagger documentation for the DELETE request to /api/v1/user
    @swag_from(
        {
            "tags": ["users"],
            "parameters": [
                {
                    "name": "user_id",
                    "in": "path",
                    "required": True,
                    "type": "integer",
                }
            ],
            "responses": {
                200: {
                    "description": "Deleted user info correctly",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "User deleted": {"type": "object",
                                                 "properties":{
                                                    "_id": {"type": "integer"},
                                                    "email": {"type": "string"},
                                                    "password": {"type": "string"},
                                                    "type": {"type": "string"},
                                                 }}
                        }
                    }
                },
                400: {
                    "description": "Invalid data",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                404: {
                    "description": "User not found",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
                500: {
                    "description": "Internal server error",
                    "schema":{
                        "type": "object",
                        "properties": {
                            "Error": {"type": "string"}
                        }
                    }
                },
            },
        }
    )
    def delete_user(self, user_id):

        try:
            deleted_user = self.user_service.delete_user(user_id)
            if deleted_user:
                self.logger.info(f"User deleted: {deleted_user}")
                return jsonify({"User deleted": deleted_user}), 200
            else:
                self.logger.error("User not found")
                return jsonify({"error": "User not found"}), 404

        except Exception as e:
            self.logger.error(f"Error deleting user: {e}")
            return jsonify({"error": f"Error deleting user: {e}"}), 500


    def healthcheck(self):
        """Function to check the health of the docker container"""

        return jsonify({"status": "Up"}), 200
