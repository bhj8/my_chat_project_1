import asyncio
import os

import openai
from dotenv import load_dotenv

import Globals

load_dotenv()
#openai.organization = "org-FJzlkB2FVUgCd3naiH46NQT2"
openai.api_key = Globals.oPENAI_API_KEY
# Set up the OpenAI API parameters for the conversation model
t_txt = """The e-sports business department piloted the system of "employees purchase office notebooks by themselves, and the company subsidizes them on a monthly basis". After an employee applies for a laptop subsidy, he cannot apply for an additional computer from the company.
Here are the detailed instructions:

All employees can apply for laptop subsidies according to their work needs. The subsidy is divided into four levels of management path and four levels of technology path.
P2-P4 subsidy of 3,000 yuan, P5-P7 subsidy of 5,000 yuan, P8-P10 subsidy of 7,000 yuan, and P11 and above subsidy of 10,000 yuan;
A subsidy of 3,000 yuan for ranks T2-T4, 5,000 yuan for ranks T5-T7, 7,000 yuan for ranks T8-T10, and 10,000 yuan for ranks T11 and above;
Special positions that need to exceed the standard configuration need to be agreed by the network management-department head-administrative person-in-charge;
After the application is approved by the company, the employee will purchase the notebook at his own expense and issue a special value-added tax invoice in the name of the company. The company will give corresponding subsidies according to the stalls. The part exceeding the stall amount will not be subsidized. Amount subsidy, the subsidy is divided into 36 months, and the salary is paid every month.
Employees who buy notebooks for office work will be given subsidies, and the property rights of notebooks will belong to individuals after 3 years;
 During the period, if someone leaves or is dismissed, the company will suspend the monthly subsidy, and the property rights of the notebook will belong to the individual. If other circumstances occur, the final interpretation right belongs to the company;
All relevant vouchers, warranty cards, manuals, etc. of the notebook computer will be kept by individuals during the period. If the documents and vouchers are lost, resulting in inability to enjoy after-sales, the individual will be responsible;
If the company's employee rank is promoted within 3 years, the follow-up notebook subsidy will also be increased accordingly;
Employees enjoy this system. If the computer is unusable due to hardware damage or software poisoning, they can ask the company to repair it on their behalf.
After applying for a notebook, employees need to use this notebook for office work. If they use other notebooks, they must report in advance and explain the reasons. The company will conduct regular inspections, and will issue warnings and fines to employees who use computers that do not meet the requirements."""
async def get_moderation(imessage: str):#是否有不当内容  True 有不当内容
  moderation = await openai.Moderation.acreate(
  input=imessage,
  )
  return moderation.results[0].flagged

#进来的list的排序从最旧到最新
def prepare_message(last_messages: list = []):
  old_message = ""
  if len(last_messages) == 0: return []
  messages=[
    {"role": "system", "content": "你是一个叫小慧个人的助手。拒绝谈论任何政治有关的内容！拒绝谈论中国历史上的任何事情！"}]
  token = 0
  for i in range(len(last_messages)-1):
    old_message = last_messages[i] + "\n"    
    token = token + len(last_messages[i])
    if token > 200:      
      break
  messages.append({"role": "user", "content": "请帮我回复关于以下通知的疑问："+t_txt})
  messages.append({"role": "assistant", "content": "好的，我知道了。"})
  messages.append({"role": "user", "content":"以下我之前和你说过的话："+ old_message})
  messages.append({"role": "assistant", "content": "好的，我知道了。"})
  messages.append({"role": "user", "content": last_messages[-1]})
  return messages


async def get_chat_response(last_messages: list = [])->str:
  completions = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    #temperature = 0.5,
    presence_penalty = 1,
    #frequency_penalty = 0.5,

    top_p = 0.2,     
    #n = 1,
    #stream = False,
    #stop =" ",# [ " User:", " Assistant:"],
    # max_tokens = 500,
    messages=prepare_message(last_messages),
    
  )
  # Return the response
  return [completions.choices[0].message.content.strip(),completions.usage.total_tokens]


      # messages=[
      #     {"role": "system", "content": "You are a talking Tommy cat."},
      #     {"role": "user", "content": "Please play a talking Tommy cat and chat with child.please say yes if you can"},#You can briefly decline to answer uncomfortable questions.
      #     {"role": "assistant", "content": "yes"},
      #     # {"role": "user", "content": "Who are you?"},
      #     # {"role": "assistant", "content": "i am talking tom cat."},
      #     {"role": "user", "content": "请帮我翻译以下英文，谢谢"},
      #     {"role": "assistant", "content": "好的，请你告诉我要翻译的内容"},
      # ]
async def get_translation(last_messages: list = []):
  completions = await openai.ChatCompletion.acreate(
    model="gpt-3.5-turbo",
    presence_penalty = 0,
    top_p = 0.2, 
    messages=[
        # {"role": "system", "content": "you are a translator."},
        # {"role": "user", "content": "Please translate the content I send you into English."},
        # {"role": "assistant", "content": "yes"},
        {"role": "user", "content": "Translate the following Chinese text to English: "+last_messages[0]},
        
    ]    
  )
  # Return the response
  return completions.choices[0].message.content.strip()

if __name__ == "__main__":
  openai.proxy=  {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
}
  # print(asyncio.run(get_translation(["一个美少女,jk,金色头发,带着眼镜"])))
  print(asyncio.run(get_chat_response(["你好","武汉好还是杭州好","最火的抖音音乐","反法西斯战争是什么"])))
  # print(asyncio.run(get_moderation(["审核能力测试"])))
# 处理生成的文本输出
#print(message)


