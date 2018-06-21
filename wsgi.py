# -*- coding: utf-8 -*-
from flask_script import Manager,Shell

from app import create_app
from app.models import db
from app.models.user import User
from app.models.fragment import Fragment
from app.models.branch import Branch
from app.models.tag import Tag
from app.main.views.home import url_for_other_page

application = create_app()
application.jinja_env.globals['url_for_other_page'] = url_for_other_page
manager = Manager(application)

def make_shell_context():
    return dict(application=application,
                db=db,User=User,
                Fragment=Fragment,
                Branch=Branch,
                Tag=Tag)
manager.add_command("shell",Shell(make_context=make_shell_context))

if __name__ == '__main__':
    application.run()
    # manager.run()