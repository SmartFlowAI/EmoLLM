import json
from loguru import logger
import os
from datasketch import MinHash
from hashlib import md5

def is_json_file(filename):
    return filename.endswith('.json')

# 绝对匹配
def is_duplicate_absolutely(d1, d2):
    return md5(d1.encode('utf-8')).hexdigest() == md5(d2.encode('utf-8')).hexdigest()

# 使用MinHash生成器计算dict的签名
def hash_dict(dict_obj):
    m = MinHash()
    for key, value in sorted(dict_obj.items()):
        # 对于非str类型值需要先转为str
        m.update(str(value).encode('utf8'))
    return m

# 使用绝对匹配和MinHash对dict列表去重
def deduplicate_json(data_list, threshold=0.8):
    seen_hashes = []
    duplicates_removed = []

    for item in data_list:
        # print(item)
        # print('###########')
        min_hash = hash_dict(item)
        # print(f'min_hash: {min_hash}')

        # 绝对匹配去重
        if not any(is_duplicate_absolutely(str(item), str(existing)) for existing in duplicates_removed):
            # MinHash相似性去重 
            has_similar = False
            for stored_min_hash, stored_text in seen_hashes:
                if stored_min_hash.jaccard(min_hash) > threshold:
                    has_similar = True
                    break
            if not has_similar:
                seen_hashes.append((min_hash,item))
                duplicates_removed.append(item)
           

    return duplicates_removed

if __name__ == '__main__':    
    data_ai = 'qwen'  
    root_dir  = rf'./{data_ai}/'
    dedup_output_dir = os.path.join(root_dir,'dedup')
    if not os.path.exists(dedup_output_dir):
        os.mkdir(dedup_output_dir)
    if not os.path.exists(root_dir):
        logger.error(f"folder {root_dir} not exist" )
        
    else:    
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if os.path.isfile(file_path):
                print(f'file name: {file_path}')
                if is_json_file(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        dedup_data = deduplicate_json(data)                   
                    with open(os.path.join(root_dir, 'dedup','dedup_' + file), 'w', encoding='utf-8') as output_file:
                        json.dump(dedup_data, output_file, ensure_ascii=False, indent=4)
                