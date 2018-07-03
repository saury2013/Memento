# -*- coding: utf-8 -*-
from flask import make_response, request, jsonify,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
import json
from werkzeug.utils import secure_filename
import os

from app.models.fragment import Fragment
from app.models.branch import Branch
from app.models.tag import Tag
from app.api import api
from app.whoosh import search_helper
from app import base_dir
from app.api.form import SearchForm
from app.main.forms.fragment import CreateFragmentForm

UPLOAD_FOLDER = 'static/resource/uploads/image/'
ALLOWED_EXTENSIONS = set(['bmp', 'webp', 'png', 'jpg', 'jpeg', 'gif'])


@api.route("/delete_tags/", methods=['POST'])
@login_required
def delete_tags():
    response = {"status": 500, "msg": "name is Null!"}
    data = request.form.getlist("data[]")
    if data != "":
        tags_delete_failed = Tag.delete_tags(data)
        if tags_delete_failed:
            response['tags_delete_failed'] = [tag.name for tag in tags_delete_failed]
            response["msg"] = "some tags cannot delete"
        else:
            response["msg"] = "tag has already delete!"
        response["status"] = 200
    return make_response(json.dumps(response))

@api.route("/add_tag/", methods=['POST'])
@login_required
def add_tag():
    # name = request.args.get('name', 0, type=int)
    response = {"status": 500, "msg": "name is Null!"}
    name = request.form['name']
    print(name)
    if name != "":
        tag = Tag.add(name)
        if tag:
            res = {"id": tag.id, "name": tag.name}
            response['tag'] = res
            response["status"] = 200
        else:
            response["msg"] = "tag has already exists!"
        print(response)
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
    print(res)
    data = {}
    data["result"] = res
    return jsonify(data)

@api.route("/search2/",methods=['POST'])
def search2():
    form = SearchForm(request.form)
    results = ""
    keyword = form.keyword.data
    if form.validate_on_submit():
        results = search_helper.search(keyword)
    return render_template("search_result.html",results=results,keyword=keyword)

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

@api.route("/fragment_update/<int:id>", methods=['GET','POST'])
@login_required
def fragment_update(id):
    fragment = Fragment.get_or_404(id)
    form = CreateFragmentForm()
    form.branch.choices = Branch.get_all_choices()
    form.tags.choices = Tag.get_all_chioces()
    if request.method == 'GET':
        form.title.data = fragment.title
        form.body.data = fragment.markdown
    elif request.method == 'POST':
        if form.validate_on_submit():
            fragment.title = form.title.data
            fragment.markdown = form.body.data
            fragment.user_id = current_user.id
            fragment.branch_id = form.branch.data
            tags_id = form.tags.data
            tags = Tag.get_by_ids(tags_id)
            fragment.tags = tags
            fragment.update()
            flash('Edit Saved.', category='success')
            return redirect(url_for("main.home"))

    return render_template("editor.html",form=form,fragment=fragment)