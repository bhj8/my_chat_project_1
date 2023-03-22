#strings
import os
import sys

import dotenv

dotenv.load_dotenv()

def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value or value == "":
        print(f"错误：又尼玛的狗日的没设置环境变量是不是？？？？",var_name)
        exit()
    return value


APPID = get_env_variable("MY_WEROBOT_APPID")
APPSECRET = get_env_variable("MY_WEROBOT_APPSECRET")
TOKEN=get_env_variable("MY_WEROBOT_TOKEN")
AES_KEY=get_env_variable('MY_ENCODING_AES_KEY')

oPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")
#boolean
USE_MESSAGED_CHANNEL = True

#don't edit the following variable
MID_JOURNEY_ID = "936929561302675456"  #midjourney bot id
targetID       = ""
targetHash     = ""
