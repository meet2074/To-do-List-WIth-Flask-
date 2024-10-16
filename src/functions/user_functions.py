from database.database import db
from flask_sqlalchemy import SQLAlchemy
from flask import abort,jsonify
from src.app import mail
from src.resources.models.user_model import User,Otp 
from sqlalchemy.exc import IntegrityError
from random import randint
from flask_mail import Message
from src.config import Env
from src.resources.models.user_model import User
import uuid
from datetime import datetime,timedelta,timezone
from src.utils.hash import hash_password,verify_password



def create_user(db: SQLAlchemy, user_data: dict):
    try:
        # breakpoint()
        data = User(
            id=str(uuid.uuid4()),
            first_name=user_data.get("first_name"),
            middle_name=user_data.get("middle_name"),
            last_name=user_data.get("last_name"),
            mobile_number = user_data.get("mobile_number"),
            email = user_data.get("email"),
            password = hash_password(user_data.get("password")),
            created_at = datetime.now(tz=timezone.utc),
            updated_at = datetime.now(tz=timezone.utc),
            is_deleted = True
        )
        
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data )
    
        create_otp(db,user_data.get("email"))
        
        
    except IntegrityError as err:
        raise abort(403)
    except Exception as err:
        return jsonify({"error:",err})
    
def create_otp(db:SQLAlchemy,email:str):
    otp = randint(100000,999999)
    msg = Message(
        subject="Otp",
        sender=Env.MAIL_DEFAULT_SENDER,
        recipients=email,
        body=f"otp - {otp}",
    )
    try:
        mail.send(msg)
        user = User.query.filter(User.email==email).one()
        otp_data = Otp(id = str(uuid.uuid4()),userid=user.id,otp=otp,created_at = datetime.now(tz=timezone.utc))
        db.session.add(otp_data)
        db.session.commit()
        db.session.refresh(otp_data)
    except Exception as err:
        abort(400)


    
        
