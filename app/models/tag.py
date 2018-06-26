# -*- coding: utf-8 -*-
from sqlalchemy.sql import func
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

    @staticmethod
    def delete_tags(data):
        res = []
        if len(data) > 0:
            tags = db.session.query(Tag).filter(Tag.id.in_(data))# .delete(synchronize_session=False)
            for tag in tags:
                if len(tag.fragments) > 0:
                    res.append(tag)
                else:
                    db.session.delete(tag)
            db.session.commit()
        return res

    @staticmethod
    def get_all_chioces():
        tags = Tag.all()
        return [(tag.id,tag.name) for tag in tags]

    @staticmethod
    def get_by_ids(ids):
        return db.session.query(Tag).filter(Tag.id.in_(ids)).all()

    @staticmethod
    def get_hot_tags(num=10):
        tags = Tag.query.filter().order_by("id").limit(num)
        return db.session.query(Tag).order_by(Tag.id).all()

    @staticmethod
    def get_fragments_by_tagname(name):
        tag = db.session.query(Tag).filter_by(name=name).first()
        return tag.fragments
