# EmoLLM通用指标评估

## 简介

本文档提供了关于如何使用 `eval.py` 和 `metric.py` 两个脚本的指导。这些脚本用于评估 EmoLLM-心理健康大模型的生成结果。

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

对data.json中的数据进行测试，结果如下：

| Model    | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU-1  | BLEU-2  | BLEU-3  | BLEU-4  |
|----------|---------|---------|---------|---------|---------|---------|---------|
| Qwen1_5-0_5B-chat | 27.23%  | 8.55%   | 17.05%  | 26.65%  | 13.11%  | 7.19%   | 4.05%   |
| InternLM2_7B_chat_qlora | 37.86%  | 15.23%   | 24.34%  | 39.71%  | 22.66%  | 14.26%   | 9.21%   |
| InternLM2_7B_chat_full  | 32.45%  | 10.82%   | 20.17%  | 30.48%  | 15.67%  | 8.84%   | 5.02%   |
| InternLM2_7B_base_qlora_5epoch  | 41.94%  | 20.21%   | 29.67%  | 42.98%  | 27.07%  | 19.33%   | 14.62%   |
| InternLM2_7B_base_qlora_10epoch | 43.47%  | 22.06%   | 31.4%  | 44.81%  | 29.15%  | 21.44%   | 16.72%   |