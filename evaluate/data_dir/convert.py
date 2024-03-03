import ujson
def transform_conversation_data(raw_data):
    try:
        instruction = raw_data.get("conversation", "")[0]['system'] + "\n\n对话："

        conversation = raw_data.get("conversation", [])
        for i, dialog in enumerate(conversation):
            instruction += "\n来访者：" + dialog["input"]

            if i < len(conversation) - 1:
                instruction += "\n医生：" + dialog["output"]

        response = conversation[-1]["output"] if conversation else ""

        instruction += "\n医生："

        return {"instruction": instruction, "output": response}
    
    except Exception as e:
        pass


with open(f'./train_dir/data.json', 'r', encoding='utf-8') as f1:
    data = ujson.load(f1)
with open(f'./train_dir/converted.json', 'w', encoding='utf-8') as f:
    for j, item in enumerate(data):
        temp=transform_conversation_data(item)
        if temp:
            transformed_data =ujson.dumps(temp, ensure_ascii=False)
            f.write(transformed_data+'\n')
    print('********')