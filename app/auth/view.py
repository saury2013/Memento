# -*- coding: utf-8 -*-
from flask_login import current_user,logout_user,login_user
from flask import redirect,render_template,url_for,flash
from app.auth import auth
from app.auth.form import LoginForm
from app.models.user import User

@auth.route("/login/",methods=['GET','POST'])
def login():
    print(current_user.is_authenticated)
    # if current_user.is_authenticated:
    #     return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_name(form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for("main.home"))
        flash("username or password incorrect!")
    form.remember.data = True
    return render_template("login.html",form=form)

@auth.route("/logout/")
def logout():
    return 'bye'