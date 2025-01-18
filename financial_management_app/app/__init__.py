from flask import Flask
from app.config import Config
from app.models import db
from app.routes import blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)
    # Migrar la base de datos
    migrate = Migrate(app, db)
    
    # Importar modelos después de inicializar la DB

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    # Importar modelos después de inicializar la DB
    from app.models import User, RecurringExpense
    # Registrar los Blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # if __name__ == "__main__":
    #     app.run(debug=True)

    return app
