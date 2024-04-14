import os
import re
import json
import glob
from typing import List, Dict

from config.config import data_dir, judge_dir
from util.logger import get_logger

logger = get_logger()


"""
递归获取 数据整合 下的所有 .jsonl 文件列表
"""
def get_jsonl_file_paths() -> List[str]:
    json_file_paths = []

    # 遍历根目录及其所有子目录
    for dirpath, dirnames, filenames in os.walk(judge_dir):
        # 对每个文件进行检查
        for filename in filenames:
            # 使用正则表达式匹配以.jsonl结尾的文件名
            if re.search(r'\.jsonl$', filename):
                # 构建完整的文件路径并添加到列表中
                json_file_path = os.path.join(dirpath, filename)
                json_file_paths.append(json_file_path)

    return json_file_paths

def get_QA_pairs(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 按照换行符分割字符串
    QA_Pairs = content.split('\n')

    return QA_Pairs

"""
递归获取 data_dir 下的所有 .txt 文件列表
"""
def get_file_list() -> List[str]:
    txt_files = []
    txt_exist_flag = False
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.txt'):
                txt_exist_flag = True
                txt_files.append(os.path.join(root, file))

    if not txt_exist_flag:
        logger.warning(f'No txt text found in {data_dir}, please check!')
    return txt_files

"""
获取 txt 文本的所有内容，按句子返回 List
file_path: txt 文本路径
window_size: 滑窗大小，单位为句子数
overlap_size: 重叠大小，单位为句子数
"""
def get_txt_content(
    file_path: str,
    window_size: int = 6,
    overlap_size: int = 2
) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 简单实现：按句号、感叹号、问号分割，并去除句内空白符
    sentences = re.split(r'(?<=[。！？])\s+', content)
    sentences = [s.replace(' ', '').replace('\t', '') for s in sentences]

    # 滑窗
    res = []
    sentences_amount = len(sentences)
    start_index, end_index = 0, sentences_amount - window_size
    # check length
    if window_size < overlap_size:
        logger.error("window_size must be greater than or equal to overlap_size")
        return None
    if window_size >= sentences_amount:
        logger.warning("window_size exceeds the amount of sentences, and the complete text content will be returned")
        return ['\n'.join(sentences)]
    
    for i in range(start_index, end_index + 1, overlap_size):
        res.append('\n'.join(sentences[i: i + window_size]))
    return res


"""
提取返回的 QA 对
"""
def capture_qa(content: str) -> List[Dict]:
    # 只捕获第一个 json 块
    match = re.search(r'```json(.*?)```', content, re.DOTALL)

    if match:
        parsed_data = None
        block = match.group(1)
        try:
            parsed_data = json.loads(block)
        except:
            logger.warning('Unable to parse JSON properly.')
        finally:
            return parsed_data
    else:
        logger.warning("No JSON block found.")
        return None


"""
将 storage_list 存入到 storage_jsonl_path
"""
def save_to_file(storage_jsonl_path, storage_list):
    with open(storage_jsonl_path, 'a', encoding='utf-8') as f:
        for item in storage_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

import time
import os

def safe_remove(file_path, max_attempts=5, delay=1):
    for attempt in range(max_attempts):
        try:
            os.remove(file_path)
            print(f"File {file_path} successfully deleted.")
            break
        except PermissionError as e:
            print(f"Attempt {attempt+1}: Unable to delete {file_path} - {str(e)}")
            time.sleep(delay)
    else:
        print(f"Failed to delete {file_path} after {max_attempts} attempts.")

"""
将并发产生的文件合并成为一个文件
"""
def merge_sub_qa_generation(directory, storage_jsonl_path):

    # 查找以指定前缀开始的所有文件
    matching_files = glob.glob(os.path.join(directory, storage_jsonl_path + "*"))
    
    file_contents = []
    for file_path in matching_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                file_contents.append(json.loads(line))
            # safe_remove(file_path)
    save_to_file(storage_jsonl_path, file_contents)