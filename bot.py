# -*- coding: utf-8 -*-

import os
import threading
import time

# import cryptography
import werobot
from dotenv import load_dotenv

import Globals  # 这个是我自己写的一个文件，里面有一些全局变量
from ChatHistory import chathistory
from mytxt import mytxt
from repeater import *
from Utils import utils

load_dotenv()
AppID = Globals.APPID
AppSecret = Globals.APPSECRET
token=Globals.TOKEN
aes_key=Globals.AES_KEY

robot = werobot.WeRoBot( token=token)
robot.config['APP_ID'] = AppID
robot.config['APP_SECRET'] = AppSecret
robot.config['ENCODING_AES_KEY'] = aes_key
client = robot.client
# disclass_thread = threading.Thread(target=run_disclass, daemon=True)
# disclass_thread.start()

sql = robot.session_storage#实例化数据库  openai：1."score"积分2."freescore"每日免费积分 3."inrmb"总充值金额 4."friendkey"邀请码 5."chats"总聊天次数 6."paints"总画画次数 7."all_invite"总邀请次数 8."already_invited" 已经被邀请 9."alredy_gift_key" 一个dic，已经使用的礼品码
#key 的 1."user_id" 用户id  2."count" 这个key成功邀请的次数



set_client(client)
# set_sql(sql)
# # @robot.handler
# # def hello(message):
# #     return message.content


#并发限制
user_status = {}
def no_in_paint(user_status,user_id):
    user_status.pop(user_id)
def execute_after_five_seconds(user_status,user_id):
    time.sleep(1)
    no_in_paint(user_status,user_id)
def later_no_paint(user_id):
    thread = threading.Thread(target=execute_after_five_seconds,args=(user_status,user_id))
    thread.start()

#储存聊天记录到内存
user_chats = {}
#为img2img专门服务的聊天记录储存
user_chats_img2img = {}

# #封装对sql的操作
# def sql_update(id,dic):
#     a = sql.get(id)
#     a.update(dic)
#     sql.set(id,a)
# def sql_del(id,dic):
#     a = sql.get(id)
#     for key in dic :
#         a.pop(key,None)    
#     sql.set(id,a)
# def sql_get(id):
#     a = sql.get(id)
#         # raise ValueError(f"在get sql数据库时发现了异常，没有get到{id}值")
#     return a
        

# #设置新用户的sql
# def set_newuser_sql(message):
#     dic = sql_get(message.source)
#     fkey = utils.get_friendkey(message.source)
#     dic['friendkey'] = fkey #先绑定一个邀请码
#     if not 'score' in dic:
#         dic['score'] = price.new_user#就这里预设了新用户的积分
#     if not 'freescore' in dic:
#         dic['freescore'] = 0
#     if not 'inrmb' in dic:
#         dic['inrmb'] = 0
#     if not 'chats' in dic:
#         dic['chats'] = 0
#     if not 'paints' in dic:
#         dic['paints'] = 0
#     if not 'all_invite' in dic:
#         dic['all_invite'] = 0
#     if not 'already_invited' in dic:
#         dic['already_invited'] = 0
#     if not 'alredy_gift_key' in dic:
#         dic['alredy_gift_key'] = {}
#     sql_update(message.source,dic)
#     sql_update(fkey,{"user_id":message.source})
#     if  "count" not in  sql_get(fkey):
#         sql_update(fkey,{"count":0})    
#     print(message.source,"new user",dic)
# #设置邀请码的sql
# def set_invite_sql(user_id):
#     sql_update(user_id,{"all_invite":sql_get(user_id)["all_invite"]+1})
#     sql_update(user_id,{"score":sql_get(user_id)["score"]+price.invite_user})
#     pass


# @robot.filter("示例")
# def show_shili(message):
#     return mytxt.welcometxt

# @robot.filter("模式")
# def show_zhongzi(message):
#     return mytxt.panint_modeltxt

# @robot.filter("管理员")
# def show_guanliyuan(message):
#     with open("admin.txt","w") as f:
#         if client._token :
#             f.write(client._token)
#         else:print("没有access_token！！！")
#     return werobot.replies.SuccessReply()

# @robot.filter("积分")
# def show_score(message):
#     set_newuser_sql(message)
#     t = sql_get(message.source)
#     return f"""你的永久积分为:{t['score']}
# 免费积分为:{ t['freescore']}
# 优先自动使用免费积分,积分可以通过邀请好友获得。
# 你已经邀请了{t['all_invite']}个用户
# 输入"价格"查看积分定价"""#(每日6点重置为{price.daily_user}


@robot.filter("全文")
def show_price(message):
    return mytxt.welcometxt

# # sql_update("id",{"score":100,"freescore":100})
# # a = sql_get("id")['score']
# # print(a)
# @robot.filter("帮助")
# def show_help(message):
#     return  mytxt.help_txt

# @robot.filter("邀请码")
# def show_invite(message):
#     set_newuser_sql(message)
#     client.send_text_message(message.source,mytxt.invite_txt)
#     return f"{sql_get(message.source)['friendkey']}"


# #新用户关注
# @robot.subscribe
# def subscribe(message):
#     set_newuser_sql(message)
#     return mytxt.newusertxt


@robot.voice #语音转文字后发送到文字处理函数
def handler_voice(message):
    message.content = message.recognition
    return hello_world(message)
#偷懒的礼品码写法，反正也是公开的，无所谓了
# gift_key = {"key_dd338b58":{"used":0,"max_count":500,"score":100,"low_score":20}}
# if "key_dd338b58" not in  sql_get("gift_key") :
#     sql_update("gift_key",gift_key)


@robot.text #文字处理函数
def hello_world(message): 
    # if message.content.startswith("key"):
    #     gift_key_txt = message.content.strip()
    #     gift_key_sql_dic =sql_get("gift_key")
    #     if utils.is_valid_gift_code(gift_key_txt):#判断是否是礼品码
    #         if gift_key_txt in gift_key_sql_dic:#判断礼品码是否存在
    #             set_newuser_sql(message)#保证用户的sql正确
    #             if gift_key_txt in sql_get(message.source)['alredy_gift_key']:#判断是否已经兑换过
    #                 return "您已经兑换过该礼品码了。"
    #             t_add_score = gift_key_sql_dic[gift_key_txt]["score"]
    #             if gift_key_sql_dic[gift_key_txt]["used"] >= gift_key_sql_dic[gift_key_txt]["max_count"]:#判断礼品码是否已经被兑换超过500名
    #                 t_add_score = gift_key_sql_dic[gift_key_txt]["low_score"]
    #             sql_update(message.source,{"score":sql_get(message.source)["score"]+t_add_score})#给用户加积分
    #             sql_update(message.source,{"alredy_gift_key":{**sql_get(message.source)['alredy_gift_key'],gift_key_txt:1}})#记录用户已经兑换过的礼品码
    #             return f"礼品码兑换成功，您获得了{t_add_score}积分。"

    #     return "您输入了的礼品码不正确，我无法识别。请检查后输入。"

    # if message.content.startswith("id"):#输入验证邀请码
    #     set_newuser_sql(message)#保证用户的sql正确
    #     if  utils.is_valid_invite_code(message.content.strip()) :
    #         if sql_get(message.source)['already_invited'] >= 1:
    #             return "你已经输入过邀请码了，不要重复输入。每个人只能被邀请一次"
    #         if sql_get(message.source)['friendkey'] == message.content.strip():
    #             return "你不能输入自己的邀请码。你总不能邀请自己吧？？？"

    #         #下面去找邀请码对应的用户
    #         key_dic = sql_get(message.content.strip())
    #         if  key_dic != {}:
    #             user_id =  key_dic["user_id"]
    #             if sql_get(user_id)  != {}:
    #                 set_invite_sql(user_id)
    #                 sql_update(message.source,{'already_invited':sql_get(message.source)['already_invited'] + 1})
    #                 return "邀请码输入成功！感谢你的支持！"
    #     return "邀请码不存在，确认后重新输入。一个正常的邀请码为  id_a665a459  。你只需要输入邀请码，不用任何多余的字符"

#     #看看积分还够不够
#     if sql_get(message.source) == {}:
#         set_newuser_sql(message)
    
#     if sql_get(message.source)["score"] + sql_get(message.source)["freescore"] <= 0:
#         client.send_text_message(message.source,sql_get(message.source)["friendkey"])
#         return f"""积分不足，无法继续聊天。你可以邀请任意好友关注 小慧很智慧 
# 并要求您的好友将您的邀请码发送给小慧,即可获得免费{price.invite_user}永久积分
# 输入“积分”查询积分
# 输入“价格”查询积分定价"""

    # if not utils.is_allow_paint_txt(message.content) :
    #     return "很抱歉，经过AI判断，您的问题中可能包含不宜回答的语义，我不会做出任何回答。意图违规使用将会被限制使用。no zuo no die！！！"
    # if not utils.is_allow_chat_txt(message.content) :
    #     return "检测到敏感语义，无心之举请无视。本轮聊天已被记录，请您知晓网络并非法外之地。如查实违规，所有聊天记录将上报。所有后果您自行承担！AI不会回答任何此类问题。"

    # if message.content.startswith("画图"):#画图
    #     message.content = message.content[2:].strip()#去掉画人两字
    #     if message.source not in user_status:#请求频率限制
    #         user_status[message.source] =True
    #         later_no_paint(message.source)
    #         seed = utils.generate_seed(message.source + message.content)
    #         # session[str(seed)] = message.content
    #         # asyncio.run(deal_message(message,{"seed":seed,"mode":"paint"}))#临时测试用
    #         get_response(message,{"seed":seed,"mode":"mj_paint"})

    #         return mytxt.start_mj_paint_txt
    #     else:
    #         return "请求过于频繁，请稍后再试。"

    # if message.content.startswith("画人"):#画人
    #     message.content = message.content[2:].strip()#去掉画人两字
    #     if message.source not in user_status:#请求频率限制
    #         user_status[message.source] =True
    #         later_no_paint(message.source)
    #         seed = utils.generate_seed(message.source + message.content)
    #         # session[str(seed)] = message.content
    #         # asyncio.run(deal_message(message,{"seed":seed,"mode":"paint"}))#临时测试用
    #         get_response(message,{"seed":seed,"mode":"paint"})

    #         return mytxt.start_paint_txt
    #     else:
    #         return "请求过于频繁，请稍后再试。"

    # if message.content.startswith("高清"):#画图
    #     message.content = message.content[2:].strip()#去掉画图两字
    #     if message.source not in user_status:#请求频率限制
    #         user_status[message.source] =True
    #         later_no_paint(message.source)
    #         seed = utils.generate_seed(message.source + message.content)
    #         # session[str(seed)] = message.content
    #         # asyncio.run(deal_message(message,{"seed":seed,"mode":"paint"}))#临时测试用
    #         get_response(message,{"seed":seed,"mode":"high_paint"})

    #         return mytxt.start_paint_txt
    #     else:
    #         return "请求过于频繁，请稍后再试。"
    #     # messages.content = replace_badword(message.content)
    # if message.content.startswith("照片"):#照片
    #     message.content = message.content[2:].strip()#去掉z照片两字
    #     seed = utils.generate_seed(message.source + message.content)
    #     user_chats_img2img[message.source] = {"seed":seed,"last_txt":message.content}
        # return "照片转换题词设置完毕"

        

    if message.source not in user_chats:
        user_chats[message.source] = chathistory()
    user_chats[message.source].add_message(message.content)
    # asyncio.run(deal_message(message,{"chathistory":user_chats[message.source],"mode":"chat"}))#临时测试用
    get_response(message,{"chathistory":user_chats[message.source],"mode":"chat"})
    
    # if "图" in message.content or "画" in message.content :
    #     return "想要画图，请以画图会开头。例如：画图 金发女孩"
    # if "邀" in message.content or "码" in message.content  or "邀请" in message.content:
    #     return show_invite(message)

    #一个success的return，不然会报错
    return werobot.replies.SuccessReply()

# @robot.image #图片处理函数
# def handler_image(message):
#         #看看积分还够不够
#     if sql_get(message.source) == {}:
#         set_newuser_sql(message)
    
#     if sql_get(message.source)["score"] + sql_get(message.source)["freescore"] <= 0:
#         client.send_text_message(message.source,sql_get(message.source)["friendkey"])
#         return f"""积分不足，无法继续聊天。你可以邀请任意好友关注 小慧很智慧 
# 并要求您的好友将您的邀请码发送给小慧,即可获得免费{price.invite_user}永久积分
# 输入“积分”查询积分
# 输入“价格”查询积分定价"""
#     if message.source not in user_status:#请求频率限制
#         user_status[message.source] =True
#         later_no_paint(message.source)
#         if message.source not in user_chats_img2img:
#             user_chats_img2img[message.source] = {"seed":-1,"last_txt":""}
#         get_response(message,{"mode":"img2img","seed":user_chats_img2img[message.source]["seed"],"last_txt":user_chats_img2img[message.source]["last_txt"]})
#         return "照片正在变换中，耗时较久。请稍后。。。。请勿发送不雅和违法的图片，触碰法律红线后台将自动上报。后果自负！！！照片转换功能尚在测试阶段，尚不完善。AI 50%概率处理不好手，照片中最好不要出现手。"
#     return "请求过于频繁，请稍后再试。同一时间只能处理一张哦。"
# @robot.handler#意外处理函数
# def echo(message):
#     return mytxt.unexpected_txt
#自定义菜单
def init_menu():
    client.create_menu({
        "button": [
            {
                "type": "click",
                "name": "说明",
                "key": "left_click"
            },
        ]
    })

init_menu()
@robot.click
def abort(message):
    if message.key == "left_click":
        return mytxt.welcometxt
#     elif message.key == "chat_click":
#         return mytxt.chat_txt
#     elif message.key == "paint_click":
#         return mytxt.paint_txt
#     elif message.key == "img2img_click":
#         return mytxt.img2img_txt
#     elif message.key == "score_click":
#         return show_score(message)
#     elif message.key == "price_click":
#         return  show_price(message)
#     elif message.key == "invite_click":
#         return show_invite(message)
#     elif message.key == "about_click":
#         return mytxt.about_txt

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

