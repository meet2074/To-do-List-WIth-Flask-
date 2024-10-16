from database.database import db
import uuid
from datetime import datetime, timezone


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    middle_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    mobile_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    is_deleted = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)


class Otp(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    userid = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    otp = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    
    
    
