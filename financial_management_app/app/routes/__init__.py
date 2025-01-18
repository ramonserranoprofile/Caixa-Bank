from flask import Blueprint
from app.routes.auth_routes import auth_bp
from app.routes.recurring_expenses_routes import recurring_expenses_bp

# Lista de blueprints
blueprints = [auth_bp, recurring_expenses_bp]

# Exportar los blueprints para que puedan registrarse en la app principal
__all__ = ["blueprints"]
