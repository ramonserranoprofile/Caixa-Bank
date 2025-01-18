import jwt
import datetime
from functools import wraps
from flask import current_app, request, jsonify


def generate_jwt(payload):
    payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def verify_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = token.split(" ")[1]  # Eliminar el prefijo "Bearer "
            decoded = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            if "user_id" not in decoded:
                return jsonify({"error": "Invalid token: user_id missing"}), 400
            request.user_id = decoded["user_id"]  # Agregar `user_id` al request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return func(*args, **kwargs)
    return wrapper        
