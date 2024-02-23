import json
import os


def save_merge_json(data_lis, file_path):
    import json

    with open(file_path, 'wt', encoding='utf-8') as file:
        json.dump(data_lis, file, ensure_ascii=False)


def get_all_file_paths(folder_path):
    # 确保传入的是一个目录
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid directory")

    # 获取文件夹下所有文件的路径
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(
        folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    return file_paths


if __name__ == '__main__':
    conversion_lis = []

    for path in get_all_file_paths(r'data\res-aiwei'):
        print(path)

        with open(path, 'rt', encoding='utf-8') as file:
            for line in file:
                # 移除行尾的换行符
                line = line.rstrip('\n')
                # 解析JSON
                try:
                    data = json.loads(line)
                    conversion_lis.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        save_merge_json(data_lis=conversion_lis,
                        file_path=r'.\merge.json')
