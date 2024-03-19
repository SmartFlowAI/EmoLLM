# -*- coding: utf-8 -*-  

import json
import os


def save_merge_json(data_lis, file_path):
    with open(file_path, 'wt', encoding='utf-8') as file:
        json.dump(data_lis, file, ensure_ascii=False, separators=(',\n',':'))


def get_all_file_paths(folder_path, file_type='.jsonl'):
    # 确保传入的是一个目录
    if not os.path.isdir(folder_path):
        raise ValueError(f"{folder_path} is not a valid directory")

    # 获取文件夹下所有文件的路径
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(
        folder_path) if os.path.isfile(os.path.join(folder_path, file)) and (file_type in file)]
    return file_paths


if __name__ == '__main__':
    
    data_ai = 'qwen'  # python merge_jsonl_r.py > qwen.txt
    # data_ai = 'zhipuai'  # python merge_jsonl_r.py > zhipuai.txt
    root_dir  = rf'./{data_ai}/'
    
    save_final_merge_json_path = f'{data_ai}_final_merge.json'

    subfolders = [os.path.join(root_dir, d) for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    final_list = []
    for folder_path in subfolders:
        conversion_lis = []
        merge_path = folder_path.split('/')[-1]
        try:
            merge_last_path = folder_path.split('/')[-2] if folder_path.split('/')[-2]!='.' else ''
        except:
            merge_last_path = '' 
        print(f'merge_path={merge_path},merge_last_path={merge_last_path}'.encode("utf-8"))
            

        for path in get_all_file_paths(folder_path):
            print(path.encode("utf-8"))

            with open(path, 'rt', encoding='utf-8') as file:
                for line in file:
                    # # 移除行尾的换行符
                    # if line == '\n':
                    #     line = line.rstrip('\n')
                    line = line.rstrip('\n')
                    # 解析JSON
                    try:
                        data = json.loads(line)
                        conversion_lis.append(data)
                        # conversion_lis.append('\n')
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        
            if merge_last_path!='':
                save_merge_json_path = rf'./{merge_last_path}/{merge_path}_merge.json'  
            elif merge_path!='':
                save_merge_json_path = rf'./{merge_path}_merge.json'
            else:
                save_merge_json_path = rf'./curr_merge.json'
                            
            save_merge_json(data_lis=conversion_lis,
                            file_path=save_merge_json_path)
        
        final_list = final_list+conversion_lis
        print(f'{len(conversion_lis)},{len(final_list)},{save_merge_json_path}'.encode("utf-8"))
        
    save_merge_json(data_lis=final_list,file_path=save_final_merge_json_path)
    print(len(conversion_lis),save_final_merge_json_path.encode("utf-8"))
        
        
