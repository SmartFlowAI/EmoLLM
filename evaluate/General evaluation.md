# EmoLLM通用指标评估

## 简介

此文件提供了关于如何使用 `eval.py` 和 `metric.py` 两个脚本的指导。这些脚本用于评估 EmoLLM-心理健康大模型的生成结果。


## 安装

- Python 3.x
- PyTorch
- Transformers 
- Datasets 
- NLTK 
- Rouge 
- Jieba 

可以使用以下命令安装：

```bash
pip install torch transformers datasets nltk rouge jieba
```

## 用法

### convert.py
将原始多轮对话数据转换为测评用的单轮数据。

### eval.py

`eval.py` 脚本用于生成医生的回复并进行评估，主要分为以下几部分：

1. 加载模型和分词器。
2. 设置测试参数，如测试数据数量和批处理大小。
3. 准备数据。
4. 生成响应并评估。

### metric.py

`metric.py` 脚本包含计算评估指标的函数，可设置按字符级别或按词级别进行评估，目前包含 BLEU 和 ROUGE 分数。



## 测试结果

基于全量微调后的Qwen1_5-0_5B-Chat模型对data.json中的数据进行测试，结果如下：
| Metric  | Value                |
|---------|----------------------|
| ROUGE-1 | 27.23%               |
| ROUGE-2 | 8.55%                |
| ROUGE-L | 17.05%               |
| BLEU-1  | 26.65%               |
| BLEU-2  | 13.11%               |
| BLEU-3  | 7.19%                |
| BLEU-4  | 4.05%                |
