# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import load_only
from sqlalchemy import func
from flask import abort
from markdown import Markdown,markdown
import re

from app.models import db,fragment_tags_table
from app.models.tag import Tag
from app.whoosh import search_helper


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
    brief = db.Column(db.String(300),nullable=False,default="")
    markdown = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    html = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_markdown = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_html = db.deferred(db.Column(LONGTEXT,default="",nullable=False))
    publish_timestamp = db.Column(db.DateTime,default=datetime.now,nullable=False)
    updatetime = db.Column(db.DateTime,default=datetime.now,nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    tags = db.relationship('Tag',secondary=fragment_tags_table,backref=db.backref('fragments'))
    # branch = db.relationship('Branch',back_populates='fragment',uselist=False)
    branch_id = db.Column(db.Integer,db.ForeignKey('branch.id'))
    # branch = db.relationship('Branch',foreign_keys=branch_id)

    def get(self,id):
        return Fragment.query.get(id)

    @staticmethod
    def get_or_404(id):
        fragment = Fragment.query.get(id)
        if fragment:
            return fragment
        abort(404)

    def set_brief(self,html_str):
        str = re.sub(r'</?\w+[^>]*>', '', html_str)
        self.brief = str[:300]

    def save(self):
        self.html = self.markdown2html(self.markdown)
        self.set_brief(self.html)
        db.session.add(self)
        db.session.commit()
        search_helper.add_document(self.title,str(self.id),self.markdown)

    def update(self):
        self.html = self.markdown2html(self.markdown)
        self.set_brief(self.html)
        db.session.add(self)
        db.session.commit()
        search_helper.update_document(self.title, str(self.id), self.markdown)

    def markdown2html(self,content):
        # md = Markdown(['codehilite', 'fenced_code', 'meta', 'tables'])
        # html = md.convert(content)
        html = markdown(content,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
        return html
    @staticmethod
    def get_nearest_fragments(num=5):
        fragments = Fragment.query.filter().order_by(Fragment.updatetime.desc()).limit(num)
        res = []
        from app.models.branch import Branch
        for fragment in fragments:
            fragment.branch = Branch.get(fragment.branch_id)
            res.append(fragment)
        return res



