from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore
from datetime import datetime

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def get_security_payload(self):
        return {
            'id': self.id,
            'email': self.email
        }

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Kanban List Model
class KanbanList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.title
    

# Kanban Card Model
class KanbanCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255))
    deadline = db.Column(db.DateTime)
    completed: bool = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('kanban_list.id'), nullable=False)

    def __str__(self):
        return self.title
    
    def toJson(self):
        self.deadline: datetime
        date = self.deadline.strftime("%Y-%m-%d")
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'deadline': date,
            'completed': self.completed,
            'list_id': self.list_id
        }