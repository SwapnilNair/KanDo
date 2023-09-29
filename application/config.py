import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir, "../db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "data.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "23kjnsa39asd57asdjn"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'toinfinityandbeyond'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('username','email')

