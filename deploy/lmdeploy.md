![](../assets/emoxlmdeploy.png)
# LMDeploy本地部署
## 0. LMDeploy简介
LMDeploy 由 [MMDeploy](https://github.com/open-mmlab/mmdeploy) 和 [MMRazor](https://github.com/open-mmlab/mmrazor) 团队联合开发，是涵盖了 LLM 任务的全套轻量化、部署和服务解决方案。 这个强大的工具箱提供以下核心功能：

- 高效的推理：LMDeploy 开发了 Persistent Batch(即 Continuous Batch)，Blocked K/V Cache，动态拆分和融合，张量并行，高效的计算 kernel等重要特性。推理性能是 vLLM 的 1.8 倍

- 可靠的量化：LMDeploy 支持权重量化和 k/v 量化。4bit 模型推理效率是 FP16 下的 2.4 倍。量化模型的可靠性已通过 OpenCompass 评测得到充分验证。

- 便捷的服务：通过请求分发服务，LMDeploy 支持多模型在多机、多卡上的推理服务。

- 有状态推理：通过缓存多轮对话过程中 attention 的 k/v，记住对话历史，从而避免重复处理历史会话。显著提升长文本多轮对话场景中的效率。
## 1. 环境配置
<details>
  
<summary>具体部署环境</summary>

Package                   Version  

------------------------- -----------  

accelerate                0.27.2  
addict                    2.4.0  
aiofiles                  23.2.1  
aiohttp                   3.9.3  
aiosignal                 1.3.1  
aliyun-python-sdk-core    2.14.0  
aliyun-python-sdk-kms     2.16.2  
altair                    5.2.0  
annotated-types           0.6.0  
anyio                     4.2.0  
async-timeout             4.0.3  
attrs                     23.2.0  
blinker                   1.7.0  
Brotli                    1.0.9  
cachetools                5.3.3  
certifi                   2023.11.17  
cffi                      1.16.0  
charset-normalizer        2.0.4  
click                     8.1.7  
contourpy                 1.2.0  
crcmod                    1.7  
cryptography              41.0.3  
cycler                    0.12.1  
datasets                  2.17.0  
dill                      0.3.8  
einops                    0.7.0  
exceptiongroup            1.2.0  
fastapi                   0.109.2  
ffmpy                     0.3.2  
filelock                  3.13.1  
fire                      0.5.0  
flash-attn                2.4.2  
fonttools                 4.49.0  
frozenlist                1.4.1  
fsspec                    2023.10.0  
fuzzywuzzy                0.18.0  
gitdb                     4.0.11  
GitPython                 3.1.42  
gmpy2                     2.1.2  
gradio                    3.50.2  
gradio_client             0.6.1  
h11                       0.14.0  
httpcore                  1.0.3  
httpx                     0.26.0  
huggingface-hub           0.20.3  
idna                      3.4  
importlib-metadata        6.11.0  
importlib-resources       6.1.1  
Jinja2                    3.1.2  
jmespath                  0.10.0  
jsonschema                4.21.1  
jsonschema-specifications 2023.12.1  
kiwisolver                1.4.5  
lmdeploy                  0.2.4  
markdown-it-py            3.0.0  
MarkupSafe                2.1.1  
matplotlib                3.8.3  
mdurl                     0.1.2  
mkl-fft                   1.3.8  
mkl-random                1.2.4  
mkl-service               2.4.0  
mmengine-lite             0.10.3  
mpmath                    1.3.0  
multidict                 6.0.5  
multiprocess              0.70.16  
networkx                  3.1  
ninja                     1.11.1.1  
numpy                     1.26.2  
nvidia-cublas-cu11        11.11.3.6  
nvidia-cuda-runtime-cu11  11.8.89  
nvidia-nccl-cu11          2.19.3  
openxlab                  0.0.34  
orjson                    3.9.14  
oss2                      2.17.0  
packaging                 23.2  
pandas                    2.2.0  
peft                      0.8.2  
Pillow                    9.5.0  
pip                       23.3.1  
platformdirs              4.2.0  
protobuf                  4.25.3  
psutil                    5.9.8  
pyarrow                   15.0.0  
pyarrow-hotfix            0.6  
pybind11                  2.11.1  
pycparser                 2.21  
pycryptodome              3.20.0 
pydantic                  2.6.1 
pydantic_core             2.16.2  
pydeck                    0.8.1b0  
pydub                     0.25.1  
Pygments                  2.17.2  
Pympler                   1.0.1  
pynvml                    11.5.0  
pyOpenSSL                 23.2.0  
pyparsing                 3.1.1  
PySocks                   1.7.1  
python-dateutil           2.8.2  
python-multipart          0.0.9  
pytz                      2023.4  
pytz-deprecation-shim     0.1.0.post0  
PyYAML                    6.0.1  
referencing               0.33.0  
regex                     2023.12.25  
requests                  2.28.2  
rich                      13.4.2  
rpds-py                   0.18.0  
safetensors               0.4.2  
semantic-version          2.10.0  
sentencepiece             0.1.99  
setuptools                60.2.0  
shortuuid                 1.0.11  
six                       1.16.0  
smmap                     5.0.1  
sniffio                   1.3.0  
starlette                 0.36.3  
streamlit                 1.24.0  
sudo                      1.0.0  
sympy                     1.11.1  
tenacity                  8.2.3  
termcolor                 2.4.0  
tiktoken                  0.6.0  
tokenizers                0.15.2  
toml                      0.10.2  
tomli                     2.0.1  
toolz                     0.12.1  
torch                     2.0.1  
torchaudio                2.0.2  
torchvision               0.15.2  
tornado                   6.4  
tqdm                      4.65.2  
transformers              4.37.1  
triton                    2.2.0  
typing_extensions         4.9.0  
tzdata                    2024.1  
tzlocal                   4.3.1  
urllib3                   1.26.18  
uvicorn                   0.27.1  
validators                0.22.0  
watchdog                  4.0.0  
websockets                11.0.3  
wheel                     0.41.2  
xxhash                    3.4.1  
yapf                      0.40.2  
yarl                      1.9.4  
zipp                      3.17.0  
</details>

lmdeploy 没有安装，我们接下来手动安装一下，建议安装最新的稳定版。 如果是在 InternStudio 开发环境，需要先运行下面的命令，否则会报错。 
```
# 解决 ModuleNotFoundError: No module named 'packaging' 问题
pip install packaging
# 使用 flash_attn 的预编译包解决安装过慢问题
pip install /root/share/wheels/flash_attn-2.4.2+cu118torch2.0cxx11abiTRUE-cp310-cp310-linux_x86_64.whl
```
由于默认安装的是 runtime 依赖包，但是我们这里还需要部署和量化，所以，这里选择 [all]。然后可以再检查一下 lmdeploy 包，如下图所示
```
pip install 'lmdeploy[all]==v0.1.0'
```
EMOLLM 是由 InternLM2 训练而来，但是lmdeploy的0.1.0版本并不支持InternLM2-7B-chat的Turbomind转化  
注意lmdeploy的版本要要进行更新:  
```
# 我们使用的是0.2.4版本的lmdeploy
pip install --upgrade lmdeploy
```

## 2. 模型转化
使用 LMDeploy 中的推理引擎 TurboMind 推理模型需要先将模型转化为 TurboMind 的格式，目前支持在线转换和离线转换两种形式。在线转换可以直接加载 Huggingface 模型，离线转换需需要先保存模型再加载。

TurboMind 是一款关于 LLM 推理的高效推理引擎，基于英伟达的 FasterTransformer 研发而成。它的主要功能包括：LLaMa 结构模型的支持，persistent batch 推理模式和可扩展的 KV 缓存管理器。
TurboMind结构如下：
![turbomind结构](../assets/turbomind结构.png)
### 2.1 在线转化
lmdeploy 支持直接读取 Huggingface 模型权重，目前共支持三种类型：

在 huggingface.co 上面通过 lmdeploy 量化的模型，如 llama2-70b-4bit, internlm-chat-20b-4bit
huggingface.co 上面其他 LM 模型，如 Qwen/Qwen-7B-Chat
示例如下：
```
# 需要能访问 Huggingface 的网络环境
lmdeploy chat turbomind internlm/internlm-chat-20b-4bit --model-name internlm-chat-20b
lmdeploy chat turbomind Qwen/Qwen-7B-Chat --model-name qwen-7b
```
上面两行命令分别展示了如何直接加载 Huggingface 的模型，第一条命令是加载使用 lmdeploy 量化的版本，第二条命令是加载其他 LLM 模型。

我们也可以直接启动本地的 Huggingface 模型，如下所示。
```
lmdeploy chat turbomind /EmoLLM  --model-name internlm2-chat-7b
```
以上命令都会启动一个本地对话界面，通过 Bash 可以与 LLM 进行对话。
### 2.2 离线转化
离线转换需要在启动服务之前，将模型转为 lmdeploy TurboMind 的格式，如下所示。
```
# 转换模型（FastTransformer格式） TurboMind
lmdeploy convert internlm2-chat-7b /EmoLLM
```
执行完成后将会在当前目录生成一个```workspace```的文件夹。这里面包含的就是 TurboMind 和 Triton “模型推理”需要到的文件。
## 3.本地运行
### 3.1 TurboMind 推理+命令行本地对话
模型转换完成后，我们就具备了使用模型推理的条件，接下来就可以进行真正的模型推理环节。

我们先尝试本地对话（Bash Local Chat），下面用（Local Chat 表示）在这里其实是跳过 API Server 直接调用 TurboMind。简单来说，就是命令行代码直接执行 TurboMind。所以说，实际和前面的架构图是有区别的。

这里支持多种方式运行，比如Turbomind、PyTorch、DeepSpeed。但 PyTorch 和 DeepSpeed 调用的其实都是 Huggingface 的 Transformers 包，PyTorch表示原生的 Transformer 包，DeepSpeed 表示使用了 DeepSpeed 作为推理框架。Pytorch/DeepSpeed 目前功能都比较弱，不具备生产能力，不推荐使用。

执行命令如下。
```
# Turbomind + Bash Local Chat
lmdeploy chat turbomind ./workspace
```
输入后两次回车，退出时输入exit 回车两次即可。此时，Server 就是本地跑起来的模型（TurboMind），命令行可以看作是前端。
### 3.2 TurboMind推理+API服务
在上面的部分我们尝试了直接用命令行启动 Client，接下来我们尝试如何运用 lmdepoy 进行服务化
首先，通过下面命令启动服务。
```
lmdeploy serve api_server ./workspace --server-name 0.0.0.0 --server-port ${server_port} --tp 1
```
详细内容请见[文档](https://lmdeploy.readthedocs.io/zh-cn/stable/serving/restful_api.html)

## 4. 模型量化

模型量化主要包括 KV Cache 量化和模型参数量化。量化是一种以参数或计算中间结果精度下降换空间节省（以及同时带来的性能提升）的策略。

前置概念：

- 计算密集（compute-bound）: 指推理过程中，绝大部分时间消耗在数值计算上；针对计算密集型场景，可以通过使用更快的硬件计算单元来提升计算速。
- 访存密集（memory-bound）: 指推理过程中，绝大部分时间消耗在数据读取上；针对访存密集型场景，一般通过减少访存次数、提高计算访存比或降低访存量来优化。

常见的 LLM 模型由于 Decoder Only 架构的特性，实际推理时大多数的时间都消耗在了逐 Token 生成阶段（Decoding 阶段），是典型的访存密集型场景。

对于优化 LLM 模型推理中的访存密集问题，我们可以使用 **KV Cache 量化**和 **4bit Weight Only 量化（W4A16）**。KV Cache 量化是指将逐 Token（Decoding）生成过程中的上下文 K 和 V 中间结果进行 INT8 量化（计算时再反量化），以降低生成过程中的显存占用。4bit Weight 量化，将 FP16 的模型权重量化为 INT4，Kernel 计算时，访存量直接降为 FP16 模型的 1/4，大幅降低了访存成本。Weight Only 是指仅量化权重，数值计算依然采用 FP16（需要将 INT4 权重反量化）。

### 4.1 KV Cache 量化

#### 4.1.1 量化步骤

KV Cache 量化是将已经生成序列的 KV 变成 Int8，使用过程一共包括三步：

第一步：计算 minmax。主要思路是通过计算给定输入样本在每一层不同位置处计算结果的统计情况。

- 对于 Attention 的 K 和 V：取每个 Head 各自维度在所有Token的最大、最小和绝对值最大值。对每一层来说，上面三组值都是 `(num_heads, head_dim)` 的矩阵。这里的统计结果将用于本小节的 KV Cache。
- 对于模型每层的输入：取对应维度的最大、最小、均值、绝对值最大和绝对值均值。每一层每个位置的输入都有对应的统计值，它们大多是 `(hidden_dim, )` 的一维向量，当然在 FFN 层由于结构是先变宽后恢复，因此恢复的位置维度并不相同。这里的统计结果用于下个小节的模型参数量化，主要用在缩放环节。

第一步执行命令如下：

```bash
# 计算 minmax
lmdeploy lite calibrate \
  --model  /EmoLLM \
  --calib_dataset "c4" \
  --calib_samples 128 \
  --calib_seqlen 2048 \
  --work_dir ./quant_output
```

在这个命令行中，会选择 128 条输入样本，每条样本长度为 2048，数据集选择 C4，输入模型后就会得到上面的各种统计值。值得说明的是，如果显存不足，可以适当调小 samples 的数量或 sample 的长度。

> 这一步需要从 Huggingface 下载 "c4" 数据集，国内经常不成功。对于在InternStudio 上的用户，需要对读取数据集的代码文件做一下替换。共包括两步：
>
> - 第一步：复制 `calib_dataloader.py` 到安装目录替换该文件：`cp /root/share/temp/datasets/c4/calib_dataloader.py  /root/.conda/envs/lmdeploy/lib/python3.10/site-packages/lmdeploy/lite/utils/`
> - 第二步：将用到的数据集（c4）复制到下面的目录：`cp -r /root/share/temp/datasets/c4/ /root/.cache/huggingface/datasets/` 

第二步：通过 minmax 获取量化参数。主要就是利用下面这个公式，获取每一层的 K V 中心值（zp）和缩放值（scale）。

```bash
zp = (min+max) / 2
scale = (max-min) / 255
quant: q = round( (f-zp) / scale)
dequant: f = q * scale + zp
```

有这两个值就可以进行量化和解量化操作了。具体来说，就是对历史的 K 和 V 存储 quant 后的值，使用时在 dequant。

第二步的执行命令如下：

```bash
# 通过 minmax 获取量化参数
lmdeploy lite kv_qparams \
  --work_dir ./quant_output  \
  --turbomind_dir workspace/triton_models/weights/ \
  --kv_sym False \
  --num_tp 1
```

在这个命令中，`num_tp` 的含义前面介绍过，表示 Tensor 的并行数。每一层的中心值和缩放值会存储到 `workspace` 的参数目录中以便后续使用。`kv_sym` 为 `True` 时会使用另一种（对称）量化方法，它用到了第一步存储的绝对值最大值，而不是最大值和最小值。

第三步：修改配置。也就是修改 `weights/config.ini` 文件（KV int8 开关），只需要把 `quant_policy` 改为 4 即可。

这一步需要额外说明的是，如果用的是 TurboMind1.0，还需要修改参数 `use_context_fmha`，将其改为 0。

接下来就可以正常运行前面的各种服务了，只不过咱们现在可是用上了 KV Cache 量化，能更省（运行时）显存了。

### 4.2 W4A16 量化

#### 4.2.1 量化步骤

W4A16中的A是指Activation，保持FP16，只对参数进行 4bit 量化。使用过程也可以看作是三步。

第一步：同 4.1.1，不再赘述。

第二步：量化权重模型。利用第一步得到的统计值对参数进行量化，具体又包括两小步：

- 缩放参数。
- 整体量化。

第二步的执行命令如下：

```bash
# 量化权重模型
lmdeploy lite auto_awq \
  --model  /EmoLLM \
  --w_bits 4 \
  --w_group_size 128 \
  --work_dir ./quant_output 
```

命令中 `w_bits` 表示量化的位数，`w_group_size` 表示量化分组统计的尺寸，`work_dir` 是量化后模型输出的位置。这里需要特别说明的是，因为没有 `torch.int4`，所以实际存储时，8个 4bit 权重会被打包到一个 int32 值中。所以，如果你把这部分量化后的参数加载进来就会发现它们是 int32 类型的。

最后一步：转换成 TurboMind 格式。

```bash
# 转换模型的layout，存放在默认路径 ./workspace 下
lmdeploy convert  internlm2-chat-7b ./quant_output \
    --model-format awq \
    --group-size 128
```

这个 `group-size` 就是上一步的那个 `w_group_size`。如果不想和之前的 `workspace` 重复，可以指定输出目录：`--dst_path`，比如：

```bash
lmdeploy convert  internlm2-chat-7b ./quant_output \
    --model-format awq \
    --group-size 128 \
    --dst_path ./workspace_quant
```

接下来和上一节一样，可以正常运行前面的各种服务了，不过咱们现在用的是量化后的模型。

最后再补充一点，量化模型和 KV Cache 量化也可以一起使用，以达到最大限度节省显存。


### 4.3 最佳实践

首先我们需要明白一点，服务部署和量化是没有直接关联的，量化的最主要目的是降低显存占用，主要包括两方面的显存：模型参数和中间过程计算结果。前者对应 W4A16 量化，后者对应 KV Cache 量化。

量化在降低显存的同时，一般还能带来性能的提升，因为更小精度的浮点数要比高精度的浮点数计算效率高，而整型要比浮点数高很多。

所以我们的建议是：在各种配置下尝试，看效果能否满足需要。这一般需要在自己的数据集上进行测试。具体步骤如下。

- Step1：优先尝试正常（非量化）版本，评估效果。
    - 如果效果不行，需要尝试更大参数模型或者微调。
    - 如果效果可以，跳到下一步。
- Step2：尝试正常版本+KV Cache 量化，评估效果。
    - 如果效果不行，回到上一步。
    - 如果效果可以，跳到下一步。
- Step3：尝试量化版本，评估效果。
    - 如果效果不行，回到上一步。
    - 如果效果可以，跳到下一步。
- Step4：尝试量化版本+ KV Cache 量化，评估效果。
    - 如果效果不行，回到上一步。
    - 如果效果可以，使用方案。


另外需要补充说明的是，使用哪种量化版本、开启哪些功能，除了上述流程外，**还需要考虑框架、显卡的支持情况**，比如有些框架可能不支持 W4A16 的推理，那即便转换好了也用不了。

根据实践经验，一般情况下：

- 精度越高，显存占用越多，推理效率越低，但一般效果较好。
- Server 端推理一般用非量化版本或半精度、BF16、Int8 等精度的量化版本，比较少使用更低精度的量化版本。
- 端侧推理一般都使用量化版本，且大多是低精度的量化版本。这主要是因为计算资源所限。

以上是针对项目开发情况，如果是自己尝试（玩儿）的话：

- 如果资源足够（有GPU卡很重要），那就用非量化的正常版本。
- 如果没有 GPU 卡，只有 CPU（不管什么芯片），那还是尝试量化版本。
- 如果生成文本长度很长，显存不够，就开启 KV Cache。

建议大家根据实际情况灵活选择方案。
更多细节查看 [LMDeploy 官方文档](https://lmdeploy.readthedocs.io/zh-cn/latest/quantization/w4a16.html)