# -*- coding: utf-8 -*-


#定义任务
from ihome_main.tasks.main import app1
from ihome_main.utils.SendTemplateSMS import CCP


@app1.task
def send_template_sms(to,datas,temp_id):
    """发送短信"""
    ccp = CCP()
    ret = ccp.send_template_sms(to,datas,temp_id)
    return ret