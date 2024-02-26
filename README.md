# EmoLLM-心理健康大模型

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]
<br />
<!-- PROJECT LOGO -->

<p align="center">
  <a href="https://github.com/aJupyter/EmoLLM/">
    <img src="assets/logo.jpeg" alt="Logo" width="30%">
  </a>

<h3 align="center">EmoLLM</h3>

  <p align="center">
      简体中文| <a href="README_English_version.md" >English</a> 
    <br />
    <a href="https://github.com/aJupyter/EmoLLM"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/aJupyter/EmoLLM/tree/main/demo">查看Demo</a>
    ·
    <a href="https://github.com/aJupyter/EmoLLM/issues">报告Bug</a>
    ·
    <a href="https://github.com/aJupyter/EmoLLM/issues">提出新特性</a>
  </p>

</p>

<!-- 本篇README.md面向开发者 -->

**EmoLLM** 是一个能够支持 **理解用户-支持用户-帮助用户** 心理健康辅导链路的心理健康大模型，由 `LLM`指令微调而来，欢迎大家star~⭐⭐。目前已经开源的 `LLM`微调配置如下：

|         模型          |   类型   |
| :-------------------: | :------: |
|   InternLM2_7B_chat   |  qlora   |
|  InternLM2_1_8B_chat  | 全量微调 |
|     Qwen_7b_chat      |  qlora   |
|   Qwen1_5-0_5B-Chat   | 全量微调 |
|  Baichuan2_13B_chat   |  qlora   |
|      ChatGLM3_6B      |   lora   |
| DeepSeek MoE_16B_chat |  qlora   |
| Mixtral 8x7B_instruct |  qlora   |
|          ……           |    ……    |
欢迎大家为本项目做出贡献~

---

心理健康大模型（Mental Health Grand Model）是一个综合性的概念，它旨在全面理解和促进个体、群体乃至整个社会的心理健康状态。这个模型通常包含以下几个关键组成部分：

- 认知因素：涉及个体的思维模式、信念系统、认知偏差以及解决问题的能力。认知因素对心理健康有重要影响，因为它们影响个体如何解释和应对生活中的事件。
- 情感因素：包括情绪调节、情感表达和情感体验。情感健康是心理健康的重要组成部分，涉及个体如何管理和表达自己的情感，以及如何从负面情绪中恢复。
- 行为因素：涉及个体的行为模式、习惯和应对策略。这包括应对压力的技巧、社交技能以及自我效能感，即个体对自己能力的信心。
- 社会环境：包括家庭、工作、社区和文化背景等外部因素，这些因素对个体的心理健康有着直接和间接的影响。
- 生理健康：身体健康与心理健康紧密相关。良好的身体健康可以促进心理健康，反之亦然。
- 心理韧性：指个体在面对逆境时的恢复力和适应能力。心理韧性强的人更能够从挑战中恢复，并从中学习和成长。
- 预防和干预措施：心理健康大模型还包括预防心理问题和促进心理健康的策略，如心理教育、心理咨询、心理治疗和社会支持系统。
- 评估和诊断工具：为了有效促进心理健康，需要有科学的工具来评估个体的心理状态，以及诊断可能存在的心理问题。

### 最近更新
- 【2024.2.23】推出基于InternLM2_7B_chat_qlora的 `温柔御姐心理医生艾薇`，[点击获取模型权重](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei)，[配置文件](xtuner_config/aiwei-internlm2_chat_7b_qlora.py)，[在线体验链接](https://openxlab.org.cn/apps/detail/ajupyter/EmoLLM_aiwei)
- 【2024.2.23】更新[若干微调配置](/xtuner_config/)，新增 [data_pro.json](/datasets/data_pro.json)（数量更多、场景更全、更丰富）和 [aiwei.json](/datasets/aiwei.json)（温柔御姐角色扮演专用，带有Emoji表情），即将推出 `温柔御姐心理医生艾薇`
- 【2024.2.18】 [基于Qwen1_5-0_5B-Chat全量微调版本开源](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary)，算力有限的道友可以玩起来~
- 【2024.2.6】 EmoLLM在[**Openxlab** ](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model) 平台下载量高达18.7k，欢迎大家体验！

<p align="center"> 
  <img src="https://github.com/aJupyter/EmoLLM/assets/62385492/7e931682-c54d-4ded-bc67-79130c68d744" alt="模型下载量">
</p>

<details>
<summary>查看更多</summary>

- 【2024.2.5】 项目荣获公众号**NLP工程化**推文宣传[推文链接](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)，为博主推广一波，欢迎大家关注！！🥳🥳

<p align="center">
  <img src="https://github.com/aJupyter/EmoLLM/assets/62385492/47868d6a-2e91-4aa9-a630-e594c14295b4" alt="公众号二维码">
</p>

- 【2024.2.3】 [项目宣传视频](https://www.bilibili.com/video/BV1N7421N76X/)完成 😊
- 【2024.1.27】 完善数据构建文档、微调指南、部署指南、Readme等相关文档 👏
- 【2024.1.25】 完成EmoLLM第一版并部署上线 https://openxlab.org.cn/apps/detail/jujimeizuo/EmoLLM 😀

</details>

## 目录

- [EmoLLM-心理健康大模型](#emollm-心理健康大模型)
  - [最近更新](#最近更新)
  - [目录](#目录)
    - [开发前的配置要求](#开发前的配置要求)
    - [**使用指南**](#使用指南)
    - [文件目录说明](#文件目录说明)
    - [数据构建](#数据构建)
    - [微调指南](#微调指南)
    - [部署指南](#部署指南)
    - [使用到的框架](#使用到的框架)
      - [如何参与本项目](#如何参与本项目)
    - [版本控制](#版本控制)
    - [作者（排名不分先后）](#作者排名不分先后)
    - [版权说明](#版权说明)
    - [特别鸣谢](#特别鸣谢)
  - [Star History](#star-history)
  - [🌟 Contributors](#-contributors)

###### 开发前的配置要求

- 硬件：A100 40G（仅针对InternLM2_7B_chat+qlora微调+deepspeed zero2优化）

###### **使用指南**

1. Clone the repo

```sh
git clone https://github.com/aJupyter/EmoLLM.git
```

2. 依次阅读或者选择感兴趣的部分阅读：
   - [文件目录说明](#文件目录说明)
   - [数据构建](#数据构建)
   - [微调指南](#微调指南)
   - [部署指南](#部署指南)
   - 查看更多详情

<details>
<summary>更多详情</summary>

### 文件目录说明

```
├─assets：图像资源
├─datasets：数据集
├─demo：demo脚本
├─generate_data：生成数据指南
│  └─xinghuo
├─scripts：一些可用工具
└─xtuner_config：微调指南
    └─images
```

### 数据构建

请阅读[数据构建指南](generate_data/tutorial.md)查阅

本次微调用到的数据集见[datasets](datasets/data.json)

### 微调指南

详见[微调指南](xtuner_config/README.md)

### 部署指南

详见[部署指南](demo/README.md)

### 使用到的框架

- [Xtuner](https://github.com/InternLM/xtuner)
- [Transformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)
- …

#### 如何参与本项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

</details>

### 作者（排名不分先后）

[aJupyter](https://github.com/aJupyter)@datawhale成员、南开大学在读硕士

[jujimeizuo](https://github.com/jujimeizuo)@江南大学硕士

[Smiling&amp;Weeping](https://github.com/Smiling-Weeping-zhr)@哈尔滨工业大学（威海）在读本科生

[Farewell](https://github.com/8baby8)@

[ZhouXinAo](https://github.com/zxazys)@南开大学在读硕士

[MING_X](https://github.com/MING-ZCH)@华中科技大学在读本科生

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/aJupyter/EmoLLM/blob/master/LICENSE)

### 特别鸣谢

- [Sanbu](https://github.com/sanbuphy)
- [上海人工智能实验室](https://www.shlab.org.cn/)
- [闻星大佬（小助手）](https://github.com/vansin)
- [扫地升（公众号宣传）](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)

<!-- links -->

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/in/aJupyter -->

<!-- 太少了，没必要放 -->

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=aJupyter/EmoLLM&type=Date)](https://star-history.com/#aJupyter/EmoLLM&Date)

## 🌟 Contributors

[![EmoLLM contributors](https://contrib.rocks/image?repo=aJupyter/EmoLLM&max=50)](https://github.com/aJupyter/EmoLLM/graphs/contributors)

[your-project-path]: aJupyter/EmoLLM
[contributors-shield]: https://img.shields.io/github/contributors/aJupyter/EmoLLM.svg?style=flat-square
[contributors-url]: https://github.com/aJupyter/EmoLLM/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/aJupyter/EmoLLM.svg?style=flat-square
[forks-url]: https://github.com/aJupyter/EmoLLM/network/members
[stars-shield]: https://img.shields.io/github/stars/aJupyter/EmoLLM.svg?style=flat-square
[stars-url]: https://github.com/aJupyter/EmoLLM/stargazers
[issues-shield]: https://img.shields.io/github/issues/aJupyter/EmoLLM.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/aJupyter/EmoLLM.svg
[license-shield]: https://img.shields.io/github/license/aJupyter/EmoLLM.svg?style=flat-square
[license-url]: https://github.com/aJupyter/EmoLLM/blob/main/LICENSE
