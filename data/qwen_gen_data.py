import json
import random
import argparse

from tqdm import tqdm


def qwen_api(data, emo):
    import dashscope
    from http import HTTPStatus

    dashscope.api_key = ""
    prompt = f'''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的专家，请你构造一些符合实际情况的具有心理健康问题的病
    人和心理健康医生的连续的多轮对话记录。要求病人的问题属于{data}场景，具有{emo}情感，医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。注意，构造的数据必须以医生的陈述为结束语，请只返回完整的对话内容。请以如下格式返回生成的数据：
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

    emotions_lis = [
        "钦佩",
        "崇拜",
        "欣赏",
        "娱乐",
        "焦虑",
        "敬畏",
        "尴尬",
        "厌倦",
        "冷静",
        "困惑",
        "渴望",
        "厌恶",
        "同情",
        "痛苦"
        "着迷",
        "嫉妒",
        "兴奋",
        "恐惧",
        "痛恨",
        "有趣",
        "快乐",
        "怀旧",
        "浪漫",
        "悲伤",
        "满意",
        "性欲",
        "同情",
        "满足"
    ]
    areas_of_life = [
        "工作",
        "学业",
        "生活",
        "身体",
        "家人",
        "朋友",
        "社交",
        "恋爱",
        "就业",
        "责任",
        "爱好",
        "环境",
        "隐私",
        "安全",
        "梦想",
        "自由"
    ]

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
        for itm in res.split('\n'):
            if itm.startswith("病人："):
                dia_tuple.append(itm.split("：")[1])
            elif itm.startswith("医生："):
                dia_tuple.append(itm.split("：")[1])

            if len(dia_tuple) == 2 and len(one_conversation['conversation']) == 0:
                one_conversation['conversation'].append(
                    {
                        "system": "现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。",
                        "input": dia_tuple[0],
                        "output": dia_tuple[1]
                    },
                )
                dia_tuple = []

            elif len(dia_tuple) == 2:
                one_conversation['conversation'].append(
                    {
                        "input": dia_tuple[0],
                        "output": dia_tuple[1]
                    },
                )
                dia_tuple = []
        conversation_lis.append(one_conversation)

        idx += 1

        # 每生成2条数据存储一次
        if (idx % 2 == 0):
            path = f'./{args.data}.jsonl'
            save_jsonl(data_lis=conversation_lis, file_path=path)
