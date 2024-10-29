from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timezone
from flask_mail  import Message
from src.mail import mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from src.resources.api.to_do_api import ToDo
from src.resources.api.user_api import User
from werkzeug.exceptions import Forbidden,Conflict
import atexit 
import asyncio

scheduler = BackgroundScheduler()

def add_reminder(db:SQLAlchemy, time ,id:str,userid:str):
    data = ToDo.query.filter(ToDo.id == id).one()
    
    if data.userid == userid:
        if data.reminder is None:
            data.reminder = time
            db.session.commit()
        else:
            raise Conflict("A reminder already exist")
    else:
        raise Forbidden("Not allwoed to set timer on other's list!")\

def one_time_reminder(title):
    
    print(f"reminder about {title}")
    
    # msg = Message("Reminder Notification", recipients=[email])
    # msg.body = f"Remider about your: {title}"

    # mail.send(msg) 
    # print("sent")

def reminder():
    reminder_data = ToDo.query.all()
    for i in reminder_data:
        r_time = i.remainder
        title = i.title
        scheduler.add_job(func=one_time_reminder, trigger=DateTrigger(run_date=r_time),args=[title])
    scheduler.start()     

# atexit.register(lambda: scheduler.shutdown())


    
    

        

        


            
                        
        
            
            
    

