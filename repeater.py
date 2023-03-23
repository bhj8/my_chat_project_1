
import math
import random
import time
import traceback
from concurrent.futures import (ALL_COMPLETED, FIRST_EXCEPTION,
                                ThreadPoolExecutor, wait)
from queue import Queue

import discord
import requests

from openai_api import *
from price import price
from Utils import utils

queue = Queue()

def set_client(c):
    global client
    client = c




async def try2chat(msg, dic): 
    user_id =  msg.source
    chathistory_class = dic["chathistory"]
    lis = chathistory_class.history
    # lis[-1]=  utils.replace_quick_question(lis[-1])# 替换快捷问题
    print(user_id,"  chat  ",lis[-1])
    try:
        result =  await get_chat_response(lis)        
        re_chat = result[0]
        use_token = result[1]
        # if await get_moderation(result) :#chatgpt的回复好像并不用过滤
        #     client.send_text_message(user_id, "很抱歉，我不喜欢聊这个话题。让我们换换其它话题吧！")
        #     return        
        # re_chat =  utils.replace_badword_all(re_chat) # 过滤不良词汇
        client.send_text_message(user_id, re_chat)

        # sql_score_change(user_id,{"score_change":- math.ceil(use_token * price.per1000_chat/1000)})#聊天扣费
        print(user_id,"send","  chat message  ",len(re_chat))
    except Exception as e:
        print(e)
        client.send_text_message(user_id, "很抱歉，因网络延迟问题。答案生成失败，请您再次发送问题。")

async def deal_message(msg,dic):
    if dic["mode"] =="chat":
        return await try2chat(msg, dic)

async def on_message():    
    try:
        while True:
            (msg,dic) = queue.get()
            while True:
                try:
                    await asyncio.wait_for(deal_message(msg, dic), 8)
                    break  # 跳出内层循环，回到处理下一条消息
                except asyncio.TimeoutError:
                    print("处理消息超时，将再次尝试。")
                except Exception as e:
                    client.send_text_message(msg.source, "很抱歉，答案生成失败，请您再次发送问题。")
                    print("\r" + str(e))
                    break  # 如果发生其他异常，则跳出内层循环，回到处理下一条消息
    except Exception as e:
        client.send_text_message(msg.source, "很抱歉，因网络延迟问题。答案生成失败，请您再次发送问题。")
        print("\r" + e)


pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="on_message")
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())
pool.submit(asyncio.run, on_message())


def get_response(msg,dic) -> None:
    queue.put((msg,dic))