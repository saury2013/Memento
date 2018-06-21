# -*- coding: utf-8 -*-

def trim_string(str):
    if len(str) > 300:
        return str[:300] + "..."
    return str