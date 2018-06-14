# -*- coding: utf-8 -*-
from flask import render_template,request
from app.main import main
from app.models.branch import Branch

@main.route("/")
def home():
    return render_template('home.html')

@main.route("/home")
def home2():
    return

@main.route("/index")
def index():
    return

@main.route("/tags")
def tags():
    return

@main.route("/search")
def search():
    return

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/create")
def create():
    return

@main.route("/test",methods=['GET','POST'])
def test():
    if request.method == "POST":
        branch = Branch.add('离散数学',praent_id=1)
        print(branch.id)
    return render_template("test_data.html")