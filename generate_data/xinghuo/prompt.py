import json
import random
import re
import copy
# new_data = [{'role': 'user', 'content': '你好'}, {'role': 'assistant', 'content': '你好！有什么我可以帮助您的吗？'}, {'role': 'user', 'content': '生成一段心理医生和病人的对话'}, {'role': 'assistant', 'content': '心理医生：你好，我是你的心理医生。请问你的名字是？\n\n病人：我叫李明。\n\n心理医生：很高兴见到你，李明先生。你来咨询是因为什么问题呢？\n\n病人：最近我总是感觉很焦虑，睡眠也不好。\n\n心理医生：好的，可以跟我具体说说你的情况吗？你有什么压力或者担忧的事情吗？\n\n病人：其实我一直在担心工作上的表现，觉得自己做得不够好，还有家庭的问题。\n\n心理医生：这些都是很常见的问题。你可以告诉我你在工作中遇到了什么困难吗？我们可以一起探讨一下如何解决。\n\n病人：我觉得自己的工作能力不够强，经常被领导批评。而且我家里的情况也不是很好，父母经常吵架，让我很难受。\n\n心理医生：我理解你的感受。这些问题确实会让人感到压力和焦虑。不过我们可以通过一些方法来缓解这种情况。比如说，你可以尝试一些放松的活动，比如瑜伽或者冥想，来减轻压力和焦虑。同时，你也可以考虑寻求家人或者朋友的帮助，让他们给你提供一些支持和鼓励。\n\n病人：好的，我会试试的。谢谢你的建议。\n\n心理医生：不用客气，如果你有任何问题或者需要进一步的帮助，随时可以联系我。'}]
# text2 = []
# data = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
# for val in new_data:
#     if val['role'] == 'user':
#         continue
#
#     print(text2)

def save_jsonl(conversations, path_file):
    # 把对话写入文件
    with open(path_file, 'a+', encoding='utf-8') as f:
        for conversation in conversations:
            Json_String = json.dumps(conversation, ensure_ascii=False) + '\n'
            f.write(Json_String)


# 生成输入提示词
def prompt(life_type=0):
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
        "痛苦",
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
        "学业（小学，初中，高中，大学，研究生，博士）",
        "生活（衣，食，住，行等等）",
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

    # 输入数据处理
    if life_type < 0:
        raise ValueError('life_type must > 0')
    
    emo = random.choice(emotions_lis)
    life_type %= 16

    Input = f'''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的专家，请你构造一些符合实际情况的具有心理健
    康问题的病人和心理健康医生的连续的一段多轮对话记录。要求病人的问题属于{areas_of_life[life_type]}场景，具有{emo}情感，医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。注意，构造的数据必须以医生的陈述为结束语，请只返回完整的对话内容。请以如下格式返回生成的数据：
    病人：病人的咨询或陈述 
    医生：医生的安抚和建议
    '''
    return Input

def xinghuo_api(content):
    # 对话格式
    conversation1 = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
    conversation = {'input':'', 'output':''}
    conversations = {'conversation':[]}
    # temp = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
    # 划分对话形式
    dialogue = re.split('医生：|病人：', content)
    # 对话前的数据处理
    if dialogue[0] == '':
        dialogue.pop(0)
    # 一次对话
    flag = False
    for ind, item in enumerate(dialogue):
        if flag == False:
            if (ind + 1) % 2 == 1:
                conversation1['input'] = dialogue[ind]
            else:
                conversation1['output'] = dialogue[ind]

            if (ind + 1) % 2 == 0 or ind + 1 == len(dialogue):
                temp = copy.deepcopy(conversation1)
                conversations['conversation'].append(temp)
                flag = True
                continue

        else:
            if (ind+1)%2 == 1:
                conversation['input'] = dialogue[ind]
            else:
                conversation['output'] = dialogue[ind]
        if (ind+1)%2 == 0 or ind+1 == len(dialogue):
                # 浅赋值只会是同一个变量，必须要copy.deepcopy
                # 若conversations['conversation'].append(conversation)后面改的话，~s里面的conversation也会改动
                # 就会变成n个一样的数据（这是我们不想看到的）
                temp = copy.deepcopy(conversation)
                conversations['conversation'].append(temp)

    return conversations

def ChatGLM3_6B(content):
    # 对话格式
    conversation = {'system': '现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input': '',
                     'output': ''}
    conversations = []
    # temp = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
    # 划分对话形式
    dialogue = re.split('医生：|病人：', content)
    # 对话前的数据处理
    if dialogue[0] == '':
        dialogue.pop(0)
    # 一次对话
    for ind, item in enumerate(dialogue):
        if (ind + 1) % 2 == 1:
            conversation['input'] = dialogue[ind]
        else:
            conversation['output'] = dialogue[ind]
        if (ind + 1) % 2 == 0 or ind + 1 == len(dialogue):
            # 浅赋值只会是同一个变量，必须要copy.deepcopy
            # 若conversations['conversation'].append(conversation)后面改的话，~s里面的conversation也会改动
            # 就会变成n个一样的数据（这是我们不想看到的）
            temp = copy.deepcopy(conversation)
            conversations.append(temp)

    return conversations