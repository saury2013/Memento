# -*- coding: utf-8 -*-
from flask import render_template,request,flash,redirect,url_for,jsonify,make_response
from flask_login import current_user,login_required
from app.main import main
from app.models.branch import Branch
from app.models.fragment import Fragment
from app.models.tag import Tag
from app.models.user import User
from app.main.forms.fragment import CreateFragmentForm
from app.utils.pagination_helper import Pagination

@main.route("/")
def home():
    fragments = Fragment.get_nearest_fragments()
    branchs = Branch.get_nearest_branch()
    tags = Tag.get_hot_tags()
    return render_template('home.html',fragments=fragments,branchs=branchs,tags=tags)

@main.route("/branch")
def branch():
    if not Branch.has_branch_tree():
        Branch.fresh_branch_tree()
    branch_tree = Branch.branch_tree_to_json()
    return render_template("branch.html",branch_tree=branch_tree)

@main.route("/tags")
def tags():
    page = request.args.get('page',1,type=int)
    pagination = Tag.query.order_by(Tag.id.desc()).paginate(page,per_page=12,error_out=False)
    tags = pagination.items
    return render_template("tags.html",tags=tags,pagination=pagination)

@main.route("/mindmap")
def mindmap():
    return render_template("mindmap.html")

@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/create",methods=['GET','POST'])
@login_required
def create():
    form = CreateFragmentForm()
    form.branch.choices = Branch.get_all_choices()
    form.tags.choices = Tag.get_all_chioces()
    fragment = Fragment()
    branch_id = form.branch.data
    if form.validate_on_submit():
        fragment.title = form.title.data
        fragment.markdown = form.body.data
        fragment.user_id = current_user.id
        fragment.branch_id = form.branch.data
        tags_id = form.tags.data
        tags = Tag.get_by_ids(tags_id)
        fragment.tags = tags
        fragment.save()
        flash('Edit Saved.', category='success')
        return redirect(url_for("main.home"))

    form.title.data = fragment.title
    form.body.data = fragment.markdown
    return render_template('editor.html',form=form)

@main.route('/page/<int:id>/')
def page(id):
    fragment = Fragment.get_or_404(id)
    relative_fragments = []
    author_name = 'NoName'
    if fragment:
        author = User.get(fragment.user_id)
        if author:
            author_name = author.username
        branch = Branch.get(fragment.branch_id)
        relative_fragments = Branch.get_fragments_by_branchname(branch.name)
    branchs = Branch.get_nearest_branch(deep=3,me_id=fragment.branch_id)
    return render_template("page.html",fragment=fragment,branchs=branchs,relative_fragments=relative_fragments,author_name=author_name)

@main.route('/result_by_tag/<string:name>/<int:page>')
def result_by_tag(name,page):
    all_fragments = Tag.get_fragments_by_tagname(name)
    count = len(all_fragments)
    PER_PAGE = 1
    fragments = all_fragments[(page-1)*PER_PAGE:page*PER_PAGE]
    pagination = Pagination(page,PER_PAGE,count)
    return render_template("result.html",fragments=fragments,pagination=pagination)

@main.route('/result_by_branch/<string:name>/<int:page>')
def result_by_branch(name,page):
    all_fragments = Branch.get_fragments_by_branchname(name)
    count = len(all_fragments)
    PER_PAGE = 1
    fragments = all_fragments[(page-1)*PER_PAGE:page*PER_PAGE]
    pagination = Pagination(page,PER_PAGE,count)
    return render_template("result.html",fragments=fragments,pagination=pagination)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


@main.route("/test/<int:id>",methods=['GET','POST'])
def test(id):

    # if request.method == "POST":
    #     branch = Branch.add('离散数学',praent_id=1)
    # tree = Branch.branch_tree()
    tree = Branch.sibling(id,sibling=[])
    print(tree)
    return "ok"#jsonify(tree)
