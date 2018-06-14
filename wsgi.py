# -*- coding: utf-8 -*-
from flask_script import Manager,Shell

from app import create_app
from app.models import db
from app.models.user import User
from app.models.fragment import Fragment
from app.models.branch import Branch
from app.models.tag import Tag

application = create_app()
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