from split_dataset import split_data
# 输入文件路径和输出文件路径
# input_jsonl_path = 'processed/ruozhiba_format_emo_sc.jsonl'
# train_jsonl_path = 'processed/ruozhiba_format_emo_sc_shuffle.jsonl'
# test_jsonl_path = 'processed/ruozhi-train_sc_emo_shuffle0.jsonl'

input_jsonl_path = 'processed/combined_data.json'
train_jsonl_path = 'processed/combined_sc_ruozhi.jsonl'
test_jsonl_path = 'processed/test_emo.jsonl0'

# 省略split_data函数
# ......... # 采用函数调用

# split_ratio 为1的时候, 实际上就是把input_jsonl shuffle成train_jsonl
split_data(input_jsonl_path, train_jsonl_path, test_jsonl_path, split_ratio=1)