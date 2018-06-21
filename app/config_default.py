#coding: utf-8

class Config(object):
    DEBUG = True
    SECRET_KEY = 'this is secret string'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12050625@localhost:3306/memento?charset=utf8'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    ERROR_LOG = "../logs/error.log"
    INFO_LOG = "../logs/info.log"


    PER_PAGE = 10

    STATIC_IMG_PATH = "img"

    AVATAR_PATH = "resource/image/avatar"
    TMP_PATH = "resource/tmp"
    IMAGE_PATH = "resource/image/image"





