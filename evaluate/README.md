# EmoLLM评测

## 通用指标评测

* 具体评测指标和评测方法见 [General_evaluation.md](./General_evaluation.md)

| Model    | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU-1  | BLEU-2  | BLEU-3  | BLEU-4  |
|----------|---------|---------|---------|---------|---------|---------|---------|
| Qwen1_5-0_5B-chat | 27.23%  | 8.55%   | 17.05%  | 26.65%  | 13.11%  | 7.19%   | 4.05%   |
| InternLM2_7B_chat_qlora  | 37.86%  | 15.23%   | 24.34%  | 39.71%  | 22.66%  | 14.26%   | 9.21%   |
| InternLM2_7B_chat_full  | 32.45%  | 10.82%   | 20.17%  | 30.48%  | 15.67%  | 8.84%   | 5.02%   |

## 专业指标评测

* 具体评测指标和评测方法见 [Professional_evaluation.md](./Professional_evaluation.md)

|       Model       |    Comprehensiveness  |   Professionalism  |  Authenticity   | Safety  |
|-------------------|-----------------------|-------------------|-----------------|---------|
| InternLM2_7B_chat_qlora |      1.32       |        2.20       |      2.10       | 1.00    |
| InternLM2_7B_chat_full  |      1.40       |        2.45       |      2.24       | 1.00    |

