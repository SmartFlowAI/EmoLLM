import json
import os


def save_merge_json(data_lis, file_path):
    with open(file_path, 'wt', encoding='utf-8') as file:
        json.dump(data_lis, file, indent=4, ensure_ascii=False)


def get_all_file_paths(folder_path, suffix=''):
    print(folder_path)
    files = os.listdir(folder_path)
    path = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            path.extend(get_all_file_paths(file_path))
        else:
            if file_path.endswith(suffix):
                path.append(file_path)
    return path


if __name__ == '__main__':
    conversion_lis = []
    folder_path = './' # input
    merge_path = 'merge.json' # input
    paths = get_all_file_paths(folder_path=folder_path, suffix='.json')

    for path in paths:
        print(path)
        with open(path, 'rt', encoding='utf-8') as lines:
            datas = []
            for line in lines:
                datas.append(line)
            try:
                datas = json.loads(''.join(datas))
                conversion_lis.extend(datas)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        save_merge_json(data_lis=conversion_lis, file_path=merge_path)