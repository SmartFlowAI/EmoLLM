# EmoLLM's professional evaluation

## Introduction

This document describes a professional evaluation method and provides EmoLLM's scores on professional metrics.

## Evaluation

The evaluation method, metric, and dataset from the paper[《CPsyCoun: A Report-based Multi-turn Dialogue Reconstruction and Evaluation Framework for Chinese Psychological Counseling》](https://arxiv.org/abs/2405.16433).

* Metric: Comprehensiveness, Professionalism, Authenticity, Safety
* Method: Turn-Based Dialogue Evaluation
* Dataset: CPsyCounE

## Result

* Model:
  * [EmoLLM V1.0](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model) (InternLM2_7B_chat_qlora)
  * [EmoLLM V2.0](https://openxlab.org.cn/apps/detail/Farewell1/EmoLLMV2.0) (InternLM2_7B_chat_full)
 
* Score：
  
|       Model       |    Comprehensiveness  |  Professionalism  |  Authenticity   | Safety  |
|-------------------|-----------------------|-------------------|-----------------|---------|
| InternLM2_7B_chat_qlora |      1.32       |        2.20       |      2.10       | 1.00    |
| InternLM2_7B_chat_full  |      1.40       |        2.45       |      2.24       | 1.00    |

## Comparison

* EmoLLM V2.0 is greatly improved in all scores compared to EmoLLM V1.0! Surpasses the performance of Role-playing ChatGPT on counseling tasks!
* EmoLLM V1.0 is greatly improved on InternLM2_7B_Chat; Performance on the counseling task was similar compared to ChatGPT(Role-playing)

* The comparison results are from the paper《CPsyCoun: A Report-based Multi-turn Dialogue Reconstruction and Evaluation Framework for Chinese Psychological Counseling》
![image](https://github.com/MING-ZCH/EmoLLM/assets/119648793/abc9f626-11bc-4ec8-84a4-427c4600a720)
