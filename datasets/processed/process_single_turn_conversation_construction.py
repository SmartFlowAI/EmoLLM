import json

# 打开JSON文件并读取其内容
file_name = 'single_turn_dataset_1.json'
# file_name = 'single_turn_dataset_2.json'
with open(f'E:\LLM\EmoLLM\datasets\\{file_name}', 'rt', encoding='utf-8') as file:
    format1_data = json.load(file)

system = "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。"

# 转换为格式2的数据
format2_data = []
for item in format1_data:
    conversation = {
        "system": system,
        "input": item["prompt"],
        "output": item["completion"]
    }
    format2_data.append({"conversation": [conversation]})

# 将转换后的数据转换为JSON格式


with open(f'./processed_{file_name}', 'wt', encoding='utf-8') as file:
    json.dump(format2_data, file, ensure_ascii=False, indent=4)

print(format2_data[0])
