from database.database import SQLAlchemy
from src.resources.models.to_do_model import ToDo
from src.resources.models.user_model import User
from flask import abort
from werkzeug.exceptions import NotFound,BadRequest
from sqlalchemy.exc import NoResultFound
from datetime import datetime,timezone,timedelta
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
        abort(500,"An unknwond error!")

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
            abort()
    # except Exception:
    #     abort(401,"Can not update other's list!")
    except NoResultFound:
        abort(404,"No list Found!")


def delete_one_list(db:SQLAlchemy,id:str , userid:str):
    try:
        data = ToDo.query.filter(ToDo.id==id).one()

        if data.userid!=userid:
            abort(500,"Can't delete other's list!") 
        if data.is_deleted:
            abort(404,"No list found!")
        else:
            data.is_deleted = True
    except Exception:
        abort(500,"An Unknown Error!")

        




    