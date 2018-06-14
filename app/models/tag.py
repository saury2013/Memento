# -*- coding: utf-8 -*-

from app.models import db

class Tag(db.Model):
    '''标签'''
    __tablename__ = 'tag'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False,default="",index=True,unique=True)

    @staticmethod
    def add(name):
        tag = Tag.query.filter_by(name=name).first()
        if tag is not None:
            return
        tag = Tag()
        tag.name = name
        db.session.add(tag)
        db.session.commit()
        return tag

    @staticmethod
    def all():
        return Tag.query.all()
