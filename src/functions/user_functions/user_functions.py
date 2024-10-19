from flask_sqlalchemy import SQLAlchemy
from flask import abort, jsonify
from jose import jwt
from src.mail import mail
from src.utils.hash import verify_password
from src.resources.models.user_model import User, Otp
from sqlalchemy.exc import IntegrityError,NoResultFound,DatabaseError
from random import randint
from flask_mail import Message
from src.config import Env
from src.resources.models.user_model import User
import uuid
from datetime import datetime, timedelta, timezone
from src.utils.hash import hash_password, verify_password

otp_exp_min = 30
access_token_exp_min = 30
refresh_token_exp_days = 7
algo = "HS256"

#--------------user_registration---------------------------#

def create_user(db: SQLAlchemy, user_data: dict):
    try:
        data = User(
            id=str(uuid.uuid4()),
            first_name=user_data.get("first_name"),
            middle_name=user_data.get("middle_name"),
            last_name=user_data.get("last_name"),
            mobile_number=user_data.get("mobile_number"),
            email=user_data.get("email"),
            password=hash_password(user_data.get("password")),
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
            is_deleted=True,
        )

        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)


    except IntegrityError as err:
        raise abort(403,"Data already exist!")
    except DatabaseError as err:
        raise abort(500,"Database Error!")
    
    
def get_user(id:str):
    try:
        user = User.query.filter(User.id==id).one()
        return user
    except Exception:
        abort(500,"A database Error!")

def create_otp(db: SQLAlchemy, email: str):
    otp = randint(100000, 999999)

    try:
        user = User.query.filter(User.email == email).one()
        otp_data = Otp(
            id=str(uuid.uuid4()),
            userid=user.id,
            otp=otp,
            created_at=datetime.now(tz=timezone.utc),
        )
        db.session.add(otp_data)
        db.session.commit()
        db.session.refresh(otp_data)
        
        msg = Message(
            subject="Otp",
            sender=Env.MAIL_DEFAULT_SENDER,
            recipients=[email],
            body=f"otp - {otp}",
        )
        mail.send(msg)
    except NoResultFound as err:
        abort(404,"Not Found!")


def verify_otp(db:SQLAlchemy,otp: int, email: str):
    try:
        user = User.query.filter(User.email == email).one()
        db_otp = Otp.query.filter(Otp.userid == user.id).one()
        
        current_time = datetime.now()
        otp_expiration_time = db_otp.created_at + timedelta(minutes=otp_exp_min)
        
        if db_otp.otp == otp:
            if current_time<otp_expiration_time:
                Otp.query.filter(Otp.otp == otp).delete()
                user.is_deleted= False
                user.is_active = True
                db.session.commit()
                return True
            else:
                return False
        return False
    except NoResultFound:
        abort(404,"NO such otp!")

def create_access_token(email:str):
    try:
        # breakpoint()
        user = User.query.filter(User.email==email).one()
        access_token_exp_time = datetime.now(tz=timezone.utc) + timedelta(hours=access_token_exp_min)
        
        payload = {"id":user.id,"name":user.first_name,"sub":"user","type":"access_token","exp":access_token_exp_time}

        token = jwt.encode(payload,key=Env.SECRET_KEY,algorithm=algo)
        return token
    except Exception:
        abort(500)

def create_refresh_token(email:str):
    try:
        user = User.query.filter(User.email==email).one()
        refresh_token_exp_time = datetime.now(tz=timezone.utc) + timedelta(days=refresh_token_exp_days)
        
        payload = {"id":user.id,"name":user.first_name,"sub":"user","type":"refresh_token","exp":refresh_token_exp_time}

        token = jwt.encode(payload,key=Env.SECRET_KEY,algorithm=algo)
        return token
    except Exception:
        abort(500)


def update_user(db:SQLAlchemy,data:dict,id:str):
    try:
        user = User.query.filter(User.id==id).one()
        for key, val in data.items():
            setattr(user, key, val)
        user.updated_at = datetime.now()
        db.session.commit()
    except Exception :
        abort(500,"A database error!")

def delete_user(db:SQLAlchemy, id:str):
    try:
        user = User.query.filter(User.id == id ).one()
        user.is_deleted = True
        db.session.commit()
    except Exception :
        abort(500,"A database error!")
        

#--------------------------------user_login------------------------------------#

def user_login(email:str,password:str):
    try:
        user = User.query.filter(User.email==email).one_or_none()
        # breakpoint()
        if not user or user.is_deleted:
            return "No user with such email id."
        
        verified = verify_password(password,user.password)
        if verified:
            access_token = create_access_token(email)
            refresh_token = create_refresh_token(email)

            return {"access_token":access_token,"refresh_token":refresh_token}
        else:
            return "Incorrect Password!"
    except Exception:
        abort(500,"A database error!")
        
    
    

      
    

    