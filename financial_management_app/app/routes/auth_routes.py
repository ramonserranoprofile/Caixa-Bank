from flask import Blueprint, request, jsonify, escape
from app.services.auth_service import register_user, authenticate_user
from app.utils.jwt_utils import verify_jwt
auth_bp = Blueprint("auth", __name__)
from werkzeug.security import generate_password_hash
from app.models import db, User


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    else:
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")

    # Validar datos básicos
    if not email or not password or not name:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Buscar si el usuario ya existe
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return (
            jsonify(
                {
                    "error": "Email already registered.",
                    "message": "Please, Login.",
                }
            ),
            409,
        )  # Código de conflicto

    # Crear nuevo usuario
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully. You can now log in."}), 201  


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status_code = authenticate_user(data)
    response = {key: escape(str(value)) for key, value in response.items()}
    sanitized_response = {key: escape(str(value)) for key, value in response.items()}
    if status_code == 200:
        sanitized_response["message"] = escape("Login successful")
        return jsonify(sanitized_response), status_code
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/protected", methods=["GET"])
@verify_jwt
def protected():
    return jsonify({"message": "This is a protected route!"}), 200