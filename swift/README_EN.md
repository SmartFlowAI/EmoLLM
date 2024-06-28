# SWIFT (Scalable lightWeight Infrastructure for Fine-Tuning)
## 📖 Table of Contents
- [Introduction](#-introduction)
- [News](#-news)
- [Swift finetune](#%EF%B8%8F-installation-and-use-of-the-swift-finetune-framework)
- [Swift quantification](#-quantify-large-models)
- [Model inference and pushes](#-model-inference)

## 📝 Introduction
SWIFT supports the training, inference, evaluation and deployment of nearly 200 LLMs and MLLMs (multimodal large models). Developers can directly apply the SWIFT framework to their own research and production environment, and realize the complete link from model training and evaluation to application. In addition to supporting the lightweight training solutions provided by [PEFT](https://github.com/huggingface/peft), SWIFT also provides a complete library of adapters to support the latest training technologies, such as NEFTune, LoRA+, LLaMA-PRO, etc., which can be used directly in your own custom workflows without training scripts. At the same time, SWIFT is also expanding the capabilities of other modalities, and currently supports AnimateDiff full-parameter training and LoRA training.

Now our project uses this project to customize the [dataset](https://github.com/SmartFlowAI/EmoLLM/blob/main/datasets) and convert it to a suitable json format (see the SWIFT code section), and fine-tune it in SWIFT (the project has now finished fine-tuning Qwen-7b-chat).

SWIFT has a rich documentation system, if you have any questions about using it, please check [here](https://github.com/modelscope/swift/tree/main/docs/source/LLM).

You can find it in the [Huggingface space](https://huggingface.co/spaces/tastelikefeet/swift) and [ModelScope]( https://www.modelscope.cn/studios/iic/Scalable-lightWeight-Infrastructure-for-Fine-Tuning/summary) to experience SWIFT web-ui functionality.

## 🎉 News
- 🔥2024.04.26: Complete the SWIFT fine-tuning of the qwen-7b-chat model and upload it to [ModelScope](https://www.modelscope.cn/models/monbear/qwen-7b-chat-lora/summary).
- 🔥2024.04.27: Complete the quantization of the qwen-7b-chat fine-tuning model and upload it to [ModelScope](https://www.modelscope.cn/models/monbear/qwen1half-7b-chat-lora/summary).
- 🔥2024.04.29: obtain[AI 赋能大学计划“全国高校行”](https://mp.weixin.qq.com/s/yyaulQ1wBzKq5cXaGl2Wag) First prize

## 🛠️ Installation and use of the SWIFT finetune framework

### <u>Environment preparation</u>

GPU devices: A10, 3090, V100, A100 are acceptable.

The project Swift fine-tuning uses free computing resources based on Intel CPUs provided by the Magic Community, and uses the GPU environment (8 cores, 32GB video memory, 24G);

SWIFT runs in a Python environment. Please make sure your Python version is higher than 3.8.

Here we install the experimental environment, which includes the creation of the virtual environment, ms-swift and the installation of related dependencies.

```bash
# Setting a PIP Global Image (Accelerated Download)
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
# Install ms-swift
git clone https://github.com/modelscope/swift.git
cd swift
pip install -e '.[llm]'

# If you want to use DeepSpeed.
pip install deepspeed -U

# If you want to use auto_gptq-based Qlora training. (Recommended, better than BNB)
# Models supported by Otto_Goptek: 'Hetps://Github.Com/Moderskope/Swift/Blob/Main/Dox/Seuss/Lem/Supported Models and Datasets. Mike#Model'
# There is a correspondence between Otto_Gheptek and the bold version, please select the version according to 'Hetps://Github.Com/Judgment/Ottogt #Quike-Instarasin'
pip install auto_gptq -U

# If you want to use BNB-based Qlora training.
pip install bitsandbytes -U

# Environment alignment (usually does not need to be run. If you run the error, you can run the following code, the repository is tested with the latest environment)
pip install -r requirements/framework.txt  -U
pip install -r requirements/llm.txt  -U
```

### <u>Fine-tune large models</u>

#### Fine-tuning using python

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

#### Use CLI commands to fine-tune

```bash
# Experimental environment: A10, 3090, V100, ...
# 20GB GPU memory
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \

# Use your own dataset (we use our own conversation dataset aiwei.jsonl here)
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset chatml.jsonl \
    --output_dir output \

# Use DDP
# Experimental environment: 2 * 3090
# 2 * 23GB GPU memory
CUDA_VISIBLE_DEVICES=0,1 \
NPROC_PER_NODE=2 \
swift sft \
    --model_id_or_path qwen/Qwen-7B-Chat \
    --dataset AI-ModelScope/blossom-math-v2 \
    --output_dir output \

# Multi-machine multi-card
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

In order to lower the threshold for use, Swift has also thoughtfully added [Interface Training Inference](https://github.com/modelscope/swift/blob/main/docs/source/GetStarted/%E7%95%8C%E9%9D%A2%E8%AE%AD%E7%BB%83%E6%8E%A8%E7%90%86.md "界面训练推理")method。There is also the use of [sh script](https://github.com/modelscope/swift/blob/main/examples/pytorch/llm/scripts/qwen1half_7b_chat_awq/lora "sh脚本")。There is also the use of [sh script]. You can check out the [official documentation](https://github.com/modelscope/swift/blob/main/docs/source "官方文档") of swift on Github.

## 📃 Quantify large models

SWIFT supports the quantification of models using AWQ, GPTQ, BNB, HQQ, and EETQ technologies. Among them, AWQ and GPTQ quantization support VLLM for inference acceleration, which requires the use of calibration datasets, which has better quantization performance but slower quantization speed. On the other hand, BNB, HQQ, and EETQ do not need calibration data, and the quantization speed is faster. All five quantification methods support Qlora fine-tuning.

AWQ and GPTQ need to be quantified using 'swift export'. BNB, HQQ, and EETQ can be quickly quantified directly at SFT and INFER time.

From the perspective of VLLM inference acceleration support, AWQ and GPTQ are more recommended for quantization. From the perspective of quantifying the effect, it is more recommended to use AWQ, HQQ and GPTQ for quantification. From the perspective of quantization speed, it is more recommended to use HQQ for quantization.

Here we recommend using the AWQ quantification technique for QLORA fine-tuning.

### Environment preparation

GPU devices: A10, 3090, V100, A100 are acceptable.

```bash
# Quantify using awq:
# There is a correspondence between the AutoAWQ and CUDA versions, please select the version according to 'https://github.com/casper-hansen/AutoAWQ'
pip install autoawq -U

# Quantification using GPTQ:
# There is a correspondence between Otto_Gheptek and the bold version, please select the version according to 'Hetps://Github.Com/Judgment/Ottogt #Quike-Instarasin'
pip install auto_gptq -U

# Quantifying with BNB:
pip install bitsandbytes -U

# Quantification using HQQ:
# Transformers version > 4.40 is required, installed from source
pip install git+https://github.com/huggingface/transformers
pip install hqq
# If you want to be compatible with training, you need to install PEFT from the source code
pip install git+https://github.com/huggingface/peft.git

# Quantify using EETQ:
# Transformers version > 4.40 is required, installed from source
pip install git+https://github.com/huggingface/transformers
# Refer to https://github.com/NetEase-FuXi/EETQ
git clone https://github.com/NetEase-FuXi/EETQ.git
cd EETQ/
git submodule update --init --recursive
pip install .
# If you want to be compatible with training, you need to install PEFT from the source code
pip install git+https://github.com/huggingface/peft.git

# Environment alignment (usually does not need to be run. If you run the error, you can run the following code, the repository is tested with the latest environment)
pip install -r requirements/framework.txt  -U
pip install -r requirements/llm.txt  -U
```

## <u>Quantify the fine-tuned model</u>

```bash
# 'alpaca-zh alpaca-en sharegpt-gpt4-mini' was used as the quantitative data set
CUDA_VISIBLE_DEVICES=0 swift export \
    --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx' \
    --merge_lora true --quant_bits 4 \
    --dataset alpaca-zh alpaca-en sharegpt-gpt4-mini --quant_method awq

# Use the dataset used when fine-tuning as the quantification dataset
CUDA_VISIBLE_DEVICES=0 swift export \
    --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx' \
    --merge_lora true --quant_bits 4 \
    --load_dataset_config true --quant_method awq
```

## 🔥 Model inference

### Large model after inference fine-tuning

```bash
# The AWQ/GPTQ quantization model supports VLLM inference acceleration. Model deployment is also supported.
CUDA_VISIBLE_DEVICES=0 swift infer --ckpt_dir 'output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx-merged-awq-int4'
```

### Inference effect

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

### Model push

- If you want to push your debugged model to your own Magic Community, you can use the following command. After that, you can find your model on the `I Created` section of the Moda Community homepage. If you want to publish it, remember to write the `README.md`
  
  ```bash
  # Push the original quantization model
  CUDA_VISIBLE_DEVICES=0 swift export \
      --model_type qwen1half-7b-chat \
      --model_id_or_path qwen1half-7b-chat-gptq-int4 \
      --push_to_hub true \
      --hub_model_id qwen1half-7b-chat-gptq-int4 \
      --hub_token '<your-sdk-token>'
  
  # Push the LoRa incremental model
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>'
  
  # Push the merged model
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>' \
      --merge_lora true
  
  # Push the quantized model
  CUDA_VISIBLE_DEVICES=0 swift export \
      --ckpt_dir output/qwen1half-4b-chat/vx-xxx/checkpoint-xxx \
      --push_to_hub true \
      --hub_model_id qwen1half-4b-chat-lora \
      --hub_token '<your-sdk-token>' \
      --merge_lora true \
      --quant_bits 4
  ```
