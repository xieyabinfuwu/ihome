#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome_main.libs.ronglianyun.CCPRestSDK import REST


# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
accountSid= '8a216da861d4f5d90161d6352e5a0113'

#主帐号Token,登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
accountToken= '22eb9eaca3244f2983cde10555c1d539'

#应用Id 请使用管理控制台首页的APPID或自己创建应用的APPID
appId='8a216da861d4f5d90161d6352ebf011a'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print ('%s:%s') % (k, s)
#         else:
#             print ('%s:%s') % (k, v)
    
   
#sendTemplateSMS(手机号码,内容数据,模板Id)

class CCP(object):
    @staticmethod
    def instance():
        if not hasattr(CCP,"_instance"):
            CCP._instance=CCP()
        return CCP._instance
    def __init__(self):
        self.rest=REST(serverIP,serverPort,softVersion)
        self.rest.setAccount(accountSid,accountToken)
        self.rest.setAppId(appId)
    def send_template_sms(self,to,datas,temp_id):
        result = self.rest.sendTemplateSMS(to,datas,temp_id)
        if result.get("statusCode") == "000000":
            return 0
        else:
            return -1