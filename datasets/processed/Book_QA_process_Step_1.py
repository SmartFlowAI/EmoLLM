import os
import json

# 设置目录路径，这里假设你的 .jsonl 文件都在当前目录下的directory_path文件夹中
directory_path = '../初步清洗的QA数据'


def convert_to_desired_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    transformed_data = []
    for entry in data:
        transformed_entry = {
            "prompt": entry["question"],
            "completion": entry["answer"]
        }
        transformed_data.append(transformed_entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=4)


# 遍历指定目录下的所有文件
for filename in os.listdir(directory_path):
    for root, dirs, files in os.walk(directory_path):
        # 遍历当前文件夹下的文件
        for filename in files:
            # 检查文件扩展名是否为.json
            if filename.endswith('.jsonl'):
                # 构建文件的完整路径
                file_path = os.path.join(root, filename)
                output_file = file_path.replace('.jsonl', '.json')
                convert_to_desired_format(file_path, output_file)

