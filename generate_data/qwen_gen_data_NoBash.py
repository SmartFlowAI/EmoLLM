# -*- coding: utf-8 -*-  
import json
import random
import argparse
import yaml 
import re
import os
import json

from tqdm import tqdm
import dashscope
from http import HTTPStatus

with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

def qwen_api(data, emo):
    dashscope.api_key = configs['dashscope_api_key']   
    prompt = f'''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的专家，请你构造一些符合实际情况的具有心理健康问题的病人和心理健康医生的连续的多轮对话记录。
    要求病人的问题属于{data}场景，具有{emo}情感，医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。
    注意，构造的数据必须以医生的陈述为结束语，每次只需要构造一个案例并且不需要写案例一、二等等，请返回完整的对话内容。
    请以如下格式返回生成的数据：
    病人：病人的咨询或陈述 
    医生：医生的安抚和建议
    '''
    try:
        response = dashscope.Generation.call(
        model='qwen-max',
        prompt=prompt,
        history=[],
    )
    except:
        response = dashscope.Generation.call(
        model='qwen-max',
        prompt=prompt,
        history=[],
    )

    if response.status_code == HTTPStatus.OK:
        result = response.output.text
        print(result)
    else:
        result = 'ERROR'
    return result


def save_jsonl(data_lis, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'at', encoding='utf-8') as f:
        for item in data_lis:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='数据生成参数')

    parser.add_argument('--data', type=str, help='生活场景')

    emotions_lis = configs['emotions_list']
    areas_of_life = configs['areas_of_life']
    ai_tool = 'qwen'
    
    save_interval = 5
    total_num_each_emo_area = 5

    conversation_lis = []

    for area in areas_of_life:
        for emo in emotions_lis:
            gen_path = f'./{ai_tool}/{area}/{emo}.jsonl'
            
            for i in tqdm(range(total_num_each_emo_area), desc='{emo}, {area}'.format(emo=emo, area=area)):
                one_conversation = {
                    "conversation": []
                }

                res = qwen_api(data=area, emo=emo)
                print(area, emo)

                # 一次会话
                doctor_pattern = r'医生：(.*?)(病人：|$)'

                doctor_matches = re.findall(doctor_pattern, res, re.DOTALL)
                doctor_conversations = [match[0] for match in doctor_matches]

                patient_pattern = r'病人：(.*?)医生：'
                patient_matches = re.findall(patient_pattern, res, re.DOTALL)
                patient_conversations = [match for match in patient_matches]

                for doc, pat in zip(doctor_conversations, patient_conversations):
                    if len(one_conversation['conversation']) == 0:
                        one_conversation['conversation'].append(
                            {
                                "system": "现在你是一个心理专家, 我有一些心理问题, 请你用专业的知识帮我解决。",
                                "input": pat,
                                "output": doc
                            },
                        )

                    else:
                        one_conversation['conversation'].append(
                            {
                                "input": pat,
                                "output": doc
                            },
                        )
                conversation_lis.append(one_conversation)

                if ((i+1) % save_interval == 0):
                    save_jsonl(data_lis=conversation_lis, file_path=gen_path)
                    print(f'generate {gen_path}')
                    conversation_lis = []  # 清空
