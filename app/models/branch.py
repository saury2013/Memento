# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import load_only
from sqlalchemy import func

from app.models import db,fragment_tags_table
from app.models.fragment import Fragment


class Branch(db.Model):
    '''分支'''
    __tablename__ = 'branch'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False,default="",index=True)

    first_child = db.Column(db.Integer,nullable=False,default=0)
    next_silbing = db.Column(db.Integer,nullable=False,default=0)
    fragments = db.relationship('Fragment',backref='branch', lazy=True)

    @staticmethod
    def add(name,praent_id=None):
        branch = Branch()
        branch.name = name
        db.session.add(branch)
        db.session.commit()
        if praent_id is not None:
            praent = Branch.query.get(praent_id)
            if praent.first_child == 0:
                praent.first_child = branch.id
            else:
                nearest_brother = Branch.find_last_silbing(praent.first_child)
                nearest_brother.next_silbing = branch.id
            db.session.commit()
        return branch

    @staticmethod
    def find_last_silbing(id):
        '''
        递归查找next_silbing为空的元素
        :param id:
        :return:
        '''
        branch = Branch.query.get(id)
        if branch.next_silbing == 0:
            return branch
        else:
            return Branch.find_last_silbing(branch.next_silbing)

