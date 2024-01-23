import json
import random
import argparse
import yaml 
import re

from tqdm import tqdm

with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

def qwen_api(data, emo):
    import dashscope
    from http import HTTPStatus

    dashscope.api_key = configs['dashscope_api_key']
    prompt = f'''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的专家，请你构造一些符合实际情况的具有心理健
    康问题的病人和心理健康医生的连续的多轮对话记录。要求病人的问题属于{data}场景，具有{emo}情感，医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。注意，构造的数据必须以医生的陈述为结束语，请只返回完整的对话内容。请以如下格式返回生成的数据：
    病人：病人的咨询或陈述 
    医生：医生的安抚和建议
    '''
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
    import json

    # 将字典列表写入文件，每一行一个字典
    with open(file_path, 'at', encoding='utf-8') as file:
        for item in data_lis:
            json_string = json.dumps(item, ensure_ascii=False) + '\n'
            file.write(json_string)


if __name__ == '__main__':
    idx = 0
    parser = argparse.ArgumentParser(description='数据生成参数')

    parser.add_argument('--data', type=str, help='生活场景')

    # 解析命令行参数
    args = parser.parse_args()

    emotions_lis = configs['emotions_list']
    areas_of_life = configs['areas_of_life']

    conversation_lis = []
    for i in tqdm(range(100)):
        one_conversation = {
            "conversation": []
        }

        dia_tuple = []
        emo = random.choice(emotions_lis)
        res = qwen_api(data=args.data, emo=emo)
        print(res)

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
                        "system": "现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。",
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

        idx += 1

        # 每生成10条数据存储一次
        if (idx % 10 == 0):
            path = f'./{args.data}.jsonl'
            save_jsonl(data_lis=conversation_lis, file_path=path)
            conversation_lis = []  # 清空
