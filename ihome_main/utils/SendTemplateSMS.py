#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome_main.libs.ronglianyun.CCPRestSDK import REST


# ˵�������˺ţ���½��ͨѶ��վ�󣬿���"����̨-Ӧ��"�п������������˺�ACCOUNT SID
accountSid= '8a216da861d4f5d90161d6352e5a0113'

#���ʺ�Token,��½��ͨѶ��վ�󣬿��ڿ���̨-Ӧ���п������������˺�AUTH TOKEN
accountToken= '22eb9eaca3244f2983cde10555c1d539'

#Ӧ��Id ��ʹ�ù������̨��ҳ��APPID���Լ�����Ӧ�õ�APPID
appId='8a216da861d4f5d90161d6352ebf011a'

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com'

#����˿� 
serverPort='8883'

#REST�汾��
softVersion='2013-12-26'

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
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
    
   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)

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