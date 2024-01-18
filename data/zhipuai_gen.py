import os
import random
from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()
client = ZhipuAI(api_key=os.getenv('ZHIPUAI_API_KEY'))

def getText(role, content, text = []):
    jsoncon = {}
    jsoncon['role'] = role
    jsoncon['content'] = content
    text.append(jsoncon)
    return text


prompt = '''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话案例的专家，请你构造一些符合实际情况的具有心理健康问题的病人和心理健康医生的多轮对话案例。要求医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。注意，构造的数据必须以医生的陈述为结束语，每次只需要构造一个案例并且不需要写案例一、二等等，请返回完整的对话内容。请以如下格式返回生成的数据：
病人：病人的咨询或陈述
医生：医生的安抚和建议'''

messages = getText('user', prompt)
temperature = random.uniform(0.1, 0.9)

response = client.chat.completions.create(
    model='glm-4',
    messages=messages,
    temperature=round(temperature, 1),
)

answer = response.choices[0].message.content

print(answer)
