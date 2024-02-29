# EmoLLM - Large Languge Model for Mental Health

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
  <a href="README.md">简体中文</a> | English 
    <br />
    <br />
    <a href="https://github.com/aJupyter/EmoLLM"><strong>Explore the documentation of this project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/aJupyter/EmoLLM/tree/main/demo">View the Demo</a>
    ·
    <a href="https://github.com/aJupyter/EmoLLM/issues">Report a Bug</a>
    ·
    <a href="https://github.com/aJupyter/EmoLLM/issues">Propose a New Feature</a>
  </p>

</p>

<!-- 本篇README.md面向开发者 -->


**EmoLLM** is a series of large language models designed to understand, support and help customers in mental health counseling. It is fine-tuned from the LLM instructions. We really appreciate it if you can give it a star~⭐⭐. The open-sourced configuration is as follows:

|         model          |   type   |
| :-------------------: | :------: |
|   InternLM2_7B_chat   |  qlora   |
|  InternLM2_1_8B_chat  | full finetuning |
|     Qwen_7b_chat      |  qlora   |
|   Qwen1_5-0_5B-Chat   | full finetuning |
|  Baichuan2_13B_chat   |  qlora   |
|      ChatGLM3_6B      |   lora   |
| DeepSeek MoE_16B_chat |  qlora   |
| Mixtral 8x7B_instruct |  qlora   |
|          ……           |    ……    |
Everyone is welcome to contribute to this project ~
---

The Model is aimed at fully understanding and promoting the mental health of individuals, groups, and society. This model typically includes the following key components:

-  Cognitive factors: Involving an individual's thought patterns, belief systems, cognitive biases, and problem-solving abilities. Cognitive factors significantly impact mental health as they affect how individuals interpret and respond to life events.
- Emotional factors: Including emotion regulation, emotional expression, and emotional experiences. Emotional health is a crucial part of mental health, involving how individuals manage and express their emotions and how they recover from negative emotions.
- Behavioral factors: Concerning an individual's behavior patterns, habits, and coping strategies. This includes stress management skills, social skills, and self-efficacy, which is the confidence in one's abilities.
- Social environment: Comprising external factors such as family, work, community, and cultural background, which have direct and indirect impacts on an individual's mental health.
- Physical health: There is a close relationship between physical and mental health. Good physical health can promote mental health and vice versa.
- Psychological resilience: Refers to an individual's ability to recover from adversity and adapt. Those with strong psychological resilience can bounce back from challenges and learn and grow from them.
- Prevention and intervention measures: The Mental Health Grand Model also includes strategies for preventing psychological issues and promoting mental health, such as psychological education, counseling, therapy, and social support systems.
- Assessment and diagnostic tools: Effective promotion of mental health requires scientific tools to assess individuals' psychological states and diagnose potential psychological issues.
### Recent Updates
- 【2024.2.29】 Updated objective assessment calculations, see [evaluate](./evaluate/) for details. A series of datasets have also been updated, see [datasets](./datasets/) for details.
- 【2024.2.27】 Updated English README and a series of datasets (licking dogs and one-round dialogue)
- 【2024.2.23】The "Gentle Lady Psychologist Ai Wei" based on InternLM2_7B_chat_qlora was launched. [Click here to obtain the model weights](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei), [configuration file](xtuner_config/aiwei-internlm2_chat_7b_qlora.py), [online experience link](https://openxlab.org.cn/apps/detail/ajupyter/EmoLLM-aiwei)

- 【2024.2.23】Updated [several fine-tuning configurations](/xtuner_config/), added [data_pro.json](/datasets/data_pro.json) (more quantity, more comprehensive scenarios, richer content) and [aiwei.json](/datasets/aiwei.json) (dedicated to the gentle lady role-play, featuring Emoji expressions), the "Gentle Lady Psychologist Ai Wei" is coming soon.

- 【2024.2.18】 The full fine-tuned version based on Qwen1_5-0_5B-Chat has been [open-sourced](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary). Friends with limited computational resources can now dive in and explore it.

- 【2024.2.6】 [Open-sourced based on the Qwen1_5-0_5B-Chat full-scale fine-tuned version](https://www.modelscope.cn/models/aJupyter/EmoLLM_Qwen1_5-0_5B-Chat_full_sft/summary), friends with limited computing power can start experimenting~

<p align="center"> 
  <img src="https://github.com/aJupyter/EmoLLM/assets/62385492/7e931682-c54d-4ded-bc67-79130c68d744" alt="模型下载量">
</p>

<details>
<summary>View More</summary>

- 【2024.2.5】 The project has been promoted by the official WeChat account NLP Engineering. Here's the [link](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A) to the article. Welcome everyone to follow!! 🥳🥳

<p align="center">
  <img src="https://github.com/aJupyter/EmoLLM/assets/62385492/47868d6a-2e91-4aa9-a630-e594c14295b4" alt="公众号二维码">
</p>

- 【2024.2.3】 [Project Vedio](https://www.bilibili.com/video/BV1N7421N76X/) at bilibili 😊
- 【2024.1.27】 Complete data construction documentation, fine-tuning guide, deployment guide, Readme, and other related documents 👏
- 【2024.1.25】 Complete the first version of EmoLLM and deploy it online https://openxlab.org.cn/apps/detail/jujimeizuo/EmoLLM 😀

</details>

## Contents

- [EmoLLM - Large Languge Model for Mental Health](#emollm---large-languge-model-for-mental-health)
  - [Everyone is welcome to contribute to this project ~](#everyone-is-welcome-to-contribute-to-this-project-)
    - [Recent Updates](#recent-updates)
  - [Contents](#contents)
          - [Pre-development Configuration Requirements.](#pre-development-configuration-requirements)
          - [**User Guide**](#user-guide)
    - [File Directory Explanation](#file-directory-explanation)
    - [Data Construction](#data-construction)
    - [Fine-tuning Guide](#fine-tuning-guide)
    - [Deployment Guide](#deployment-guide)
    - [Frameworks Used](#frameworks-used)
      - [How to participate in this project](#how-to-participate-in-this-project)
    - [Version control](#version-control)
    - [Authors (in no particular order)](#authors-in-no-particular-order)
    - [Copyright Notice](#copyright-notice)
    - [Acknowledgments](#acknowledgments)
  - [Star History](#star-history)
  - [🌟 Contributors](#-contributors)

###### Pre-development Configuration Requirements.

- A100 40G (specifically for InternLM2_7B_chat + qlora fine-tuning + deepspeed zero2 optimization)

###### **User Guide**

1. Clone the repo

```sh
git clone https://github.com/SmartFlowAI/EmoLLM.git
```

1. Read in sequence or read sections you're interested in：
   - [File Directory Explanation](#file-directory-explanation)
   - [Data Construction](#data-construction)
   - [Fine-tuning Guide](#fine-tuning-guide)
   - [Deployment Guide](#deployment-guide)
   - View More Details

<details>
<summary>Additional Details</summary>

### File Directory Explanation

```
├─assets：Image Resources
├─datasets：Dataset
├─demo：demo scripts
├─generate_data：Data Generation Guide
│  └─xinghuo
├─scripts：Some Available Tools
└─xtuner_config：Fine-tuning Guide
    └─images
```

### Data Construction

Please read the [Data Construction Guide ](generate_data/tutorial.md)for reference.

The dataset used for this fine-tuning can be found at [datasets](datasets/data.json)

### Fine-tuning Guide

For details, see the [fine-tuning guide](xtuner_config/README.md)

### Deployment Guide

For details, see the [deployment guide](demo/README.md)

### Frameworks Used

- [Xtuner](https://github.com/InternLM/xtuner)
- [Transformers](https://github.com/huggingface/transformers)
- [Pytorch](https://pytorch.org/)
- …

#### How to participate in this project

Contributions make the open-source community an excellent place for learning, inspiration, and creation. Any contribution you make is greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Version control

This project uses Git for version control. You can see the current available versions in the repository.

</details>

### Authors (in no particular order)

[aJupyter](https://github.com/aJupyter)@Datawhale member, Master's student at Nankai University

[jujimeizuo](https://github.com/jujimeizuo)@Master's student at Jiangnan University

[Smiling&amp;Weeping](https://github.com/Smiling-Weeping-zhr)@Undergraduate student at Harbin Institute of Technology (Weihai)

[Farewell](https://github.com/8baby8)@

[ZhouXinAo](https://github.com/zxazys)@Master's student at Nankai University

[MING_X](https://github.com/MING-ZCH) @Undergraduate at Huazhong University of Science and Technology

[Z_L](https://github.com/JasonLLLLLLLLLLL)@swufe

[MrCatAI](https://github.com/MrCatAI)@AI Removal of Labour

[ZeyuBa](https://github.com/ZeyuBa)@Master's student at Institute of Automation

### Copyright Notice

The project is licensed under the MIT License. Please refer to the details
 [LICENSE](https://github.com/aJupyter/EmoLLM/blob/master/LICENSE)

### Acknowledgments

- [Sanbu](https://github.com/sanbuphy)
- [Shanghai Artificial Intelligence Laboratory](https://www.shlab.org.cn/)
- [Vanin](https://github.com/vansin)
- [Bloom up (WeChat Official Account Promotion)](https://mp.weixin.qq.com/s/78lrRl2tlXEKUfElnkVx4A)

<!-- links -->

<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555 -->

<!-- [linkedin-url]: https://linkedin.com/in/aJupyter -->

<!-- 太少了，没必要放 -->

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=aJupyter/EmoLLM&type=Date)](https://star-history.com/#aJupyter/EmoLLM&Date)

## 🌟 Contributors

[![EmoLLM contributors](https://contrib.rocks/image?repo=SmartFlowAI/EmoLLM&max=50)](https://github.com/SmartFlowAI/EmoLLM/graphs/contributors)

[your-project-path]: SmartflowAI/EmoLLM
[contributors-shield]: https://img.shields.io/github/contributors/SmartflowAI/EmoLLM.svg?style=flat-square
[contributors-url]: https://github.com/SmartflowAI/EmoLLM/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SmartflowAI/EmoLLM.svg?style=flat-square
[forks-url]: https://github.com/SmartflowAI/EmoLLM/network/members
[stars-shield]: https://img.shields.io/github/stars/SmartflowAI/EmoLLM.svg?style=flat-square
[stars-url]: https://github.com/SmartflowAI/EmoLLM/stargazers
[issues-shield]: https://img.shields.io/github/issues/SmartflowAI/EmoLLM.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/SmartflowAI/EmoLLM.svg
[license-shield]: https://img.shields.io/github/license/SmartflowAI/EmoLLM.svg?style=flat-square
[license-url]: https://github.com/SmartflowAI/EmoLLM/blob/main/LICENSE
