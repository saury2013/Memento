# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import load_only
from sqlalchemy import func
from flask import abort

from app.models import db,fragment_tags_table


class Fragment(db.Model):
    '''知识碎片'''
    __tablename__ = 'fragment'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    title = db.Column(db.String(255),nullable=False,default="",index=True)
    access = db.Column(db.Integer,nullable=False,default=1)
    status = db.Column(db.Integer,nullable=False,default=0)
    markdown = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    html = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_markdown = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_html = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_timestamp = db.Column(db.DateTime,default=datetime.now,nullable=False)
    updatetime = db.Column(db.DateTime,default=datetime.now,nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # tags = db.relationship('Tag',secondary=fragment_tags_table,backref=db.backref('fragments'))
    # branch = db.relationship('Branch',back_populates='fragment',uselist=False)
    branch_id = db.Column(db.Integer,db.ForeignKey('branch.id'))
    # branch = db.relationship('Branch',foreign_keys=branch_id)

    def get(self,id):
        return Fragment.query.get(id)

    def get_or_404(self,id):
        fragment = Fragment.query.get(id)
        if fragment:
            return fragment
        abort(404)

