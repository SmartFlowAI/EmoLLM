import json

# 打开JSON文件并读取其内容

file_name = '../ruozhiba_raw.jsonl' 

# with open(f'data/{file_name}', 'r', encoding='utf-8') as file:
#     data = json.load(file)

n = 0
datas = []
format0 = '''
    {
        "conversation": [
            {
                "input": "",
                "output": "",
                "system": ""
            }
        ]
    }
'''
with open(f'data/{file_name}', 'r', encoding='utf-8') as f:
    for line in f:
        json_data = json.loads(line.strip())

        dict_ = dict()
        # dict_['conversation'] = i
        # print(dict_)
        try:
            dict_['conversation']= [format0]
            dict_['conversation'][0]['input'] = json_data['instruction']
            dict_['conversation'][0]['output'] = json_data['output']
            dict_['conversation'][0]['system'] = "你是心理健康助手EmoLLM, 由EmoLLM团队打造, 是一个研究过无数具有心理健康问题的病人与心理健康医生对话的心理专家, 在心理方面拥有广博的知识储备和丰富的研究咨询经验。你旨在通过专业心理咨询, 协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术, 一步步帮助来访者解决心理问题。"

            dict_['conversation'][0].pop('instruction')
            print(dict_)
            datas.append(dict_)
        except:
            print(n,line)   # 4 empty lines in data.json 425 483 742 1120 
        n+=1
        break

# with open(f'data/processed_{file_name}', 'wt', encoding='utf-8') as file:
#     json.dump(datas, file, ensure_ascii=False, indent=4)

print(datas[0])
# print(datas[1])