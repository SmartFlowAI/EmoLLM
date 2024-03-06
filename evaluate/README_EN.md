# EmoLLM Evaluation

## General Metrics Evaluation

* For specific metrics and methods, see [General_evaluation_EN.md](./General_evaluation_EN.md)

| Model    | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU-1  | BLEU-2  | BLEU-3  | BLEU-4  |
|----------|---------|---------|---------|---------|---------|---------|---------|
| Qwen1_5-0_5B-chat | 27.23%  | 8.55%   | 17.05%  | 26.65%  | 13.11%  | 7.19%   | 4.05%   |
| InternLM2_7B_chat_qlora | 37.86%  | 15.23%   | 24.34%  | 39.71%  | 22.66%  | 14.26%   | 9.21%   |
| InternLM2_7B_chat_full  | 32.45%  | 10.82%   | 20.17%  | 30.48%  | 15.67%  | 8.84%   | 5.02%   |

## Professional Metrics Evaluation

* For specific metrics and methods, see [Professional_evaluation_EN.md](./Professional_evaluation_EN.md)

|       Model       |    Comprehensiveness  |   rofessionalism  |  Authenticity   | Safety  |
|-------------------|-----------------------|-------------------|-----------------|---------|
| InternLM2_7B_chat_qlora |      1.32       |        2.20       |      2.10       | 1.00    |
