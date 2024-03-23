import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from openxlab.model import download
from modelscope import snapshot_download

# download model in openxlab
model_name_or_path =download(model_repo='ajupyter/EmoLLM_internlm2_7b_full', 
        output='EmoLLM_internlm2_7b_full')

# download model in modelscope
model_name_or_path = snapshot_download('chg0901/EmoLLM-InternLM7B-base')

# offline model
# model_name_or_path = "/root/StableCascade/emollm2/EmoLLM/xtuner_config/merged"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
model = model.eval()

system_prompt = '你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。'

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