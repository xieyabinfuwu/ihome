# -*- coding: utf-8 -*-
import logging
import random
import re
from flask import request, make_response, jsonify, json

from ihome_main import redis_store, constants
from ihome_main.api_1_0 import api
from ihome_main.models import User
from ihome_main.tasks.sms import tasks
from ihome_main.utils.SendTemplateSMS import CCP
from ihome_main.utils.captcha.captcha import captcha


# @api.route('/imagecode/<image_code_id>',methods=["GET"])
from ihome_main.utils.response_code import RET


@api.route('/imagecode')
def generate_image_code():
    """图片验证码"""
    # 获取当前和之前的ｉｄ信息
    per_image_id = request.args.get('pre')
    cur_image_id = request.args.get('cur')

    # 生成图片验证码
    # name-图片验证码的名字， text-图片验证码的文本， image-图片的二进制数据
    name,text,image = captcha.generate_captcha()
    try:
        redis_store.delete("ImageCode_"+per_image_id)
        redis_store.setex("ImageCode_"+ cur_image_id,constants.IMAGE_CODE_EXPIRES,text)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg="保存验证码失败")
    else:

        response = make_response(image)
        response.headers["Content-Type"]="image/jpg"
        return response
#第二种方式获取图片验证码
# @api.route("/image_code")
# def get_image_code():
#     """提供图片验证码"""
#     per_image_id = request.args.get('pre')
#     cur_image_id = request.args.get('cur')
#     #业务处理
#     #生成验证吗图片
#     #名字，验证码真实值，图片的二进制内容
#     name,text,image_data = captcha.generate_captcha()
#     try:
#         #保存验证码编的真实值／编号／redis数据ｖ的有效时间
#         redis_store.delete("image_code_%s"%per_image_id)
#         redis_store.setex("image_code_%s"% cur_image_id,constants.IMAGE_CODE_EXPIRES,text)
#     except Exception as e:
#         logging.error(e)
#         resp = {
#             "errno":RET.DBERR,
#             "errmsg":"保存验证码失败"
#         }
#         return jsonify(resp)
#     resp = make_response(image_data)
#     resp.headers["Content-Type"] = "image/jpg"
#     return resp

#短信发送函数
# @api.route('/smscode/<string:mobile>')
# def send_sms_code(mobile):
#     image_code = request.args.get('text')
#     image_code_id = request.args.get('id')
#     print(image_code,image_code_id,mobile)
#     if not all([mobile,image_code,image_code_id]):
#         # print("a")
#         return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
#     if not re.match(r"^1[34578]\d{9}$",mobile):
#         # print("b")
#         return jsonify(errno=RET.PARAMERR,errmsg="手机号格式错误")
#     #获取数据库中的ｉｍａｇｅ_code
#     try:
#         real_image_code = redis_store.get("ImageCode_"+image_code_id)
#     except Exception as e:
#         logging.error(e)
#         # print("c")
#         return jsonify(errno=RET.DBERR,errmsg="查询数据库异常")
#     # print(real_image_code)
#     if not real_image_code:
#         # print("d")
#         return jsonify(errno=RET.DATAERR,errmsg='图片验证码已过期')
#     try:
#         redis_store.delete("ImageCode_"+image_code_id)
#     except Exception as e:
#         logging.error(e)
#     if image_code.lower() != real_image_code.lower().decode("utf-8"):
#         print(image_code.lower(),real_image_code.lower().decode("utf-8"))
#         # print("e")
#         return jsonify(errno=RET.DATAERR,errmsg="图片验证码错误")
#     sms_code = '%06d'%random.randint(0,1000000)
#     try:
#         redis_store.setex("SMSCode_"+mobile,constants.SMS_CODE_EXPIRES,sms_code)
#     except Exception as e:
#         logging.error(e)
#         # print("f")
#         return jsonify(errno=RET.DBERR,errmsg="保存短信验证码失败")
#     try:
#         ccp = CCP.instance()
#         result=ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_EXPIRES/60],1)
#     except Exception as e:
#         logging.error(e)
#         # print("g")
#         return jsonify(errno=RET.THIRDERR,errmsg="发送短信异常")
#     if result == 0:
#         return jsonify(errno=RET.OK,errmsg="发送短信验证码成功")
#     else:
#         # print("h")
#         return jsonify(errno=RET.THIRDERR,errmsg="发送短信验证码失败")

#post请求试图函数
# @api.route('/smscode',methods=['POST'])
# def send_sms_code():
#     dict_data = json.loads(request.get_data())
#     mobile = dict_data.get('mobile')
#     image_code = dict_data.get('text')
#     image_code_id = dict_data.get('id')
#
#     print(image_code,image_code_id,mobile)
#     if not all([mobile,image_code,image_code_id]):
#         # print("a")
#         return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
#     if not re.match(r"^1[34578]\d{9}$",mobile):
#         # print("b")
#         return jsonify(errno=RET.PARAMERR,errmsg="手机号格式错误")
#     #获取数据库中的ｉｍａｇｅ_code
#     try:
#         real_image_code = redis_store.get("ImageCode_"+image_code_id)
#     except Exception as e:
#         logging.error(e)
#         # print("c")
#         return jsonify(errno=RET.DBERR,errmsg="查询数据库异常")
#     # print(real_image_code)
#     if not real_image_code:
#         # print("d")
#         return jsonify(errno=RET.DATAERR,errmsg='图片验证码已过期')
#     try:
#         redis_store.delete("ImageCode_"+image_code_id)
#     except Exception as e:
#         logging.error(e)
#     if image_code.lower() != real_image_code.lower().decode("utf-8"):
#         print(image_code.lower(),real_image_code.lower().decode("utf-8"))
#         # print("e")
#         return jsonify(errno=RET.DATAERR,errmsg="图片验证码错误")
#     #验证手机好是否存在：
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         logging.error(e)
#     else:
#         if user is not None:
#             return jsonify(errno=RET.DBERR,errmsg="手机号已存在")
#     sms_code = '%06d'%random.randint(0,1000000)
#     try:
#         redis_store.setex("SMSCode_"+mobile,constants.SMS_CODE_EXPIRES,sms_code)
#     except Exception as e:
#         logging.error(e)
#         # print("f")
#         return jsonify(errno=RET.DBERR,errmsg="保存短信验证码失败")
#     try:
#         ccp = CCP.instance()
#         result=ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_EXPIRES/60],1)
#     except Exception as e:
#         logging.error(e)
#         # print("g")
#         return jsonify(errno=RET.THIRDERR,errmsg="发送短信异常")
#     if result == 0:
#         return jsonify(errno=RET.OK,errmsg="发送短信验证码成功")
#     else:
#         # print("h")
#         return jsonify(errno=RET.THIRDERR,errmsg="发送短信验证码失败")

@api.route('/smscode',methods=['POST'])
def send_sms_code():
    dict_data = json.loads(request.get_data())
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('text')
    image_code_id = dict_data.get('id')

    print(image_code,image_code_id,mobile)
    if not all([mobile,image_code,image_code_id]):
        # print("a")
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
    if not re.match(r"^1[34578]\d{9}$",mobile):
        # print("b")
        return jsonify(errno=RET.PARAMERR,errmsg="手机号格式错误")
    #获取数据库中的ｉｍａｇｅ_code
    try:
        real_image_code = redis_store.get("ImageCode_"+image_code_id)
    except Exception as e:
        logging.error(e)
        # print("c")
        return jsonify(errno=RET.DBERR,errmsg="查询数据库异常")
    # print(real_image_code)
    if not real_image_code:
        # print("d")
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码已过期')
    try:
        redis_store.delete("ImageCode_"+image_code_id)
    except Exception as e:
        logging.error(e)
    if image_code.lower() != real_image_code.lower():
        # print(image_code.lower(),real_image_code.lower().decode("utf-8"))
        # print("e")
        return jsonify(errno=RET.DATAERR,errmsg="图片验证码错误")
    #验证手机好是否存在：
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
    else:
        if user is not None:
            return jsonify(errno=RET.DBERR,errmsg="手机号已存在")
    #创建短信验证码
    sms_code = '%06d'%random.randint(0,1000000)
    #保存短信验证码
    try:
        redis_store.setex("SMSCode_"+mobile,constants.SMS_CODE_EXPIRES,sms_code)
    except Exception as e:
        logging.error(e)
        # print("f")
        return jsonify(errno=RET.DBERR,errmsg="保存短信验证码失败")
    #使用celery发送验证码短信
    result = tasks.send_template_sms.delay(mobile,[sms_code,constants.SMS_CODE_EXPIRES/60],1)
    #返回异步结果对象，通过这个对象能够获得最终执行结果
    print(result.id)
    # 通过get方法能不用自己去backend中拿取执行结果，get方法会帮助我们返回执行结果
    # get()默认是阻塞的，会等到worker执行完成有了结果的时候才会返回
    # get()通过timeout超时时间，可以在超过超时时间后立即返回
    ret = result.get()
    print(ret)
    return jsonify(errno=RET.OK,errmsg="OK")