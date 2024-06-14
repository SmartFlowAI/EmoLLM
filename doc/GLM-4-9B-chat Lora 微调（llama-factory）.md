# GLM4-9B-chat Lora 微调.

介绍如何基于 llama-factory 框架，对 glm-4-9b-chat 模型进行 Lora 微调。Lora 是一种高效微调方法，深入了解其原理可参见博客：[知乎|深入浅出 Lora](https://zhuanlan.zhihu.com/p/650197598)。

## 一、环境准备
我们实践了两种平台进行选择
*  在[autodl](https://www.autodl.com/)平台中租一个3090等24G显存的显卡机器，如下图所示镜像选择`PyTorch`-->`2.0.0`-->`3.8(ubuntu20.04)`-->`11.8`
![autodl](../xtuner_config/images/autodl.png)
  
  
*  在 [InternStudio](https://studio.intern-ai.org.cn/) 平台中选择 A100(1/4) 的配置，如下图所示镜像选择 `Cuda11.7-conda`，如下图所示：
![internstudio](../xtuner_config/images/internstudio.png)
在Terminal中，进行pip换源和安装依赖包

## 环境配置

在完成基本环境配置和本地模型部署的情况下，你还需要安装一些第三方库，可以使用以下命令：

```bash
python -m pip install --upgrade pip
# 更换 pypi 源加速库的安装
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 LLaMA-Factory
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
#上面这步操作会完成torch、transformers、datasets等相关依赖包的安装

```


## 二、模型下载

使用 `modelscope` 中的`snapshot_download`函数下载模型，第一个参数为模型名称，参数`cache_dir`为模型的下载路径。

在 `/root/autodl-tmp` 路径下新建 `download.py` 文件并在其中输入以下内容，粘贴代码后记得保存文件，如下图所示。并运行 `python /root/autodl-tmp/download.py`执行下载，模型大小为 14 GB，下载模型大概需要 10~20 分钟

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('ZhipuAI/glm-4-9b-chat', cache_dir='/root/autodl-tmp', revision='master')
```

## 三、指令集构建 —— Alpaca 格式

 LLaMA-Factory 支持 alpaca 格式和 sharegpt 格式的数据集,本次微调我们使用 alpaca 格式

### 指令监督微调数据格式说明

在指令监督微调时，`instruction` 列对应的内容会与 `input` 列对应的内容拼接后作为人类指令，即人类指令为 `instruction\ninput`。而 `output` 列对应的内容为模型回答。

如果指定，`system` 列对应的内容将被作为系统提示词。

`history` 列是由多个字符串二元组构成的列表，分别代表历史消息中每轮对话的指令和回答。注意在指令监督微调时，历史消息中的回答内容**也会被用于模型学习**。

```json
[
  {
    "instruction": "人类指令（必填）",
    "input": "人类输入（选填）",
    "output": "模型回答（必填）",
    "system": "系统提示词（选填）",
    "history": [
      ["第一轮指令（选填）", "第一轮回答（选填）"],
      ["第二轮指令（选填）", "第二轮回答（选填）"]
    ]
  }
]
```


### 单轮对话数据的格式转换
使用以下程序将[数据集](../datasets/)转换成 alpaca 格式
```python
import json
import re

# 选择要格式转换的数据集
file_name = "single_turn_dataset_1.json"
#file_name = "single_turn_dataset_2.json"

system_prompt = "如果要添加系统提示词，请放在这里"

with open(f'../{file_name}', 'rt', encoding='utf-8') as file:
    data = json.load(file)

converted_data = [{"instruction": item["prompt"], 
                   "input": "", 
                   "output": item["completion"],
                   "system": system_prompt
                  } for item in data]

for i in range(len(converted_data)):

    # 数据清洗-去掉特殊符号
    if "🐳" in converted_data[i]["output"]:
        converted_data[i]["output"] = converted_data[i]["output"].replace("🐳", "")
        
    # 数据清洗-去掉“你好，我是红烧肉”，会影响大模型的自我认知
    if '好，我是' in converted_data[i]["output"]:
        converted_data[i]["output"] = converted_data[i]["output"].strip()
        intro_pattern = r"^[^\n]+\n"
        converted_data[i]["output"] = re.sub(intro_pattern, "", converted_data[i]["output"]).strip() 

with open(f'./processed/{file_name}', 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=4)
print(f'./processed/{file_name} Done')

```

### 多轮对话数据的格式转换
使用以下程序将[数据集](../datasets/)转换成 alpaca 格式
```python
from tqdm import tqdm
import json

# 选择要格式转换的数据集
file_name = "data.json"
#file_name = "data_pro.json"
#file_name = "multi_turn_dataset_1.json"
#file_name = "multi_turn_dataset_2.json"
#file_name = "aiwei.json"

system_prompt = "如果要添加系统提示词，请放在这里"

with open(f'../{file_name}', 'rt', encoding='utf-8') as file:
    data = json.load(file)

# 遍历原始数据，进行格式转换

# 转换后的数据格式
converted_data = []
for item in tqdm(data):
    conversation = item['conversation']
    history = [(c['input'], c['output']) for c in conversation[:-1]]
    last_item = conversation[-1]
    converted_data.append({
        "instruction": last_item['input'],
        "input": "",
        "output": last_item['output'],
        "system": system_prompt,
        "history": history
    })
    # 将转换后的数据转换为JSON格式
    converted_json = json.dumps(converted_data, ensure_ascii=False, indent=4)

with open(f'./processed/{file_name}', 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=4)
```


### 角色扮演数据的格式转换
代码同上，根据原数据集是单轮对话还是多轮对话来选择。注意设置各个角色的“system_prompt”。


### 数据集合并
为了方便处理（不想在LLaMA-Factory中添加太多的数据集），这里将所有已经处理好的 alpaca 格式的数据集（每一个数据集文件都是一个json字符串）合并成一个文件（一个大的json字符串），合并代码如下：
```python
import json

# 初始化一个空列表来存储所有数据
merged_data = []
file_list = [
    "single_turn_dataset_1.json",
    "single_turn_dataset_2.json",
    "self_cognition_EmoLLM.json",
    "ruozhiba_raw.json",
    "data.json",
    "data_pro.json",
    "multi_turn_dataset_1.json",
    "multi_turn_dataset_2.json",
    "aiwei.json",
    "tiangou.json",
    "SoulStar_data.json",
    "mother_v2.json",
    "scientist.json"
]

# 遍历所有文件并读取数据
for filename in file_list:
    with open(f"./processed/{filename}", 'r', encoding='utf-8') as file:
        data = json.load(file)
        merged_data.extend(data)

# 将合并后的数据写入新的 JSON 文件
with open('emo_glm4_merged_data.json', 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print("合并完成，已保存到 emo_glm4_merged_data.json 文件中。")
```


### 将数据集配置到LLaMA-Factory 中

修改 LLaMa-Factory 目录中的 data/dataset_info.json 文件，在其中添加：

```json
"emo_merged": {
  "file_name": "emo_glm4_merged_data.json文件的绝对路径",
  }
}
```

## 四、微调模型
在 LLaMA-Factory 目录中新建配置文件 emo_glm4_lora_sft.yaml ：
```python
### model
model_name_or_path: glm-4-9b-chat模型地址的绝对路径

### method
stage: sft
do_train: true
finetuning_type: lora
lora_target: all

### dataset
# dataset 要和 data/dataset_info.json 中添加的信息保持一致
dataset: emo_merged
template: glm4
cutoff_len: 2048
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 16

### output
# output_dir是模型训练过程中的checkpoint，训练日志等的保存目录
output_dir: saves/emo-glm4-epoch10/lora/sft
logging_steps: 10
#save_steps: 500
plot_loss: true
overwrite_output_dir: true
save_strategy: epoch

### train
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
learning_rate: 1.0e-4
num_train_epochs: 10.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
fp16: true

### eval
do_eval: false
val_size: 0.1
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 10
```

执行以下命令开始微调：
```bash
cd LLaMA-Factory
llamafactory-cli train glm4_emo_lora_sft.yaml
```

训练完成后，在 LLaMA-Factory 目录中新建配置文件 emo_glm4_lora_sft_export.yaml:

```python
### model
model_name_or_path: glm-4-9b-chat模型地址的绝对路径
# 刚才emo_glm4_lora_sft.yaml文件中的 output_dir
adapter_name_or_path: saves/emo-glm4-epoch10/lora/sft
template: glm4
finetuning_type: lora

### export
export_dir: models/EmoLLM-glm-4-9b-chat
export_size: 2
export_device: cpu
export_legacy_format: false
```

## 五、合并模型

执行以下命令开始合并模型：
```bash
cd LLaMA-Factory
llamafactory-cli export emo_glm4_lora_sft_export.yaml
```

在 models/EmoLLM-glm-4-9b-chat 目录中就可以获得经过Lora微调后的完整模型。

模型权重已开源：[ModelScope](https://www.modelscope.cn/models/wwewwt/EmoLLM-glm-4-9b-chat/summary)