# -*- coding: utf-8 -*-
from flask import make_response, request, jsonify
from flask_login import login_required
import json

from app.models.fragment import Fragment
from app.models.branch import Branch
from app.models.tag import Tag
from app.api import api
from app.whoosh import search_helper


@api.route("/add_tag/", methods=['POST'])
@login_required
def add_tag():
    # name = request.args.get('name', 0, type=int)
    response = {"status": 500, "msg": "name is Null!"}
    name = request.form['name']
    if name != "":
        tag = Tag.add(name)
        if tag:
            res = {"id": tag.id, "name": tag.name}
            response['tag'] = res
            response["status"] = 200
        else:
            response["msg"] = "tag has already exists!"
    return make_response(json.dumps(response))


@api.route("/add_branch/", methods=['POST'])
@login_required
def add_branch():
    response = {"status": 500, "msg": "name is Null!"}
    name = request.form['name']
    parent_id = request.form['parent']
    if name != "":
        branch = Branch.add(name, parent_id=parent_id)
        if branch:
            res = {"id": branch.id, "name": branch.name}
            response['branch'] = res
            response["status"] = 200
        else:
            response["msg"] = "branch has already exists!"
    return make_response(json.dumps(response))


@api.route("/search/<string:keyword>")
def search(keyword):
    res = search_helper.search(keyword)
    data = {}
    data["result"] = res
    return jsonify(data)
