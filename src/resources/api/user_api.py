from flask import Blueprint, request
from src.functions.user_functions.user_functions import *
from sqlalchemy.exc import DatabaseError
from database.database import db
from flask_jwt_extended import jwt_required, get_jwt

user_blueprint = Blueprint("user", __name__)

#-----User-Registration------------------------------
@user_blueprint.route("/register", methods=["POST"])
def create():
    data = request.get_json()
    create_user(db, dict(data))
    create_otp(db, data.get("email"))
    return "Please check for the otp!"


@user_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    payload = get_jwt()
    user = get_user(payload.get("id"))
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number,
        "email": user.email,
    }


@user_blueprint.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    is_verified = verify_otp(db, data.get("otp"), data.get("email"))
    # breakpoint()

    if is_verified:
        access_token = create_access_token(data.get("email"))
        refresh_token = create_refresh_token(data.get("email"))

        return {"access_token": access_token, "refresh_token": refresh_token}
    else:
        return "Incorrect Otp , please try again!"


@user_blueprint.route("/refresh", methods=["GET"])
@jwt_required()
def refresh():
    # breakpoint()
    payload = get_jwt()
    try:
        if payload.get("type") == "refresh_token":
            user = User.query.filter(User.id == payload.get("id")).one()
            token = create_access_token(user.email)
            return {"access_tokekn": token}
        else:
            return "Invalid Token type!"
    except DatabaseError:
        abort(500, "A database error!")


@user_blueprint.route("/update", methods=["PUT"])
@jwt_required()
def update():
    # breakpoint()
    payload = get_jwt()
    data = request.get_json()
    update_user(db, data, payload.get("id"))
    return "Data updated successfully!"


@user_blueprint.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    payload = get_jwt()
    delete_user(db, payload.get("id"))
    return "Deleted Successfully!"


#---------------------user-login--------------------------------#

@user_blueprint.route("/login",methods = ['POST'])
def login():
    data = request.get_json()
    # breakpoint()
    if data.get("email") is None and data.get("password") is None:
        return "Please provide Credentials!"
    if not data.get("email"):
        return "Please enter email-id!"
    if not data.get("password"):
        return "Please enter your password!"
    
    login_result = user_login(data.get("email"),data.get("password"))
    return login_result


