from flask import Flask
from application import config
from application.config import Config
from application.database import db
from flask_security import Security,SQLAlchemySessionUserDatastore,SQLAlchemyUserDatastore
from application.models import User,Roles


app = Flask(__name__,template_folder="templates")  

app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

user_datastore = SQLAlchemySessionUserDatastore(db.session,User,Roles) 
security = Security(app,user_datastore)

from application.controllers import *

@app.errorhandler(404)
def pnf(x):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080)
