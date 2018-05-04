# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import config, Config
from ihome_main.utils.commons import RegexConverter

#创建数据库对象
db = SQLAlchemy()
#使用wtf提供的csrf保护机制
csrf = CSRFProtect()

#设置日志的级别
logging.basicConfig(level=logging.DEBUG)
#创建日志记录其，指明日志保存的路径／每个日志文件的最大值，保存的上线日志
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日后记录器
logging.getLogger().addHandler(file_log_handler)
#创建redis数据库
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,
                                port=Config.REDIS_POST,decode_responses=True)

def create_app(config_name):
    """创建flask应用ａｐｐ对象"""
    app = Flask(__name__)
    # 从配置对象中为ａｐｐ设置配置信息
    app.config.from_object(config[config_name])
    # 为ａｐｐ中的ｕｒｌ路由添加正则表达式匹配
    app.url_map.converters['regex'] = RegexConverter

    #初始化db
    db.init_app(app)
    # 为app添加CSRF保护
    csrf.init_app(app)
    #创建ｓｅｓｓｉｏｎ
    Session(app)

    from ihome_main.api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix="/api/v1.0")

    from ihome_main.web_pages import html as html_blueprint
    app.register_blueprint(html_blueprint)

    return app