# ChatGLM3-6B
## 环境准备
我们实践了两种平台进行选择
*  在[autodl](https://www.autodl.com/)平台中租一个3090等24G显存的显卡机器，如下图所示镜像选择`PyTorch`-->`2.0.0`-->`3.8(ubuntu20.04)`-->`11.8`
![autodl](images/autodl.png)
  
  
*  在 [InternStudio](https://studio.intern-ai.org.cn/) 平台中选择 A100(1/4) 的配置，如下图所示镜像选择 `Cuda11.7-conda`，如下图所示：
![internstudio](images/internstudio.png)
在Terminal中，进行pip换源和安装依赖包
  
```shell
# 升级pip
python -m pip install --upgrade pip

pip install modelscope==1.9.5
pip install transformers==4.35.2
pip install streamlit==1.24.0
pip install sentencepiece==0.1.99
pip install accelerate==0.24.1
pip install peft==0.4.0
pip install datasets==2.10.1
```
## 模型下载

使用 `modelscope` 中的`snapshot_download`函数下载模型，第一个参数为模型名称，参数`cache_dir`为模型的下载路径。

在 `/root/autodl-tmp` 路径下新建 `download.py` 文件并在其中输入以下内容，粘贴代码后记得保存文件，如下图所示。并运行 `python /root/autodl-tmp/download.py`执行下载，模型大小为 14 GB，下载模型大概需要 10~20 分钟

```python
import torch
from modelscope import snapshot_download, AutoModel, AutoTokenizer
import os
model_dir = snapshot_download('ZhipuAI/chatglm3-6b', cache_dir='/root/autodl-tmp', revision='master')
```
更多关于ChatLLM的内容请详见与[self-llm](https://github.com/datawhalechina/self-llm)
## 指令集构建

LLM 的微调一般指指令微调过程。所谓指令微调，是说我们使用的微调数据形如：

```json
{
    "system":"回答以下用户问题，仅输出答案。",
    "input":"1+1等于几?",
    "output":"2"
}
```

其中，`system` 是用户指令，告知模型其需要完成的任务；`input` 是用户输入，是完成用户指令所必须的输入内容；`output` 是模型应该给出的输出。

即我们的核心训练目标是让模型具有理解并遵循用户指令的能力。因此，在指令集构建时，我们应针对我们的目标任务，针对性构建任务指令集。，我们的目标是构建一个能够模拟心理医生解决心理问题的个性化 LLM，因此我们构造的指令形如：

```json
{
    "system": "现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。",
    "input":"我觉得自己总是拖延，很难集中精力完成任务。",
    "output":"拖延问题很常见，但也是可以克服的。首先，你可以尝试为自己设定一个明确的目标，并将其拆分成小任务。这样一来，你会觉得任务变得更容易管理。此外，保持工作环境整洁有序也有助于提高工作效率。最后，当你完成一个任务时，记得给自己一些奖励，以激励自己继续前进。"
}
```
## 数据格式化

`Lora` 训练的数据是需要经过格式化、编码之后再输入给模型进行训练的，如果是熟悉 `Pytorch` 模型训练流程的同学会知道，我们一般需要将输入文本编码为 input_ids，将输出文本编码为 `labels`，编码之后的结果都是多维的向量。我们首先定义一个预处理函数，这个函数用于对每一个样本，编码其输入、输出文本并返回一个编码后的字典：

```python
def process_func(example):
    MAX_LENGTH = 512
    input_ids, labels = [], []
    instruction = tokenizer.encode(text="\n".join(["<|system|>", example["system"], "<|user|>", example["input"] + "<|assistant|>"]).strip() + "\n",
                                    add_special_tokens=True, truncation=True, max_length=MAX_LENGTH)

    response = tokenizer.encode(text=example["output"], add_special_tokens=False, truncation=True,
    max_length=MAX_LENGTH)

    input_ids = instruction + response + [tokenizer.eos_token_id]
    labels = [tokenizer.pad_token_id] * len(instruction) + response + [tokenizer.eos_token_id]
    pad_len = MAX_LENGTH - len(input_ids)
    input_ids += [tokenizer.pad_token_id] * pad_len
    labels += [tokenizer.pad_token_id] * pad_len
    labels = [(l if l != tokenizer.pad_token_id else -100) for l in labels]

    return {
        "input_ids": input_ids,
        "labels": labels
    }
```

经过格式化的数据，也就是送入模型的每一条数据，都是一个字典，包含了 `input_ids`、`labels` 两个键值对，其中 `input_ids` 是输入文本的编码，`labels` 是输出文本的编码。decode之后应该是这样的：

```text
[gMASK]sop <|system|>
现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。
<|user|>
我的团队氛围很好，同事们都很友善。而且我们经常一起出去玩，感觉像是一个大家庭一样。\n<|assistant|>
这是一个很棒的工作环境，有良好的人际关系和团队合作确实可以带来很多快乐感。不过，我也注意到你在工作中可能会遇到一些挑战，比如任务压力或者与同事之间的冲突。你有没有想过如何应对这些问题呢？
```

为什么会是这个形态呢？好问题！不同模型所对应的格式化输入都不一样，所以需要我们深度模型的训练源码来查看，因为按照原本模型指令微调的形式进行Lora微调效果应该是最好的，所以我们依然遵循原本模型的输入格式。OK，这里我给大家放一下源码的链接，各位如果感兴趣可以自行探索一下：

[hugging face ChatGLM3仓库](https://github.com/THUDM/ChatGLM3/blob/main/finetune_chatmodel_demo/preprocess_utils.py)：其中的`InputOutputDataset`类。  
此外，还可以参考这个仓库对ChatGLM的数据处理[LLaMA-Factory](https://github.com/KMnO4-zx/LLaMA-Factory/blob/main/src/llmtuner/data/template.py)。


## 加载tokenizer和半精度模型

模型以半精度形式加载，如果你的显卡比较新的话，可以用`torch.bfolat`形式加载。对于自定义的模型一定要指定`trust_remote_code`参数为`True`。

```python
tokenizer = AutoTokenizer.from_pretrained('./model/chatglm3-6b', use_fast=False, trust_remote_code=True)

# 模型以半精度形式加载，如果你的显卡比较新的话，可以用torch.bfolat形式加载
model = AutoModelForCausalLM.from_pretrained('./model/chatglm3-6b', trust_remote_code=True, torch_dtype=torch.half, device_map="auto")
```

## 定义LoraConfig

`LoraConfig`这个类中可以设置很多参数，但主要的参数没多少，简单讲一讲，感兴趣的同学可以直接看源码。

- `task_type`：模型类型
- `target_modules`：需要训练的模型层的名字，主要就是`attention`部分的层，不同的模型对应的层的名字不同，可以传入数组，也可以字符串，也可以正则表达式。
- `r`：`lora`的秩，具体可以看`Lora`原理
- `lora_alpha`：`Lora alaph`，具体作用参见 `Lora` 原理 
- `modules_to_save`指定的是除了拆成lora的模块，其他的模块可以完整的指定训练。

`Lora`的缩放是啥嘞？当然不是`r`（秩），这个缩放就是`lora_alpha/r`, 在这个`LoraConfig`中缩放就是4倍。
这个缩放的本质并没有改变LoRa的参数量大小,本质在于将里面的参数数值做广播乘法,进行线性的缩放。

```python
config = LoraConfig(
    task_type=TaskType.CAUSAL_LM, 
    target_modules=["query_key_value"],
    inference_mode=False, # 训练模式
    r=8, # Lora 秩
    lora_alpha=32, # Lora alaph，具体作用参见 Lora 原理
    lora_dropout=0.1# Dropout 比例
)
```

## 自定义 TrainingArguments 参数

`TrainingArguments`这个类的源码也介绍了每个参数的具体作用，当然大家可以来自行探索，这里就简单说几个常用的。

- `output_dir`：模型的输出路径
- `per_device_train_batch_size`：顾名思义 `batch_size`
- `gradient_accumulation_steps`: 梯度累加，如果你的显存比较小，那可以把 `batch_size` 设置小一点，梯度累加增大一些。
- `logging_steps`：多少步，输出一次`log`
- `num_train_epochs`：顾名思义 `epoch`
- `gradient_checkpointing`：梯度检查，这个一旦开启，模型就必须执行`model.enable_input_require_grads()`，这个原理大家可以自行探索，这里就不细说了。

```python
# Data collator GLM源仓库从新封装了自己的data_collator,在这里进行沿用。

data_collator = DataCollatorForSeq2Seq(
    tokenizer,
    model=model,
    label_pad_token_id=-100,
    pad_to_multiple_of=None,
    padding=False
)

args = TrainingArguments(
    output_dir="./output/ChatGLM",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    logging_steps=10,
    num_train_epochs=3,
    gradient_checkpointing=True,
    save_steps=100,
    learning_rate=1e-4,
)
```

### 使用 Trainer 训练

把 model 放进去，把上面设置的参数放进去，数据集放进去，OK！开始训练！

```python
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_id,
    data_collator=data_collator,
)
trainer.train()
```

## 模型推理

可以用这种比较经典的方式推理。

```python
while True:
    # 推理
    model = model.cuda()
    input_text = input("User  >>>")
    ipt = tokenizer("<|system|>\n现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。\n<|user|>\n {}\n{}".format(input_text, "").strip() + "<|assistant|>\n", return_tensors="pt").to(model.device)
    print(tokenizer.decode(model.generate(**ipt, max_length=128, do_sample=True)[0], skip_special_tokens=True))
```

## 重新加载
通过PEFT所微调的模型，都可以使用下面的方法进行重新加载，并推理:
- 加载源model与tokenizer；
- 使用`PeftModel`合并源model与PEFT微调后的参数。

```python
from peft import PeftModel

model = AutoModelForCausalLM.from_pretrained("./model/chatglm3-6b", trust_remote_code=True, low_cpu_mem_usage=True)
tokenizer = AutoTokenizer.from_pretrained("./model/chatglm3-6b", use_fast=False, trust_remote_code=True)

p_model = PeftModel.from_pretrained(model, model_id="./output/ChatGLM/checkpoint-1000/")  # 将训练所得的LoRa权重加载起来

while True:
    # 推理
    model = model.cuda()
    input_text = input("User  >>>")
    ipt = tokenizer("<|system|>\n现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。\n<|user|>\n {}\n{}".format(input_text, "").strip() + "<|assistant|>\n", return_tensors="pt").to(model.device)
    print(tokenizer.decode(model.generate(**ipt, max_length=128, do_sample=True)[0], skip_special_tokens=True))

```
