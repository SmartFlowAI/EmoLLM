import json

# 打开JSON文件并读取其内容
with open('/root/Emollm/datasets/multi_turn_dataset_2.json', 'rt', encoding='utf-8') as file:
    data = json.load(file)

n = 0
for i in data:
    i['conversation'][0]['system'] = "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。"

with open('output2.json', 'wt', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
