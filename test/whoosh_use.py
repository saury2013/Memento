# -*- coding: utf-8 -*-
from app.whoosh import search_helper

# search_helper.add_document("未来","/wl","我们可以预见的不是未来而是昨天的重演。")
res = search_helper.search("未来")
print(res)