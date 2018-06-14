# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from app.models import db

class User(db.Model,UserMixin):
    '''user table'''
    __tablename__ = "user"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    username = db.Column(db.String(255),unique=True,nullable=False,index=True,default="")
    nickname = db.Column(db.String(255),nullable=False,default="")
    password = db.Column(db.String(255),nullable=False)
    avatar = db.Column(db.String(255),default="")
    updatetime = db.Column(db.DateTime,default=datetime.now,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.now,nullable=False)

    @staticmethod
    def add(username,password):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return
        user = User()
        user.username = username
        user.nickname = username
        user.password = generate_password_hash(password)
        user.avatar = "/static/avatar/avatar.jpg"
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_by_name(username):
        return User.query.filter_by(username=username).first()

    def set_nickname(self,nickname):
        self.nickname = nickname

    def change_password(self,password):
        self.password = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password,password)



