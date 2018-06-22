# -*- coding: utf-8 -*-
from flask import make_response, request, jsonify
from flask_login import login_required
import json
from werkzeug.utils import secure_filename
import os

from app.models.fragment import Fragment
from app.models.branch import Branch
from app.models.tag import Tag
from app.api import api
from app.whoosh import search_helper
from app import base_dir

UPLOAD_FOLDER = 'static/resource/uploads/image/'
ALLOWED_EXTENSIONS = set(['bmp', 'webp', 'png', 'jpg', 'jpeg', 'gif'])


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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route("/upload_image/",methods=['POST'])
def upload_image():
    result = {
        "success" : 0,
        "message" : "",
        "url"    : ""
    }
    if request.method == "POST":
        print(request.files)
        if 'editormd-image-file' not in request.files:
            result["message"] = "No file part"
            return jsonify(result)
        file = request.files['editormd-image-file']
        if file.filename == '':
            result["message"] = "No selected file"
            return jsonify(result)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(base_dir,UPLOAD_FOLDER,filename)
            file.save(save_path)
            result["success"] = 1
            result["message"] = "Success"
            result["url"] = "/"+ UPLOAD_FOLDER + filename
            return jsonify(result)


