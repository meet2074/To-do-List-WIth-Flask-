from flask import Flask
from src.config import Env
from flask_jwt_extended import JWTManager
from database.database import init_database
from src.resources.api.user_api import user_blueprint
from src.mail import mail

app = Flask(__name__)   

app.config["SQLALCHEMY_DATABASE_URI"] = Env.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SERVER'] = Env.MAIL_SERVER
app.config['MAIL_PORT'] = Env.MAIL_PORT  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = Env.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Env.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Env.MAIL_DEFAULT_SENDER
app.config['MAIL_USE_SSL'] = False  

JWTManager(app)

mail.init_app(app)

init_database(app)

app.register_blueprint(user_blueprint)
