# -*- coding: utf-8 -*-
from app.main import main

@main.route("/")
def index():
    return 'hex'