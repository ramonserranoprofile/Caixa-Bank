from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.jwt_utils import generate_jwt
from app.models import db, User 
from typing import Dict, Tuple, Union, TYPE_CHECKING


def register_user(data: Dict[str, str]) -> Tuple[Dict[str, Union[str, int]], int]:
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    # Validation
    if not all([email, password, name]):
        return {"error": "All fields are required."}, 400

    if not email or not password or not name:
        return {"error": "All fields are required."}, 400

    if not email.strip() or not password.strip() or not name.strip():
        return {"error": "No empty fields allowed."}, 400

    if "@" not in email or "." not in email:
        return {"error": f"Invalid email: {email}"}, 400

    if len(password) < 8:
        return {"error": "Password must be at least 8 characters long."}, 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "Email already exists."}, 400

    # Create new user // # Pylance error ignored because the model attributes are dynamically added
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256") 
    new_user = User(
        email=email, name=name, hashed_password=hashed_password)  # id are automátically generated  and pylance error type: ignore
    
    print(
        f"Creating user with: email={email}, name={name}, hashed_password={hashed_password}"
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"name": name, "email": email}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500


def authenticate_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Bad credentials."}, 401

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": f"User not found for the given email: {email}"}, 400

    # Check password
    if not check_password_hash(user.hashed_password, password):
        return {"error": "Bad credentials."}, 401

    # Generate JWT con el user_id incluido
    user_id= user.id
    # El id generado automáticamente
    token = generate_jwt({"email": email, "user_id": user_id})
    return {"token": token}, 200
