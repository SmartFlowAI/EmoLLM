# InternLM2 7B Base QLoRA 微调指南

## 模型基座与配置文件

- 本项目在XTuner项目所提供的[**internlm2_7b_chat_qlora_e3**模型配置文件](./internlm2_7b_chat_qlora_e3.py)和在[EmoLLM模型微调指南](./README.md)的基础上，创建和更新了对**InternLM2_7B_base模型**在[EmoLLM通用数据集](../datasets/README.md)上进行QLoRA微调训练，配置文件详见[**internlm2_7b_base_qlora_e10_M_1e4_32_64.py**](./internlm2_7b_base_qlora_e10_M_1e4_32_64.py)。
- 为了用户可以根据自己不同的硬件配置进行复现和微调训练，EmoLLM也提供了其他的配置文件以满足不同的配置需求。
  - [internlm2_7b_base_qlora_e10_b8_16_32.py](./internlm2_7b_base_qlora_e10_b8_16_32.py)
  - [internlm2_7b_base_qlora_e3_M_1e4_32_64.py](./internlm2_7b_base_qlora_e3_M_1e4_32_64.py)

## 模型公布和训练epoch数设置

- 由于采用了合并后的数据集，我们对选用的InternLM2_7B_base模型进行了**10 epoch**的训练，读者可以根据训练过程中的输出和loss变化，进行训练的终止和模型的挑选，也可以采用更加专业的评估方法，来对模型评测。

- 在我们公布的InternLM2_7B_base QLoRA微调模型时，也分别在OpenXLab和ModelScope中提供了两个不同的权重版本供用户使用和测试，更多专业测评结果将会在近期更新，敬请期待。

  - **OpenXLab**：
    - [5 epoch 模型](https://openxlab.org.cn/models/detail/chg0901/EmoLLM-InternLM7B-base)
    - [10 epoch 模型](https://openxlab.org.cn/models/detail/chg0901/EmoLLM-InternLM7B-base-10e)
  - **ModelScope**：
    - [5 epoch 模型](https://www.modelscope.cn/models/chg0901/EmoLLM-InternLM7B-base/files)
    - [10 epoch 模型](https://www.modelscope.cn/models/chg0901/EmoLLM-InternLM7B-base-10e/files)

- 目前EmoLLM团队已经采用**通用指标**评估了QLoRA微调训练的InternLM2_7B_base模型（包括5 epoch 模型和10 epoch 模型），结果如下表所示，可以看到10 epoch QLoRA微调训练的InternLM2_7B_base模型通用指标已经超过其他模型，我们将近期更新在心理咨询专业指标上的评测结果。更多评测详情请查看[通用测评结果页面（General_evaluation.md）](../evaluate/General_evaluation.md)和[测评目录README](../evaluate/README.md).

| Model    | ROUGE-1 | ROUGE-2 | ROUGE-L | BLEU-1  | BLEU-2  | BLEU-3  | BLEU-4  |
|----------|---------|---------|---------|---------|---------|---------|---------|
| Qwen1_5-0_5B-chat | 27.23%  | 8.55%   | 17.05%  | 26.65%  | 13.11%  | 7.19%   | 4.05%   |
| InternLM2_7B_chat_qlora | 37.86%  | 15.23%   | 24.34%  | 39.71%  | 22.66%  | 14.26%   | 9.21%   |
| InternLM2_7B_chat_full  | 32.45%  | 10.82%   | 20.17%  | 30.48%  | 15.67%  | 8.84%   | 5.02%   |
| InternLM2_7B_base_qlora_5epoch  | 41.94%  | 20.21%   | 29.67%  | 42.98%  | 27.07%  | 19.33%   | 14.62%   |
| **InternLM2_7B_base_qlora_10epoch** | **43.47%** | **22.06%**   | **31.4%**  | **44.81%**  | **29.15%**  | **21.44%**   | **16.72%**   |

### 超参数设置

训练config设置详情，请查看[**`internlm2_7b_base_qlora_e10_M_1e4_32_64.py`（配置文件）**](./internlm2_7b_base_qlora_e10_M_1e4_32_64.py)，这里我们只列出了关键的超参数或者我们做过调整的超参数。

```python
prompt_template = PROMPT_TEMPLATE.internlm2_chat
max_length = 2048
pack_to_max_length = True

batch_size = 16 # per_device
accumulative_counts = 1

max_epochs = 10
lr = 1e-4
evaluation_freq = 500

SYSTEM = "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。"
evaluation_inputs = [
    '我最近总是感到很焦虑，尤其是在学业上。我有个特别崇拜的同学，他好像在各方面都比我优秀，我总觉得自己怎么努力也追不上他，这让我压力特别大。', 
    '我知道应该理性看待，但就是忍不住会去比较。我甚至晚上会因为这个睡不着觉，总想着怎样才能像他那样出色。',
    '我今天心情不好，感觉不开心，很烦。']

model = dict(
    lora=dict(
        type=LoraConfig,
        r=32,
        lora_alpha=64,  # lora_alpha=2*r
        lora_dropout=0.1,
        bias='none',
        task_type='CAUSAL_LM'
        )
        )
```

## 数据

### 数据集

只采用了通用的数据集，不包括带有Role-Play色彩的数据集，详情请查看[数据集](../datasets/README.md)页面

|   Category  |        Dataset        |     Type     |  Total  |
| :---------: | :-------------------: | :----------: | :-----: |
|  General  |         data          | Conversation |  5600+  |
|  General  |       data_pro        | Conversation | 36500+  |
|  General  | multi_turn_dataset_1  | Conversation | 36,000+ |
|  General  | multi_turn_dataset_2  | Conversation | 27,000+ |
|  General  | single_turn_dataset_1 |      QA      | 14000+  |
|  General  | single_turn_dataset_2 |      QA      | 18300+  |

注意：此处的数据量计数是将多轮对话拆成单轮问答后的数据量，请注意联系区别，合并后总数据量为**51468**个对话（多轮对话算一个）。

### 数据集处理

#### 数据格式

训练用的数据，被处理成单轮或者多轮对话的形式，如

```python
[
    # 多轮对话
    {
        "conversation": [
            {
                "input": "我最近很迷茫，高三后的压力让我感到恐惧，我对自己的存在感到怀疑，您能不能给我一些建议呢？",
                "output": "看到你面临的困境与压力，真心希望能够帮助你。首先，我想说的是，你并不是孤独的，高考前的困惑与迷茫是很常见的。不要给自己太大的压力，给自己短暂的放松。你认识到问题所在，这已经是一个很大的进步了。",
                "system": "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。"
            },
            {
                "input": "谢谢您的鼓励，但我觉得自己学习成绩不好，没有进步，这让我更加困惑。",
                "output": "学习成绩好坏不是解决问题的关键，专注于自己的进步更为重要。为了达到自己的目标，制定一份合理的计划，按部就班的完成每一项任务。有时候自学不如求助他人，不要害怕问老师和同学问题，以便获得更好的帮助和理解。"
            },
            {
                "input": "我认为我缺乏自信，不知道怎样扭转自己的消极情绪，您能给我一些建议吗？",
                "output": "建立自信需要时间和努力。让我们从一点一滴的进步中建立自信心。设立一些具体的目标，完成这些目标将会培养自己的自信。鼓励自己，在每天结束前，总结一下自己的成就，这将帮助你更好的看到自身的优点。"
            },
            {
                "input": "我感到很无助，不知道该如何调整自己的心态。",
                "output": "了解自己的情绪并寻找有效的调节方法是处理感到无助情况的关键。比如爱好运动、听音乐和阅读书籍等，这些活动对于您的心理健康都是有积极帮助的。此外，在处理感到无助的情况下，家庭和朋友的支持也是非常关键的。"
            },
            {
                "input": "我感觉我的思维和学习方法都很糟糕，该怎样改进呢？",
                "output": "学习方法确实很重要，它会对你的成绩和情绪有很大的影响。最有效的学习方法是利用时间来做练习，多做一些题目，练习自己的掌握能力。建立起对知识的兴趣，这需要不断的积累，不要害怕失败或挫折，它们会成为助你成长的宝贵财富。"
            },
            {
                "input": "我会按照您的建议努力，但想问一下，我该如何面对可能的失败？",
                "output": "每个人都会面对失败和挫折，不要让它们打败你。碰到失败时，重新审视自己，分析分析自己的不足，寻找方法去改进。记得勇敢地看向未来，不要让过去的失败阻碍了自己前进的脚步。"
            },
            {
                "input": "非常感谢您的建议和支持，我会努力去实践。",
                "output": "这是我应该做的，你有勇气面对自己困难，你并不孤独，我们会一起为你打气，祝愿你早日获得心灵的平静和所有的成功。"
            }
        ]
    },
    # 单轮对话
    {
        "conversation": [
            {
                "system": "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。",
                "input": "一想到事情就紧张……?\n我最近因为考试，觉得心情很不好，自己没有及格，而且，明明觉得自己比室友付出的多，努力的多，平时做题也是一样的，可是不知道为什么只有我不及格，感觉很苦恼。而且我只要一有什么事情就十分紧张，考试也是，心跳加速，手心出汗，而且大脑一片空白，有时甚至会头疼，高考以及现在的考试都是这样。而且我觉得一情绪激动的时候就会咳嗽，想哭哭不出来，感觉很难受，头也会疼。就是觉得心情不好，但是有不敢表现出来。我该怎么办呢？",
                "output": "为什么不敢表现出来呢？试试表现出来，会怎样？\n有时候我们越抗拒，就会越强化。当我们接受了，反而症状就消失了。\n那我们要怎样接受呢？\n这本书《心灵的七种兵器》推荐看看哦，内容精简，又有真实事例可以帮助理解。\n我们为什么改不掉这个所谓的坏习惯。\n"
            }
        ]
    },
```

### 数据处理

- 使用 `../datasets/process.py` 以处理 **multi_turn_dataset(1 和 2，QA数据转单轮对话)**， `data.json` 和 `data_pro.json` 文件（两个多轮对话），以添加或者调整 **`system` prompt**
- 使用 `../datasets/processed/process_single_turn_conversation_construction.py` 处理 **single-turn dataset** (1 和 2)，修改 (`input` 和 `ouput`) ，并在每次 **conversation** 中添加 **`system` prompt**
- 使用 `../datasets/processed/process_merge.py` 用于合并 `../datasets/processed/` 目录下**6个更新后的数据集**，生成一个合并后的数据集 `combined_data.json`用于最终训练

## 基于XTuner的微调🎉🎉🎉🎉🎉

### 环境准备

```bash
datasets==2.16.1
deepspeed==0.13.1
einops==0.7.0
flash_attn==2.5.0
openxlab==0.0.34
peft==0.7.1
sentencepiece==0.1.99
torch==2.1.2
transformers==4.36.2

# 需要注意的几个库（版本调整或者安装较麻烦）
mmengine==0.10.3
xtuner==0.1.15
flash_attn==2.5.0
mpi4py==3.1.5 # conda install mpi4py 
```

也可以一键安装

```bash
cd xtuner_config/
pip install -r requirements.txt
```

温馨提示：`flash_attn`的安装可能需要在本地编译，大约需要一到两小时，可以去[flash-attention](https://github.com/Dao-AILab/flash-attention/releases)中，查找和自己机器配置匹配的whl安装包或者采用InternLM AI studio提供的`2.4.2`版本whl安装包，自行安装，如：

```bash
# from flash-attention
pip install flash_attn-2.5.0+cu122torch2.1cxx11abiTRUE-cp310-cp310-linux_x86_64.whl  

# from InternLM AI studio share folder
pip install /root/share/wheels/flash_attn-2.4.2+cu118torch2.0cxx11abiTRUE-cp310-cp310-linux_x86_64.whl  
```

---

### 微调

```bash
cd xtuner_config/
xtuner train internlm2_7b_base_qlora_e10_M_1e4_32_64.py --deepspeed deepspeed_zero2
```

---

### 将得到的 PTH 模型转换为 HuggingFace 模型

即：生成 HuggingFace Adapter 文件夹, 用于和原模型权重合并

```bash
cd xtuner_config/
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1

xtuner convert pth_to_hf internlm2_7b_base_qlora_e10_M_1e4_32_64.py ./work_dirs/internlm2_7b_base_qlora_e10_M_1e4_32_64/epoch_5.pth ./hf
```

---

### 将 HuggingFace Adapter QLoRA权重合并到大语言模型

```bash
xtuner convert merge /root/share/model_repos/internlm2-base-7b ./hf ./merged --max-shard-size 2GB
# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
#     --max-shard-size 2GB
```

### 10 epoch 模型的处理

```bash

cd xtuner_config/
mkdir hf10
export MKL_SERVICE_FORCE_INTEL=1

xtuner convert pth_to_hf internlm2_7b_base_qlora_e10_M_1e4_32_64.py ./work_dirs/internlm2_7b_base_qlora_e10_M_1e4_32_64/epoch_10.pth ./hf

xtuner convert merge /root/share/model_repos/internlm2-base-7b ./hf10 ./merged10 --max-shard-size 2GB
# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
#     --max-shard-size 2GB
```

---

### 测试

```bash
cd demo/
python cli_internlm2.py
```

---

## 其他

欢迎大家给[xtuner](https://github.com/InternLM/xtuner)和[EmoLLM](https://github.com/aJupyter/EmoLLM)点点star~

🎉🎉🎉🎉🎉
