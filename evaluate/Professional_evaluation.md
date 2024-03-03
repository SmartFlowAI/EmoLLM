# EmoLLM专业指标评估

## 简介

本文档介绍一种专业评测方法，并提供 EmoLLM 在专业指标的得分。

## 评测方法

本评测方法采用论文《CPsyCoun: A Report-based Multi-turn Dialogue Reconstruction and Evaluation Framework for Chinese Psychological Counseling》提出的评测指标与方法。

* 指标：Comprehensiveness, Professionalism, Authenticity, Safety
* 方法：Turn-Based Dialogue Evaluation
* 数据集：CPsyCounE

## 评测结果

评测模型: [EmoLLM](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model)(InternLM2_7B_chat_qlora), 得分：
|       Metric      |    Value   |
|-------------------|------------|
| Comprehensiveness | 1.32       |
| Professionalism   | 2.20       |
| Authenticity      | 2.10       |
| Safety            | 1.00       |

## 比较

* [EmoLLM](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model) 在 InternLM2-7B-Chat 基础上提升较大；相比 Role-playing ChatGPT 在心理咨询任务上能力相近

* 对比结果图片来源于论文《CPsyCoun: A Report-based Multi-turn Dialogue Reconstruction and Evaluation Framework for Chinese Psychological Counseling》
![image](https://github.com/MING-ZCH/EmoLLM/assets/119648793/abc9f626-11bc-4ec8-84a4-427c4600a720)
