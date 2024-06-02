import json
import jsonlines


def convert_json_to_jsonl(json_file, jsonl_file):
    with open(json_file, 'r',encoding='utf-8') as file:
        data = json.load(file)

        # 将原始数据转换为所需的格式
        converted_data = []
        for conversation_data in data:
            for i, conversation in enumerate(conversation_data["conversation"]):
                history = []
                if i == 0:
                    query = conversation["input"]
                    response = conversation["output"]
                    # history = []
                else:
                    history.append({"query": conversation["input"], "response": conversation["output"]})
                converted_data.append({
                    "query": query,
                    "response": response,
                    "history": history
                })

        # 输出到JSON Lines格式的文件
        # with open('converted.jsonl', 'w', encoding='utf-8') as f:
        #     for item in converted_data:
        #         f.write(json.dumps(item, ensure_ascii=False) + '\n')

        # 输出到JSON Lines格式的文件
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for item in converted_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

convert_json_to_jsonl('aiwei.json','aiwei.jsonl')
