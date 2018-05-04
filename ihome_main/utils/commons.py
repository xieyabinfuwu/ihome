# -*- coding: utf-8 -*-
import functools

from flask import session, jsonify, g
from werkzeug.routing import BaseConverter

from ihome_main.utils.response_code import RET


class RegexConverter(BaseConverter):
    """在路由中使用正则表达式进行提取参数的转换工具"""
    def __init__(self,url_map,*args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        user_id = session.get("user_id")
        if user_id is None:
            return jsonify(errno=RET.SESSIONERR,errmsg="用户未登录")
        else:
            g.user_id=user_id
            return func(*args,**kwargs)
    return wrapper