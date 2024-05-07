# 将微调的数据格式转为预训练的格式
import json


def convert(data_path:str, target_path:str):
    # 假设原始JSON数据存储在名为'data.json'的文件中
    filename = data_path

    # 读取文件内容
    with open(filename, 'rt', encoding='utf-8') as file:
        original_json = file.read()

    # 将原始JSON字符串解析为Python对象
    data = json.loads(original_json)

    # 遍历每个对话
    converted_data = []

    # 遍历原始数据中的每个对话对象
    for conversation_group in data:
        # 遍历每个对话
        for dialog in conversation_group["conversation"]:
            # 创建一个新的对话对象，用于存储转换后的对话
            new_conversation_group = {
                "conversation": []
            }
            # 创建一个新的对话，其中输出被替换为"xxx"
            new_dialog = {
                "input": '',
                "output": f'问题:{dialog["input"]}\n答案:{dialog["output"]}',
            }
            # 将新的对话添加到新对话对象的列表中
            new_conversation_group["conversation"].append(new_dialog)
            
            # 将新对话对象添加到转换后的数据列表中
            converted_data.append(new_conversation_group)


    # 将更新后的数据转换回JSON字符串，并格式化输出
    updated_json = json.dumps(converted_data, indent=4, ensure_ascii=False)


    # 将更新后的JSON数据写入到新的文件中
    with open(f'{target_path}', 'wt', encoding='utf-8') as file:
        file.write(updated_json)

if __name__ == '__main__':
    convert(data_path='./output2.json', target_path='pt.json')