# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class SearchForm(FlaskForm):
    keyword = StringField("username",validators=[InputRequired("keyword cannot be empty!")])