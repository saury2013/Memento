# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
# import app.models.fragment
# import app.models.tag
# import app.models.branch
# import app.models.user

db = SQLAlchemy()

# fragment&tag middle table
fragment_tags_table = db.Table('fragment_tags',
    db.Column('fragment_id',db.Integer,db.ForeignKey('fragment.id'),primary_key=True),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'),primary_key=True),
)