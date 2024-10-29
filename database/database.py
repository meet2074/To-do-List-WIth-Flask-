from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = None  # Store migrate instance

def init_database(app):
    global migrate
    db.init_app(app)
    migrate = Migrate(app, db)

