# -*- coding: utf-8 -*-
from celery import Celery

app1 = Celery("ihome")


app1.config_from_object("ihome_main.tasks.config")

#让celery自己找到任务
app1.autodiscover_tasks(["ihome_main.tasks.sms"])