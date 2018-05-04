# -*- coding: utf-8 -*-
import logging
import re
from flask import request, jsonify, json, session, redirect

from ihome_main import db, redis_store, constants
from ihome_main.api_1_0 import api
from ihome_main.models import User
from ihome_main.utils.commons import login_required
from ihome_main.utils.response_code import RET


@api.route("/users",methods=["POST"])
def register():
    """用户注册"""
    #从ｊｓｏｎ中获取参数
    req_data=request.get_data()
    if not req_data:
        return jsonify(erron=RET.PARAMERR,errmsg="参数不完整")
    dict_data = json.loads(req_data)

    mobile = dict_data.get("mobile")
    sms_code = dict_data.get("sms_code")
    password = dict_data.get("password")
    #检查参数
    if not all([mobile,sms_code,password]):
        return jsonify(erron=RET.PARAMERR,errmsg="参数不完整")
    # 手机号格式校验
    if not re.match(r"1[34578]\d{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 检查短信验证码
    # 从redis中读取真实的短信验证码
    try:
        real_sms_code = redis_store.get("SMSCode_" + mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取验证码异常")

    # 判断验证码是否过期
    if not real_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码过期")

    # 判断用户输入的验证码的正确性
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码无效")

    # 已经进行过短信验证码的对比校验，所以删除redis中的smscode
    try:
        redis_store.delete("SMSCode_" + mobile)
    except Exception as e:
        logging.error(e)

    # 保存用户信息
    user = User(name=mobile, mobile=mobile)
    # 通过设置user模型的password属性，实际调用了设置密码的方法，对密码进行了加密
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    # 保存用户的session数据
    session["user_id"] = user.id
    session["name"] = mobile
    session["mobile"] = mobile

    return jsonify(errno=RET.OK, errmsg="注册成功")

@api.route("/sessions",methods=["POST"])
def login():
    """用户登陆"""
    #获取参数
    req_data = request.get_data()
    print(req_data)
    if not req_data:
        return jsonify(erron=RET.PARAMERR,errmsg="参数不完整")
    dict_data = json.loads(req_data)
    print(dict_data)
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")
    #检查参数
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    #手机号格式校验
    if not re.match(r"^1[34578]\d{9}$",mobile):
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式错误")

    #判断用户的错误次数
    #从sedis中获得错误次数、
    user_ip = request.remote_addr
    try:
        access_counts = redis_store.get("access_%s"% user_ip)
    except Exception as e:
        logging.error(e)
    else:
        if access_counts is not None and int(access_counts)>=constants.LOGIN_ERROR_MAX_NUM:
            return jsonify(errno=RET.REQERR,errmsg="登陆过于多,请稍候")
    #检查密码是否正确
    user = User.query.filter_by(mobile=mobile).first()
    #调用ｕｓｅｒ模型中实的检验用户密码的方法
    if user is None or not user.check_password(password):
        #出现错误，累加错误次数
        try:
            redis_store.incr("access_%s"% user_ip)
            redis_store.expire("access_%s"%user_ip,constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            logging.error(e)

        return jsonify(errno=RET.DATAERR,errmsg="用户名或密码错误")
    #登陆成功
    #清除用户的登陆错误次数
    try:
        redis_store.delete("access_%s"%user_ip)
    except Exception as e:
        logging.error(e)
    #用户验证成功，保存用户的session数据
    session["user_id"] = user.id
    session["name"] = user.name
    session["mobile"] = user.mobile
    return jsonify(errno=RET.OK,errmsg="登陆成功",data={"user_id":user.id})

#是否登陆
@api.route('/check_status',methods=["GET"])
def check_login():
    """检查用户的登陆状态"""
    user_id = session.get("user_id")
    user_name = session.get("name")
    if user_id is None:
        return jsonify(errno=RET.SESSIONERR,errmsg="用户没登陆")
    return jsonify(errno=RET.OK,errmsg='已登陆',data=user_name)

#退出登陆
#第一种方法，重定向模板
# @api.route('/session')# methods=['DELETE']
# # @login_required
# def logout():
#     """退出"""
#     session.clear()
#     # return jsonify(errno=RET.OK,errmsg="OK")
#     return redirect("/")
#第二种方法
@api.route("/session",methods=["DELETE"])
def logout():
    """登出"""
    session.clear()
    return jsonify(errno=RET.OK,errmsg="OK")
