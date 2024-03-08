![](../assets/emoxlmdeploy.png)
# LMDeploy本地部署
## 1.环境配置
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
但是lmdeploy的0.1.0版本并不支持InternLM2-7B-chat的Turbomind转化  
注意lmdeploy的版本要要进行更新:  
```
# 我们使用的是0.2.4版本的lmdeploy
pip install --upgrade lmdeploy
```

## 2.模型转化
使用 TurboMind 推理模型需要先将模型转化为 TurboMind 的格式，目前支持在线转换和离线转换两种形式。在线转换可以直接加载 Huggingface 模型，离线转换需需要先保存模型再加载。

TurboMind 是一款关于 LLM 推理的高效推理引擎，基于英伟达的 FasterTransformer 研发而成。它的主要功能包括：LLaMa 结构模型的支持，persistent batch 推理模式和可扩展的 KV 缓存管理器。
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
#  转换模型（FastTransformer格式） TurboMind
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
