# EmoLLM-心理健康大模型



<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Stargazers][stars-shield]][stars-url]

<!-- PROJECT LOGO -->
<br />

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- PROJECT LOGO -->

<br />

<p align="center">
  <a href="https://github.com/aJupyter/EmoLLM/">
    <img src="assets/logo.jpeg" alt="Logo" width="30%">
  </a>

<h3 align="center">EmoLLM</h3>
  <p align="center">
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

**EmoLLM**是一个能够支持 **理解用户-支持用户-帮助用户** 心理健康辅导链路的心理健康大模型，由[InternLM2](https://github.com/InternLM/InternLM)指令微调而来，欢迎大家star~⭐⭐

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

## 目录

- [EmoLLM-心理健康大模型](#emollm-心理健康大模型)
  - [目录](#目录)
    - [开发前的配置要求](#开发前的配置要求)
    - [**安装步骤**](#安装步骤)
    - [文件目录说明](#文件目录说明)
    - [数据构建](#数据构建)
    - [微调指南](#微调指南)
    - [demo部署](#demo部署)
    - [使用到的框架](#使用到的框架)
    - [贡献者](#贡献者)
      - [如何参与开源项目](#如何参与开源项目)
    - [版本控制](#版本控制)
    - [作者](#作者)
    - [版权说明](#版权说明)
    - [鸣谢](#鸣谢)
  - [Star History](#star-history)
  - [🌟 Contributors](#-contributors)

###### 开发前的配置要求

详见[部署要求](https://github.com/aJupyter/EmoLLM/tree/main/%E9%85%8D%E7%BD%AE%E8%A6%81%E6%B1%82)

###### **安装步骤**

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo

```sh
git clone https://github.com/aJupyter/EmoLLM.git
```

### 文件目录说明

eg:

```
filetree 
├── ARCHITECTURE.md
├── LICENSE.txt
├── README.md
├── /account/
├── /bbs/
├── /docs/
│  ├── /rules/
│  │  ├── backend.txt
│  │  └── frontend.txt
├── manage.py
├── /oa/
├── /static/
├── /templates/
├── useless.md
└── /util/

```


### 数据构建

请阅读[数据构建指南](generate_data/tutorial.md)查阅

本次微调用到的数据集见[datasets](datasets/data.json)

### 微调指南

详见[微调指南](xtuner_config/README.md)

### demo部署

详见[demo](https://github.com/aJupyter/EmoLLM/demo)

<details>
<summary>更多详情</summary>



### 使用到的框架

- [Xtuner](https://github.com/InternLM/xtuner)
- [Trasformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)
- …

### 贡献者

请阅读**CONTRIBUTING.md** 查阅为该项目做出贡献的开发者。

#### 如何参与开源项目

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

[jujimeizup](https://github.com/jujimeizuo)@

[Smiling&amp;Weeping](https://github.com/Smiling-Weeping-zhr)@

[Farewell](https://github.com/8baby8)@

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE](https://github.com/aJupyter/EmoLLM/blob/master/LICENSE)

### 特别鸣谢

- [Sanbu](https://github.com/sanbuphy)
- [上海人工智能实验室](https://www.shlab.org.cn/)
- [闻星大佬（小助手）](https://github.com/vansin)

<!-- links -->

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/in/aJupyter -->

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

