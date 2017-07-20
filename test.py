#coding=gbk

import requests as req
import hashlib
import os
import json
import time

# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot(cache_path = True, console_qr = True)
my_friend = bot.friends().search("吴小昊")[0]
my_group = bot.groups().search("联邦EE申请")[0]

@bot.register()
def auto_reply(msg):
    if msg.sender != my_group:
        my_friend.send_msg('收到消息{}: {} ({})'.format(msg.sender,msg.text, msg.type))


url_list={
    'cic':'http://www.cic.gc.ca/english/express-entry/rounds.asp',
    'nsnp':'http://novascotiaimmigration.com/move-here/nova-scotia-demand-express-entry/',
    'oinp':'http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html'
}

md5_list={}.fromkeys(url_list.keys())

def Check():
    fo = open("foo.txt")
    md5_list=json.loads(fo.readline())

    fo.close()

    print(md5_list)

    for item,url in url_list.items():
        
        try:
            rsp=req.get(url=url, headers={'Accept-Encoding': ''})
            rsp.raise_for_status()
        except req.RequestException as e:
            my_friend.send_msg(e.message)
            md5=e.errno
        else:
            #0.75 as magic number
            md5=hashlib.md5(rsp.content[:int(len(rsp.content)*0.75/100)*100]).hexdigest()
            
        if md5 != md5_list[item]:
            #push notify
            my_friend.send_msg(item + ' is changed\n' + url)
            my_group.send_msg('@所有人'+ item + ' is changed\n' + url)
            md5_list[item] = md5
            print (item + ' is changed')
        else:
            print (item + ' is ok')

    fo = open("foo.txt",'w')
    fo.writelines(json.dumps(md5_list, ensure_ascii = False))
    fo.close()
    print (md5_list)

while True:  
    print (time.strftime('%Y-%m-%d %X',time.localtime()))  
    Check() # 此处为要执行的任务  
    time.sleep(600)