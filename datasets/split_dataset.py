import json
import random

def split_data(input_file, train_file, test_file, split_ratio=0.7, seed=42):
    # 读取原始的jsonl文件
    # with open(input_file, 'r', encoding='utf-8') as f:
    #     data = [json.loads(line.strip()) for line in f]
        
    with open(input_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)

    # 设置随机种子，确保每次划分结果一致
    random.seed(seed)
    # 打乱数据
    random.shuffle(data)

    # 计算训练集和测试集的划分点
    split_point = int(len(data) * split_ratio)

    # 划分数据
    train_data = data[:split_point]
    test_data = data[split_point:]

    # # 保存训练集
    # with open(train_file, 'w', encoding='utf-8') as f_train:
    #     for d in train_data:
    #         json.dump(d, f_train, ensure_ascii=False)
    #         f_train.write('\n')

    # # 保存测试集
    # with open(test_file, 'w', encoding='utf-8') as f_test:
    #     for d in test_data:
    #         json.dump(d, f_test, ensure_ascii=False)
    #         f_test.write('\n')
    
    
    with open(train_file, 'w', encoding='utf-8') as file:
        json.dump(train_data, file, ensure_ascii=False, indent=4)
        
    with open(test_file, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, ensure_ascii=False, indent=4)
        
    print(len(data),len(train_data),len(test_data),)


def main():
    
    # 输入文件路径和输出文件路径
    input_jsonl_path = 'data/ruozhiba_format_emo.jsonl'
    train_jsonl_path = 'data/train_emo.jsonl'
    test_jsonl_path = 'data/test_emo.jsonl'

    # 划分数据集，按照7:3的比例
    split_data(input_jsonl_path, train_jsonl_path, test_jsonl_path, split_ratio=0.8)


if __name__== "__main__" :
    main()
    


