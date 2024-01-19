import json
import os


def save_merge_json(data_lis, file_path):
    with open(file_path, 'wt', encoding='utf-8') as file:
        json.dump(data_lis, file, indent=4, ensure_ascii=False)


def get_all_file_paths(folder_path):
    files = os.listdir(folder_path)
    path = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            path.extend(get_all_file_paths(file_path))
        else:
            path.append(file_path)
    return path


if __name__ == '__main__':
    conversion_lis = []
    folder_path = '' # input
    merge_path = '' # input
    paths = get_all_file_paths(folder_path=folder_path)

    for path in paths:
        print(path)
        with open(path, 'rt', encoding='utf-8') as lines:
            for line in lines:
                # 移除行尾的换行符
                line.rstrip('\n')
                # 解析JSON
                try:
                    data = json.loads(line)
                    conversion_lis.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        save_merge_json(data_lis=conversion_lis, file_path=merge_path)