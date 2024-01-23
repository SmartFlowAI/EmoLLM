import SparkApi
from prompt import *
from tqdm import tqdm


with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)


# 以下密钥信息从控制台获取
appid = configs['appid']  # 填写控制台中获取的 APPID 信息
api_secret = configs['api_secret']  # 填写控制台中获取的 APISecret 信息
api_key = configs['api_key']  # 填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    


if __name__ == '__main__':
    text.clear
    file_name = 'a2.jsonl'
    conversations = []
    for i in range(1):
        for j in tqdm(range(10)):
            Input = prompt(i)
            question = checklen(getText("user",Input))
            SparkApi.answer =""
            SparkApi.main(appid,api_key, api_secret, Spark_url, domain, question)
            getText("assistant", SparkApi.answer)
            conversations.append(xinghuo_api(SparkApi.answer))
            if i % 2 == 0 :
                save_jsonl(conversations, file_name)
                conversations.clear()

