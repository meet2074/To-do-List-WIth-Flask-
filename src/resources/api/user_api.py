from flask import Blueprint, request
from src.functions.user_functions import *
from database.database import db

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["POST"])
def create():
    data = request.get_json()
    create_user(db, dict(data))
    create_otp(db, data.get("email"))
    return "Please check for the otp!"


@user_blueprint.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    is_verified = verify_otp(db,data.get("otp"), data.get("email"))
    # breakpoint()
    
    if is_verified:
        db.session.commit()
        access_token = create_access_token(data.get("email"))
        refresh_token = create_refresh_token(data.get("email"))

        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return "Incorrect Otp , please try again!"
    

