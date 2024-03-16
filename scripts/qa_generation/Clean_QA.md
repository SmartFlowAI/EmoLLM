# 清洗 QA 对
调用qwen去判断当前QA对是否属于心理学范畴，去除非心理学范畴的 QA 对

## Step 1
1. 准备好需要清洗的 QA 对数据
2. 将该数据放进 model 同级 data 文件夹下
3. 根据文件夹名去修改 config/config.py 中的 judge_dir。我个人没有对文件名进行更改，所以我的judge_dir是 judge_dir = os.path.join(data_dir, '数据整合')

## Step 2
1. 运行QA_clean.py即可
2. 清洗完的 QA 对会以 jsonl 的格式存在 data/cleaned 下