# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,TextField,PasswordField,SelectField,SelectMultipleField
from wtforms.validators import InputRequired,ValidationError,DataRequired

class CreateFragmentForm(FlaskForm):
    title = StringField("title",[InputRequired()])
    branch = SelectField("branch",[DataRequired()],coerce=int)
    tags = SelectMultipleField("tags",[DataRequired()],coerce=int)
    body = TextAreaField("content",[InputRequired()])