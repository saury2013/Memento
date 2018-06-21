# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import load_only
from sqlalchemy import func
from sqlalchemy import event
import json
import os

from app.models import db,fragment_tags_table
from app.models.fragment import Fragment
from app import base_dir


class Branch(db.Model):
    '''分支'''
    __tablename__ = 'branch'
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    id = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False,default="",index=True)

    first_child = db.Column(db.Integer,nullable=False,default=0)
    next_sibling = db.Column(db.Integer,nullable=False,default=0)
    fragments = db.relationship('Fragment',backref='branch', lazy=True)

    @staticmethod
    def add(name,parent_id=None):
        branch = Branch()
        branch.name = name
        db.session.add(branch)
        db.session.commit()
        if parent_id is not None:
            praent = Branch.query.get(parent_id)
            if praent.first_child == 0:
                praent.first_child = branch.id
            else:
                nearest_brother = Branch.find_last_sibling(praent.first_child)
                nearest_brother.next_sibling = branch.id
            db.session.commit()
        return branch

    @staticmethod
    def get(id):
        return db.session.query(Branch).get(id)

    @staticmethod
    def get_fragments_by_branchname(name,find_sibling=False):
        res = []
        branch = db.session.query(Branch).filter_by(name=name).first()
        res.extend(branch.fragments)
        if branch.first_child != 0:
            first_child = Branch.get(branch.first_child)
            res.extend(Branch.get_fragments_by_branchname(first_child.name,find_sibling=True))
        if find_sibling:
            if branch.next_sibling != 0:
                next_sibling = Branch.get(branch.next_sibling)
                res.extend(Branch.get_fragments_by_branchname(next_sibling.name,find_sibling=True))
        return res

    @staticmethod
    def find_last_sibling(id):
        '''
        递归查找next_sibling为空的元素
        :param id:
        :return:
        '''
        branch = Branch.query.get(id)
        if branch.next_sibling == 0:
            return branch
        else:
            return Branch.find_last_sibling(branch.next_sibling)

    @staticmethod
    def get_all_choices():
        branchs = Branch.query.all()
        return [(branch.id,branch.name) for branch in branchs]

    @staticmethod
    def get_nearest_branch(deep=3,me_id=1):
        # print("up:",Branch.get_nearest_branch_up(deep=deep,me_id=me_id))
        # print("down:",Branch.get_nearest_branch_down(deep=deep,me_id=me_id))
        return Branch.get_nearest_branch_up(deep=deep,me_id=me_id) + Branch.get_nearest_branch_down(deep=deep,me_id=me_id)

    @staticmethod
    def get_nearest_branch_down(deep=3, me_id=1):
        res = []
        if me_id == 0:
            return []
        me = Branch.query.get(me_id)
        if (me.first_child == 0 and me.next_sibling == 0) or deep == 0:
            res.append(me)
            return res
        else:
            sibling = Branch.get_nearest_branch_down(deep=deep - 1, me_id=me.next_sibling)
            child = Branch.get_nearest_branch_down(deep=deep - 1, me_id=me.first_child)
            res.extend(sibling)
            res.extend(child)
            res.append(me)
            return res

    @staticmethod
    def get_nearest_branch_up(deep=3,me_id=1):
        res = []
        if me_id == 0:
            return []
        parent = Branch.query.filter_by(first_child=me_id).first()
        borther = Branch.query.filter_by(next_sibling=me_id).first()
        if parent:
            res.append(parent)
            if parent.id != 1 and deep != 0:
                grandfarther = Branch.get_nearest_branch_up(deep=deep - 1, me_id=parent.id)
                res.extend(grandfarther)
        if borther:
            res.append(borther)
            if borther.id != 1 and deep != 0:
                borhter = Branch.get_nearest_branch_up(deep=deep - 1, me_id=borther.id)
                res.extend(borhter)
        return res




    @staticmethod
    def sibling(id,sibling):
        '''
        获取所有兄弟分支
        :param id:
        :return: list(Branch)
        '''
        me = Branch.get(id)
        if me.next_sibling == 0:
            return sibling
        else:
            brother = Branch.get(me.next_sibling)
            sibling.append(brother)
            return Branch.sibling(brother.id, sibling=sibling)

    @staticmethod
    def branch_tree(root=1):
        '''生成json格式的分支树格式如下：
        json_data = {"id": "root", "topic": "jsMind", "children": [
            {"id": "easy", "topic": "Easy", "direction": "left", "children": [
                {"id": "easy1", "topic": "Easy to show"},
                {"id": "easy2", "topic": "Easy to edit"},
                {"id": "easy3", "topic": "Easy to store"},
                {"id": "easy4", "topic": "Easy to embed"},
                {"id": "other3", "background-image": "ant.png", "width": "100", "height": "100"}
            ]},
            {"id": "open", "topic": "Open Source", "direction": "right", "children": [
                {"id": "open1", "topic": "on GitHub", "background-color": "#eee", "foreground-color": "blue"},
                {"id": "open2", "topic": "BSD License"}
            ]},
            {"id": "powerful", "topic": "Powerful", "direction": "right", "children": [
                {"id": "powerful1", "topic": "Base on Javascript"},
                {"id": "powerful2", "topic": "Base on HTML5"},
                {"id": "powerful3", "topic": "Depends on you"}
            ]},
            {"id": "other", "topic": "test node", "direction": "left", "children": [
                {"id": "other1", "topic": "I'm from local variable"},
                {"id": "other2", "topic": "I can do everything"}
            ]}
        ]}
        '''
        tree = {}
        children = []
        me = Branch.get(root)
        tree["id"] = "root" if root == 1 else me.id
        tree["topic"] = me.name
        # 先找第一个儿子，有的话再找儿子的兄弟
        if me.first_child != 0:
            children.append(Branch.branch_tree(root=me.first_child))
            # children_of_me = Branch.get(me.first_child)
            my_sibling = []
            my_sibling = Branch.sibling(me.first_child,sibling=[])
            print("i'm",me,"my_sibling",my_sibling)
            if len(my_sibling) > 0:
                for branch in my_sibling:
                    print(branch.id,branch)
                    children.append(Branch.branch_tree(root=branch.id))

        tree["children"] = children
        print("tree",tree)

        return tree

    @staticmethod
    def fresh_branch_tree():
        branch_tree = {
            "meta": {
                "name": "branch_tree",
                "author": "allen",
                "version": "0.1"
            },
            "format": "node_tree",
            "data":{}
        }
        data = Branch.branch_tree()
        branch_tree["data"] = data
        branch_tree_str = json.dumps(branch_tree)
        json_file = os.path.join(base_dir,"branch_tree.json")
        if os.path.exists(json_file):
            os.remove(json_file)
        with open(json_file,'w',encoding="utf-8") as f:
            f.write(branch_tree_str)
            f.close()

    @staticmethod
    def has_branch_tree():
        return os.path.exists(os.path.join(base_dir, "branch_tree.json"))

    @staticmethod
    def branch_tree_to_json():
        json_file = os.path.join(base_dir, "branch_tree.json")
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding="utf-8") as f:
                branch_tree_str = f.read()
                f.close()
            return branch_tree_str
        else:
            return None

@event.listens_for(Branch, 'after_update')
def fresh_branch_tree_callback(mapper, connection, target):
    Branch.fresh_branch_tree()
    # print(Branch.branch_tree())
    # pass