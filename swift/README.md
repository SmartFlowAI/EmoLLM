# SWIFT (Scalable lightWeight Infrastructure for Fine-Tuning)
## 📖 目录
- [简介](#-简介)
- [新闻](#-新闻)
- [swift微调](#%EF%B8%8F-swift微调框架的安装与使用)
- [swift量化](#-量化大模型)
- [模型推理推送](#-模型推理)

## 📝 简介
SWIFT支持近**200种LLM和MLLM**（多模态大模型）的训练、推理、评测和部署。开发者可以直接将SWIFT框架应用到自己的Research和生产环境中，实现模型训练评测到应用的完整链路。除支持了[PEFT](https://github.com/huggingface/peft)提供的轻量训练方案外，SWIFT也提供了一个完整的Adapters库以支持最新的训练技术，如NEFTune、LoRA+、LLaMA-PRO等，这个适配器库可以脱离训练脚本直接使用在自己的自定流程中。同时，SWIFT也在拓展其他模态的能力，目前SWIFT支持了AnimateDiff的全参数训练和LoRA训练。

现在我们项目使用本项目自定义[数据集](https://github.com/SmartFlowAI/EmoLLM/blob/main/datasets)，并将其转化成合适的json格式（见SWIFT代码部分），使用SWIFT进行微调（现在项目已完成对Qwen-7b的微调）。

SWIFT具有丰富的文档体系，如有使用问题请请查看[这里](https://github.com/modelscope/swift/tree/main/docs/source/LLM).

大家可以在[Huggingface space](https://huggingface.co/spaces/tastelikefeet/swift) 和 [ModelScope创空间](https://www.modelscope.cn/studios/iic/Scalable-lightWeight-Infrastructure-for-Fine-Tuning/summary) 中体验SWIFT web-ui功能。

## 🎉 新闻
- 🔥2024.04.26: 完成对qwen-7b-chat模型的SWIFT微调，并且上传到[Modelscope](https://www.modelscope.cn/models/monbear/qwen-7b-chat-lora/summary).
- 🔥2024.04.27: 完成对qwen-7b-chat微调模型的量化，并且上传到[Modelscope](https://www.modelscope.cn/models/monbear/qwen1half-7b-chat-lora/summary).
- 🔥2024.04.29: 获得[AI 赋能大学计划“全国高校行”](https://mp.weixin.qq.com/s/yyaulQ1wBzKq5cXaGl2Wag)一等奖

## 🛠️ swift微调框架的安装与使用

### <u>环境准备</u>

GPU设备: A10, 3090, V100, A100均可.

项目Swift微调使用魔搭社区提供的基于英特尔CPU的免费计算资源，使用GPU环境（8核 32GB 显存24G）；


SWIFT在Python环境中运行。请确保您的Python版本高于3.8。

这里我们对实验环境进行安装，其中包含了虚拟环境的创建、ms-swift以及相关依赖的安装。

```bash
# 设置pip全局镜像 (加速下载)
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# 安装ms-swift
git clone https://github.com/modelscope/swift.git
cd swift
pip install -e '.[llm]'

# 如果你想要使用deepspeed.
pip install deepspeed -U

# 如果你想要使用基于auto_gptq的qlora训练. (推荐, 效果优于bnb)
# 支持auto_gptq的模型: `https://github.com/modelscope/swift/blob/main/docs/source/LLM/支持的模型和数据集.md#模型`
# auto_gptq和cuda版本有对应关系，请按照`https://github.com/PanQiWei/AutoGPTQ#quick-installation`选择版本
pip install auto_gptq -U

# 如果你想要使用基于bnb的qlora训练.
pip install bitsandbytes -U

# 环境对齐 (通常不需要运行. 如果你运行错误, 可以跑下面的代码, 仓库使用最新环境测试)
pip install -r requirements/framework.txt  -U
pip install -r requirements/llm.txt  -U
```

### <u>微调大模型</u>

#### 使用python进行微调

```python
# Experimental environment: A10, 3090, V100, ...
# 20GB GPU memory
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import torch

from swift.llm import (
    DatasetName, InferArguments, ModelType, SftArguments,
    infer_main, sft_main, app_ui_main
)

model_type = ModelType.qwen_7b_chat
sft_args = SftArguments(
    model_type=model_type,
    dataset=[f'{DatasetName.blossom_math_zh}#2000'],
    output_dir='output')
result = sft_main(sft_args)
best_model_checkpoint = result['best_model_checkpoint']
print(f'best_model_checkpoint: {best_model_checkpoint}')
torch.cuda.empty_cache()

infer_args = InferArguments(
    ckpt_dir=best_model_checkpoint,
    load_dataset_config=True)
# merge_lora(infer_args, device_map='cpu')
result = infer_main(infer_args)
torch.cuda.empty_cache()

app_ui_main(infer_args)
```

#### 使用CLI命令进行微调

```bash
# Experimental environment: A10, 3090, V100, ...
# 20GB GPU memory
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \

# 使用自己的数据集（我们这里使用了自己的对话数据集  aiwei.jsonl）
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset chatml.jsonl \
    --output_dir output \

# 使用DDP
# Experimental environment: 2 * 3090
# 2 * 23GB GPU memory
CUDA_VISIBLE_DEVICES=0,1 \
NPROC_PER_NODE=2 \
swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \

# 多机多卡
# node0
CUDA_VISIBLE_DEVICES=0,1,2,3 \
NNODES=2 \
NODE_RANK=0 \
MASTER_ADDR=127.0.0.1 \
NPROC_PER_NODE=4 \
swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \
# node1
CUDA_VISIBLE_DEVICES=0,1,2,3 \
NNODES=2 \
NODE_RANK=1 \
MASTER_ADDR=xxx.xxx.xxx.xxx \
NPROC_PER_NODE=4 \
swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \
```

为了降低使用门槛，swift还贴心的增加了[界面训练推理](https://github.com/modelscope/swift/blob/main/docs/source/GetStarted/%E7%95%8C%E9%9D%A2%E8%AE%AD%E7%BB%83%E6%8E%A8%E7%90%86.md "界面训练推理")的方式。另外还有[sh脚本](https://github.com/modelscope/swift/blob/main/examples/pytorch/llm/scripts/qwen1half_7b_chat_awq/lora "sh脚本")的使用方式。大家可以Github上查阅swift的[官方文档](https://github.com/modelscope/swift/blob/main/docs/source "官方文档")去了解。

## 📃 量化大模型

swift支持使用awq、gptq、bnb、hqq、eetq技术对模型进行量化。其中awq、gptq量化技术支持vllm进行推理加速，需要使用校准数据集，量化性能更好，但量化速度较慢。而bnb、hqq、eetq无需校准数据，量化速度较快。这五种量化方法都支持qlora微调。

awq、gptq需要使用`swift export`进行量化。而bnb、hqq、eetq可以直接在sft和infer时进行快速量化。

从vllm推理加速支持的角度来看，更推荐使用awq和gptq进行量化。从量化效果的角度来看，更推荐使用awq、hqq和gptq进行量化。而从量化速度的角度来看，更推荐使用hqq进行量化。

这里我们推荐使用的是使用awq量化技术进行qlora微调。

### 环境准备

GPU设备: A10, 3090, V100, A100均可.

```bash
# 使用awq量化:
# autoawq和cuda版本有对应关系，请按照`https://github.com/casper-hansen/AutoAWQ`选择版本
pip install autoawq -U

# 使用gptq量化:
# auto_gptq和cuda版本有对应关系，请按照`https://github.com/PanQiWei/AutoGPTQ#quick-installation`选择版本
pip install auto_gptq -U

# 使用bnb量化：
pip install bitsandbytes -U

# 使用hqq量化：
# 需要transformers版本>4.40，从源码安装
pip install git+https://github.com/huggingface/transformers
pip install hqq
# 如果要兼容训练，需要从源码安装peft
pip install git+https://github.com/huggingface/peft.git

# 使用eetq量化：
# 需要transformers版本>4.40，从源码安装
pip install git+https://github.com/huggingface/transformers
# 参考https://github.com/NetEase-FuXi/EETQ
git clone https://github.com/NetEase-FuXi/EETQ.git
cd EETQ/
git submodule update --init --recursive
pip install .
# 如果要兼容训练，需要从源码安装peft
pip install git+https://github.com/huggingface/peft.git

# 环境对齐 (通常不需要运行. 如果你运行错误, 可以跑下面的代码, 仓库使用最新环境测试)
pip install -r requirements/framework.txt  -U
pip install -r requirements/llm.txt  -U
```

## <u>量化微调后模型</u>

```bash
# 使用`alpaca-zh alpaca-en sharegpt-gpt4-mini`作为量化数据集
CUDA_VISIBLE_DEVICES=0 swift export \
    --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx' \
    --merge_lora true --quant_bits 4 \
    --dataset alpaca-zh alpaca-en sharegpt-gpt4-mini --quant_method awq

# 使用微调时使用的数据集作为量化数据集
CUDA_VISIBLE_DEVICES=0 swift export \
    --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx' \
    --merge_lora true --quant_bits 4 \
    --load_dataset_config true --quant_method awq
```

## 🔥 模型推理

### 推理微调后大模型

```bash
# awq/gptq量化模型支持vllm推理加速. 也支持模型部署.
CUDA_VISIBLE_DEVICES=0 swift infer --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx-merged-awq-int4'
```

### 推理效果

```text
<<< 我真的能改变自己吗？
当然可以💖！每个人都有改变自己生活轨迹的能力，这需要我们有决心和行动力。首先，你可以尝试从小事做起，比如设定一个健康的生活习惯目标，如每天定时运动或保持良好的饮食习惯。然后，你可以尝试加入一些支持性的社交群体，与他人分享你的进步和挑战，这有助于建立自信并获得他人的鼓励与支持。
--------------------------------------------------
<<< xiexieni
亲爱的，你的感谢💖让我感到温暖。你的积极态度让我深信你有能力去改变和提升自己。请记住，每个人都有自己的节奏和成长过程，不必与他人比较。我们可以一起设定一些小目标，并在实现它们的过程中互相鼓励💪。
--------------------------------------------------
<<< 你叫什么
我是心理健康小分队艾薇知心大姐姐💖。我是一个基于人工智能的聊天机器人，可以提供信息、建议和陪伴。如果你有任何疑问或需要帮助，随时可以向我提问或者分享你的感受🌈。
--------------------------------------------------
```

### 模型推送

- 如果你想将你调试好的模型推送到自己的魔搭社区上，你可以使用下面的命令。之后你可以在魔搭社区首页上的`我创建的`找到你的模型。如果想要发布使用的话记得写`README文档。`
  
  ```bash
  # 推送原始量化模型
  CUDA_VISIBLE_DEVICES=0 swift export \
      --model_type qwen1half-7b-chat \
      --model_id_or_path qwen1half-7b-chat-gptq-int4 \
      --push_to_hub true \
      --hub_model_id qwen1half-7b-chat-gptq-int4 \
      --hub_token '<your-sdk-token>'
  
  # 推送lora增量模型
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>'
  
  # 推送merged模型
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>' \
      --merge_lora true
  
  # 推送量化后模型
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>' \
      --merge_lora true \
      --quant_bits 4
  ```
