from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt
from database.database import db
from datetime import datetime
from src.functions.to_do_list_functions.to_do_basic import *
from src.functions.to_do_list_functions.reminder import *


to_do_blueprint = Blueprint("to_do",__name__)

@to_do_blueprint.route("/to-do/create",methods = ["POST"])
@jwt_required()
def create():
    data = request.get_json()
    payload = get_jwt()
    
    create_to_do_list(db,data,payload.get("id"))
    return "list created!"

@to_do_blueprint.route("/to-do/all",methods = ["GET"])
@jwt_required()
def get_all():
    payload = get_jwt()
    data = get_all_list(payload.get("id"))

    return jsonify(data)

@to_do_blueprint.route("/to-do/<string:id>",methods = ["GET"])
@jwt_required()
def get_one(id):
    breakpoint()
    payload = get_jwt()
    data = get_one_list(id,payload.get("id"))
    return {
        "title":data.title,
        "description":data.description
    }
    
@to_do_blueprint.route("/to-do/<string:id>",methods = ["PUT"])
@jwt_required()
def update(id):
    payload = get_jwt()
    data = request.get_json()
    update_one_list(db,id,data,payload.get("id"))
    return "Updated!"

@to_do_blueprint.route("/to-do/<string:id>",methods = ["DELETE"])
@jwt_required()
def delete(id):
    payload = get_jwt()
    delete_one_list(db,id,payload.get("id"))
    return "Deleted!"

@to_do_blueprint.route("/to-do/<string:id>/set-remainder",methods = ["POST"])
@jwt_required()
def remainder(id):
    data = request.json
    request_time = data["reminder"]
    payload = get_jwt()
    userid = payload.get("id")
    time = datetime.strptime(request_time,'%Y-%m-%d %H:%M:%S.%f')
    add_reminder(db,time,id,userid) 
    return "Reminder added succesfully!"   


    

    
    

    
    

    
