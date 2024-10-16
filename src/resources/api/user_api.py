from flask import Blueprint,request
from src.functions.user_functions import *
from database.database import db

user_blueprint = Blueprint("user",__name__)

@user_blueprint.route("/register",methods=["POST"])
def create():
    data = request.get_json()
    user = create_user(db,dict(data))
    return "user created successfully!"

