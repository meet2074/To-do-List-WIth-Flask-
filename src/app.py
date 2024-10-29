from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from src.config import Env
from datetime import datetime
from src.functions.to_do_list_functions.reminder import reminder , scheduler
import asyncio
from flask_jwt_extended import JWTManager
from database.database import init_database
from src.resources.api.user_api import user_blueprint
from src.resources.api.to_do_api import to_do_blueprint 
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
app.config["JWT_SECRET_KEY"] = Env.SECRET_KEY

JWTManager(app)

with app.app_context():
    mail.init_app(app)
    
init_database(app)
app.register_blueprint(user_blueprint)
app.register_blueprint(to_do_blueprint)

with app.app_context():
    reminder()

# with app.app_context():
    
