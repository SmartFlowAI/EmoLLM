import os
import json

def get_all_file_paths(folder_path, suffix=''):
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

def check(filepath):
    with open(path, 'rt', encoding='utf-8') as file:
        data = json.load(file)
        for idx, item in enumerate(data):
            dict_item = dict(item)
            for conversation in dict_item:
                if conversation != 'conversation':
                    return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
                try:
                    if len(dict_item[conversation]) == 0:
                        return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
                except:
                    return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
                for in_out in dict_item[conversation]:
                    for key in in_out:
                        if key != 'system' and key != 'input' and key != 'output':
                            return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
                        try :
                            if len(in_out[key]) == 0:
                                return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
                        except:
                            return 'found error in file: ' + filepath + ' at conversation index: ' + str(idx)
    return 'no error in file: ' + filepath


if __name__ == '__main__':
    dir_path = '.'
    paths = get_all_file_paths(dir_path, suffix='.json')
    for path in paths:
         print(check(filepath=path))