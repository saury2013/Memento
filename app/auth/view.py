# -*- coding: utf-8 -*-
from app.auth import auth

@auth.route("/login/",methods=['GET','POST'])
def login():
    return 'hello'