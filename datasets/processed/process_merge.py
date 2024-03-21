import os
import json

# 设置目录路径，这里假设你的JSON文件都在当前目录下的directory_path文件夹中
directory_path = './'

# 初始化一个空列表，用于存储所有JSON文件的数据
combined_list = []

# 遍历指定目录下的所有文件
for filename in os.listdir(directory_path):
    # 检查文件扩展名是否为.json
    if filename.endswith('.json'):
        # 构建文件的完整路径
        file_path = os.path.join(directory_path, filename)
        
        # 打开并读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as json_file:
            # 加载JSON文件的内容
            data = json.load(json_file)
            
            # 将读取到的数据添加到combined_list中
            # 假设每个JSON文件包含的是一个列表，如果不是，可以根据实际情况调整
            if isinstance(data, list):
                combined_list.extend(data)
            else:
                combined_list.append(data)

# 打印合并后的列表 very large and slow
# print(combined_list)

# 如果需要，可以将合并后的列表保存到一个新的JSON文件中
with open('combined_data.json', 'w', encoding='utf-8') as combined_json_file:
    json.dump(combined_list, combined_json_file, ensure_ascii=False, indent=4)
