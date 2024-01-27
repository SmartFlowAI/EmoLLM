import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from openxlab.model import download

download(model_repo='jujimeizuo/EmoLLM_Model', 
        output='model')

model_name_or_path = "model"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
model = model.eval()

system_prompt = "你是一个由aJupyter、Farewell、jujimeizuo、Smiling&Weeping研发（排名按字母顺序排序，不分先后）、散步提供技术支持、上海人工智能实验室提供支持开发的心理健康大模型。现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。"

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:
    input_text = input("User  >>> ")
    input_text.replace(' ', '')
    if input_text == "exit":
        break
    response, history = model.chat(tokenizer, input_text, history=messages)
    messages.append((input_text, response))
    print(f"robot >>> {response}")