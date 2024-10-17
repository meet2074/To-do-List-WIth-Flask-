import os

class Env:
    DATABASE_URI = os.getenv("DATABASE_URI")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER  = os.getenv("MAIL_DEFAULT_SENDER")
    SECRET_KEY = os.getenv("SECRET_KEY")