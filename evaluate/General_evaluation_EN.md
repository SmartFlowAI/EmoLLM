# EmoLLM's general evaluation

## Introduction

This document provides instructions on how to use the 'eval.py' and 'metric.py' scripts. These scripts are used to evaluate the generation results of EmoLLM- a large model of mental health.

## Installation

- Python 3.x
- PyTorch
- Transformers
- Datasets
- NLTK
- Rouge
- Jieba

It can be installed using the following command:

```bash
pip install torch transformers datasets nltk rouge jieba
```

## Usage

### convert.py

Convert raw multi-round conversation data into single round data for evaluation.

### eval.py

The `eval.py` script is used to generate the doctor's response and evaluate it, mainly divided into the following parts:

1. Load the model and word divider.
2. Set test parameters, such as the number of test data and batch size.
3. Obtain data.
4. Generate responses and evaluate.

### metric.py

The `metric.py` script contains functions to calculate evaluation metrics, which can be set to evaluate by character level or word level, currently including BLEU and ROUGE scores.

## Results

Test the data in data.json with the following results:

| Model    | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU-1  | BLEU-2  | BLEU-3  | BLEU-4  |
|----------|---------|---------|---------|---------|---------|---------|---------|
| Qwen1_5-0_5B-chat | 27.23%  | 8.55%   | 17.05%  | 26.65%  | 13.11%  | 7.19%   | 4.05%   |
| InternLM2_7B_chat_qlora | 37.86%  | 15.23%   | 24.34%  | 39.71%  | 22.66%  | 14.26%   | 9.21%   |
| InternLM2_7B_chat_full  | 32.45%  | 10.82%   | 20.17%  | 30.48%  | 15.67%  | 8.84%   | 5.02%   |
| InternLM2_7B_base_qlora_5epoch  | 41.94%  | 20.21%   | 29.67%  | 42.98%  | 27.07%  | 19.33%   | 14.62%   |
| InternLM2_7B_base_qlora_10epoch | 43.47%  | 22.06%   | 31.4%  | 44.81%  | 29.15%  | 21.44%   | 16.72%   |
