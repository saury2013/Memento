# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in
from whoosh.index import open_dir,exists_in
from whoosh.fields import TEXT, ID, Schema
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from jieba.analyse import ChineseAnalyzer

from app.utils.string_helper import trim_string

whoosh_dir = os.path.abspath(os.path.dirname(__file__))

index_file = os.path.join(whoosh_dir, "index")
if not os.path.exists(index_file):
    os.makedirs(index_file)
    # 使用结巴中文分词
analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                path=ID(stored=True),
                content=TEXT(stored=True,analyzer=analyzer))
if exists_in(index_file):
  ix = open_dir(index_file)
else:
  ix = create_in(index_file, schema)

def add_document(title, path, content):
    writer = ix.writer()
    writer.add_document(title=title, path=path, content=content)
    writer.commit()

def update_document(title, path, content):
    writer = ix.writer()
    writer.update_document(title=title, path=path, content=content)
    writer.commit()


def search(search_str):
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(search_str)
        print(query)
        result = searcher.search(query)
        res = []
        for hit in result:
            dict = {}
            dict["title"] = hit["title"]
            dict["path"] = hit["path"]
            dict["content"] = trim_string(hit["content"])
            res.append(dict)
        return res


if __name__ == '__main__':
    # add_document("高兴", '/ps', "快快乐乐高高兴兴开开开开心心")
    res = search("python")
    for i in res:
        print(i)
