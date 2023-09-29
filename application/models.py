from .database import db
from flask_security import UserMixin,RoleMixin
from sqlalchemy import DDL, event


roles_users_table = db.Table('roles_users',
  db.Column('user_id', db.Integer(), 
  db.ForeignKey('users.id')),
  db.Column('role_id', db.Integer(), 
  db.ForeignKey('roles.id')))

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean())

class Roles(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Phase(db.Model):
    __tablename__ = 'phase'
    phaseid = db.Column(db.Integer(),primary_key=True,unique=True,autoincrement=True)
    phase_name = db.Column(db.String(255),unique=True)
    pending = db.Column(db.Integer())
    done = db.Column(db.Integer())
    late = db.Column(db.Integer())

    def __init__(self,name:str,pending:int,done:int,late:int):
        self.phase_name = name
        self.pending=pending
        self.done = done
        self.late = late

    @staticmethod
    def create(name,pending,done,late):
        new_phase = Phase(name,pending,done,late)
        db.session.add(new_phase)
        db.session.commit() 

update_task_state = DDL('''\
CREATE TRIGGER update_task_state UPDATE OF state ON obs
  BEGIN
    UPDATE task SET state = 2 WHERE (obs_id = old.id) and (new.state = 2);
  END;''')
event.listen(User, 'after_update', update_task_state)


class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    title = db.Column(db.String(255))
    deadline = db.Column(db.String(50))
    status = db.Column(db.Integer)
    content = db.Column(db.String)
    phase_name = db.Column(db.String,db.ForeignKey("phase.phase_name"),nullable=False)
    color = db.Column(db.Integer)

    def __init__(self,title:str,deadline:int,status:int,content:str,phase_name:str,color:int):
        self.title = title
        self.deadline=deadline
        self.status = status
        self.content = content
        self.phase_name = phase_name
        self.color = color

    @staticmethod
    def create(title,deadline,status,content,phase_name,color):
        new_card = Card(title,deadline,status,content,phase_name,color)
        db.session.add(new_card)
        db.session.commit() 

    def done(self,color):
        self.color = "green"
        self.status = 1
        db.session.commit()

    def rename(self,name):
        self.title = name
        db.session.commit() 
        
class Position(db.Model):
    __tablename__ = 'position'
    index = db.Column(db.Integer,primary_key = True,autoincrement=True)
    card_id =  db.Column(db.Integer,db.ForeignKey("card.card_id"),nullable=False)
    phase_name = db.Column(db.String,db.ForeignKey("phase.phase_name"),nullable=False)

    def __init__(self, card_id: int,phase_name:str):
        self.card_id = card_id
        self.phase_name= phase_name

    @staticmethod
    def create(card_id,phase_name):  
        new_pos = Position(card_id,phase_name)
        db.session.add(new_pos)
        db.session.commit()


