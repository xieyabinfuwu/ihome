# -*- coding: utf-8 -*-
import redis


class Config:
    """基本配置参数"""
    SECRET_KEY = "TQ6uZxn+SLqiLgVimX838/VplIsLbEP5jV7vvZ+Ohqw="
    # flask-sqlalchemy使用的参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:xyb.1206@127.0.0.1/ihome" #数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 追踪数据库的修改行为

    #配置redis端口信息
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379
    #flask-session使用的参数
    SESSION_TYPE="redis"#制定保存session数据ｖ的地方
    SESSION_USE_SIGNER = True#对session_id进行签名
    SESSION_REDIS=redis.StrictRedis(host=REDIS_HOST,port=REDIS_POST)
    PERMANENT_SESSION_LEFE_TIME=86400#session数据ｖ的有效时间（单位秒）
class DevelopmentConfig(Config):
    """开发模式的配置参数"""
    DEBUG = True
    #支付宝
    ALIPAY_APPID = "2016091100488692"
    ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"
class ProductionConfig(Config):
    """生产模式的配置参数"""
    pass
class TestingConfig(Config):
    """测试模式的配置参数"""
    TESTING = True


config = {
    "development": DevelopmentConfig,  # 开发模式
    "production": ProductionConfig,  # 生产/线上模式
    "testing":TestingConfig, #测试模式
    "default":DevelopmentConfig # 默认模式
}