import json
import os

# 打开JSON文件并读取其内容
directory_path = '../初步清洗的QA数据'

system = "你由EmoLLM团队打造的心理健康助手，是一个研究过无数具有心理健康问题的病人与心理健康医生对话的心理专家, 在心理方面拥有广博的知识储备和丰富的研究咨询经验。请充分利用专业心理学知识，对用户提出的问题进行回答。"

format2_data = []
# 遍历指定目录下的所有文件
for filename in os.listdir(directory_path):
    for root, dirs, files in os.walk(directory_path):
        # 遍历当前文件夹下的文件
        for filename in files:
            # 检查文件扩展名是否为.json
            if filename.endswith('.json'):
                # 构建文件的完整路径
                file_path = os.path.join(root, filename)
                with open(file_path, 'rt', encoding='utf-8') as file:
                    format1_data = json.load(file)
                for item in format1_data:
                    conversation = {
                        "system": system,
                        "input": item["prompt"],
                        "output": item["completion"]
                    }
                    format2_data.append({"conversation": [conversation]})


with open(f'processed_Book_QA.json', 'wt', encoding='utf-8') as file:
    json.dump(format2_data, file, ensure_ascii=False, indent=4)

