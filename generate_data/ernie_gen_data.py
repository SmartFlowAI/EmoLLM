import json
import random
import yaml 
import erniebot
with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

erniebot.api_type = 'aistudio'
#此处需要将你的token也就是AIstudio主页的访问令牌放到下方
erniebot.access_token = configs['aistudio _token']
system = configs['system']
areas_of_life = configs['areas_of_life']
emotions_list = configs['emotions_list']
words = ''
# prompt = '''
# 你是一个研究过无数具有心理健康问题的病人与心理健康医生对话案例的专家，请你构造一些符合实际情况的具有心理健康问题的病人和心理健康医生的多轮对话案例。要求医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。注意，构造的数据必须以医生的陈述为结束语。请以如下格式返回生成的数据：
# 病人：病人的咨询或陈述
# 医生：医生的安抚和建议
# '''

for data in areas_of_life:
    for emo in emotions_list:
        res = []
        print(f'正在为{data}_{emo}场景生成对应数据集')
        
        prompt = f'''你是一个研究过无数具有心理健康问题的病人与心理健康医生对话的专家，请你构造一些符合实际情况的具有心理健康问题的病人和心理健康医生的连续的多轮对话记录。
        要求病人的问题属于{data}场景，具有{emo}情感，医生的回复尽可能包含心理辅导知识，并且能够一步步诱导病人说出自己的问题进而提供解决问题的可行方案。
        注意，构造的数据必须以医生的陈述为结束语，每次只需要构造一个案例并且不需要写案例一、二等等，请返回完整的对话内容。
        请以如下格式返回生成的数据：
        病人：病人的咨询或陈述 
        医生：医生的安抚和建议
        '''
        for i in range(15):
            response = erniebot.ChatCompletion.create(
                model='ernie-3.5',
                messages=[{'role': 'user', 'content': f"{prompt}"}],
                # top_p=random.uniform(0.5, 0.99),
                # penalty_score = random.uniform(1.0, 2.0)
            )
            tmp = response.result
            print(tmp)
            ls = tmp.split('\n')
            conversation = {'conversation':[]}
            for j in range(0, len(ls)-1, 2):
                # print(j)
                q_a = {}
                if j == 0:
                    q_a = {'system':system, 'input':ls[j].split("：")[-1], 'output':ls[j+1].split("：")[-1]}
                else:
                    q_a = {'input':ls[j].split("：")[-1], 'output':ls[j+1].split("：")[-1]}
                # print(q_a)
                conversation['conversation'].append(q_a)
            res.append(conversation)
        print(f'第{i}条数据生成完成！！')
    print('================================')
    print(f'{data}_{emo}场景对应数据集生成完毕')
    # 将数据写入JSON文件  
    
    with open('./data/Ernie_{data}_{emo}.json', 'w', encoding='utf-8') as file:  
        json.dump(res, file, ensure_ascii=False, indent=4)
