import json
from tqdm import tqdm


def qwen_api(prompt):
    import dashscope
    from http import HTTPStatus

    dashscope.api_key = "your key"
    prompt = "你是一位非常擅长将英文翻译成中文的专家。请你将下面的英文翻译成正确地道的中文，要求只返回翻译的中文句子:\n" + prompt
    response = dashscope.Generation.call(
        model='qwen-max',
        prompt=prompt,
        history=[],
    )

    if response.status_code == HTTPStatus.OK:
        result = response.output.text
        # print(result)
    else:
        result = 'ERROR'
    return result


def get_conversation_list():
    with open('./ESConv.json', 'rt', encoding='utf-8') as file:
        data = json.load(file)

    idx = 0
    conversation_list = []
    for itm in tqdm(data):
        one_conversation = {
            "conversation": []
        }
        dia_tuple = []
        for dia in tqdm(itm['dialog']):
            # print(dia['speaker'], dia['content'])
            if dia['speaker'] == 'seeker':
                dia_tuple.append(qwen_api(dia['content']))
            elif dia['speaker'] == 'supporter':
                dia_tuple.append(qwen_api(dia['content']))
            else:
                exit("不存在角色!")

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

        conversation_list.append(one_conversation)
        idx += 1

        # if (idx == 1):
        #     print(conversation_list)
        #     break
        print(idx)
    return conversation_list


if __name__ == '__main__':
    conversation_list = get_conversation_list()
    # 将conversation_list保存为一个json文件
    with open('conversation_list.json', 'wt', encoding='utf-8') as f:
        json.dump(conversation_list, f, ensure_ascii=False)
