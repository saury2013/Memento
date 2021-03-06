# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired("username cannot be empty!")])
    password = PasswordField("password",validators=[DataRequired("password cannot be empty!")])
    remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
    username = StringField("username",validators=[DataRequired("username cannot be empty!")])
    password = PasswordField("password", validators=[DataRequired("password cannot be empty!")])
    password2 = PasswordField("confirm password", validators=[DataRequired("password2 cannot be empty!")])