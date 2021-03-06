# -*- coding: utf-8 -*-
import datetime
import cronjobs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from weixin.models import Conversation

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)


global conversation

def handle_user(str):
    global conversation
    num1 = str.find('{')
    num2 = str.find('}')
    if not(num1 == -1):
        info = str[num1:num2+1]
        info = eval(info)
        createtime = datetime.datetime.fromtimestamp(info['CreateTime'])
        uid = info['FromUserName']
        content_type = info['MsgType']
    
        if content_type == 'text':
            content = info['Content'].encode('utf-8').replace(' ','')
        elif content_type == 'event':
            content = info['Event']
        elif content_type == 'voice':
            content = u'声音无法识别'
   
        conversation = Conversation(uid=uid, user_content=content, content_type=content_type, createtime=createtime)
        conversation.save()

def handle_match(str):
    global conversation
    num1 = str.find('match')
    num2 = num1 + 6
    match_type = str[num2:-1]
    conversation.match_type = match_type
    conversation.save()

def handle_reply(str):
    global conversation
    num1 = str.find('type')
    num1 += 5
    num2 = str.find('platform')
    num2 -= 1
    reply_type = str[num1:num2]
    conversation.reply_type = reply_type
    
    num3 = str.find('data')
    num3 += 5
    reply_data = str[num3:-1]
    conversation.reply_data = reply_data
    conversation.save()



#1 represents user;2 represents match;3 represents reply 
def judge(str):
    number1 = str.find('receive')
    number2 = str.find('match')
    number3 = str.find('reply')
    
    if not(number1 == -1):
        return 1
    if not(number2 == -1):
        return 2
    if not(number3 == -1):
        return 3


@cronjobs.register
def update_conversation():  

    today = datetime.datetime.now().date()
    yesterday = today + datetime.timedelta(days=-1)

    file = open('/data/logs/conversation.log.'+str(yesterday))
    strs = file.readlines()
    for str in strs:        
        if judge(str) == 1:
            handle_user(str)
        elif judge(str) == 2:
            handle_match(str)
        elif judge(str) == 3:
            handle_reply(str)


    file.close()


#可以重新记录所有的数据
@cronjobs.register
def update_conversation_all():

    file = open('/data/logs/weixin.log')
    strs = file.readlines()
    for str in strs:
        if judge(str) == 1:
            handle_user(str)
        elif judge(str) == 2:
            handle_match(str)
        elif judge(str) == 3:
            handle_reply(str)


    file.close()
    
    
