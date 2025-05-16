# 对文本类的（非QA对）数据做切分 --- 使用qwen的api对书籍进行语义分割
import json
import random
import argparse
import yaml
import re
import copy

from tqdm import tqdm

# config.yml文件由自己定义
with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

def qwen_api(content):
    import dashscope
    from http import HTTPStatus

    Input = '''我们的分割要求是每一个划分占一行，请你帮我将下列txt文本按照书本的内容（比如：事件的背景，心理学名词的定义，特点，阶段划分，实验内容等）进行划分，要求文本内容不能缩减，也可以按照语义分割，比如某几句话都是讲的一回事就划分一行，要求划分之后的文本内容详细，主题明确，要求每一个划分仅用一行表示。以下为要求分割的txt文本：{}
        '''.format(content)

    dashscope.api_key = configs['dashscope_api_key']
    response = dashscope.Generation.call(
        model='qwen-max',
        prompt=Input,
        history=[],
    )

    if response.status_code == HTTPStatus.OK:
        result = response.output.text
        print(result)
    else:
        result = 'ERROR'
    return result


def save_jsonl(data_lis, file_path):
    import json

    # 将字典列表写入文件，每一行一个字典
    with open(file_path, 'at', encoding='utf-8') as file:
        for item in data_lis:
            json_string = json.dumps(item, ensure_ascii=False) + '\n'
            file.write(json_string)


if __name__ == '__main__':
    file_name = 'a0.jsonl'
    conversations = []
    path = configs['txt_path']
    f = open(path, 'r', encoding='utf-8')
    str = f.read()
    f.close()
    for i in tqdm(range(0, len(str), 2500)):
        # 保证所有文本都能按照完整的语义进行分割
        content = str[i:i+3500]
        print(content)
        answer = qwen_api(content)

        f2 = open('seg1.txt', 'a', encoding='utf-8')
        f2.write(answer)
        f2.close()