from database.database import SQLAlchemy
from src.resources.models.to_do_model import ToDo
from src.resources.models.user_model import User
from flask import abort
from werkzeug.exceptions import NotFound,BadRequest,Unauthorized,InternalServerError
from datetime import datetime,timezone
import uuid


def create_to_do_list(db:SQLAlchemy,data:dict,id:str):
    try:
        list_data = ToDo(
            id = str(uuid.uuid4()),
            userid = id,
            title = data.get("title"),
            description = data.get("description"),
            created_at = datetime.now(tz=timezone.utc),
        )
        db.session.add(list_data)
        db.session.commit()
        db.session.refresh(list_data)
    except Exception:
        raise InternalServerError("A database error!")

def get_all_list(id:str):
    try:
        all_lists= ToDo.query.filter(ToDo.userid==id).all()
        res = []
        for i in all_lists:
            res.append({"title":i.title,"description":i.description})
        return res
    except AttributeError:
        raise BadRequest("Invalid id")
    
def get_one_list(list_id:str,userid:str):
    try:
        
        data = ToDo.query.filter(ToDo.id == list_id).one_or_none()
        if data.userid == userid:
            return data
        else:
            raise NotFound("not found!")
    except AttributeError:
        raise BadRequest("Invalid id")
            
def update_one_list(db:SQLAlchemy,list_id:str , data:dict, userid:str):
    
    try:
        # breakpoint()
        list_data = ToDo.query.filter(ToDo.id==list_id).one()
        if list_data.userid == userid:
            for key ,val in data.items():
                setattr(list_data,key,val)
            list_data.updated_at = datetime.now(tz=timezone.utc)
            db.session.commit()
        else:
            raise Unauthorized("Can't updated other's list!")
    except AttributeError:
        raise BadRequest("Invalid id")


def delete_one_list(db:SQLAlchemy,id:str , userid:str):
    try:
        # breakpoint()
        data = ToDo.query.filter(ToDo.id==id).one_or_none()

        if data.userid!=userid:
            raise Unauthorized("Can't delete other's list!") 
        if data.is_deleted:
            raise NotFound("No list found!")
        else:
            data.is_deleted = True
        db.session.commit()
    except AttributeError:
        raise BadRequest("Invalid id")
    

        




    