from database.database import db
import uuid
from datetime import datetime, timezone
datetime.strptime

class ToDo(db.Model):
    id = db.Column(db.String,primary_key=True,default=str(uuid.uuid4()))
    userid = db.Column(db.String, db.ForeignKey("user.id"),nullable=False)
    title = db.Column(db.String,nullable=True)
    description = db.Column(db.String,nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    updated_at =  db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    remainder = db.Column(db.DateTime, default=None)
    is_deleted = db.Column(db.Boolean, default=False)
    shedule =  db.Column(db.DateTime, default=None)

    