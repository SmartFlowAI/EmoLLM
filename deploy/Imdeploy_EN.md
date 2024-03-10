![](../assets/emoxlmdeploy.png)
# Local deployment of LMDeploy
## 1.Environment configuration
<details>
  
<summary>Specific deployment environment</summary>

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

lmdeploy has not been installed. We will install it manually next. It is recommended to install the latest stable version. If you use the InternStudio development environment, run the following command first. Otherwise, an error occurs. 
```
# Resolved ModuleNotFoundError: No module named 'packaging' problem
pip install packaging
# Use flash_attn's precompiled package to solve slow installation problems
pip install /root/share/wheels/flash_attn-2.4.2+cu118torch2.0cxx11abiTRUE-cp310-cp310-linux_x86_64.whl
```
Because the default installation is the runtime dependency package, but we also need to deploy and quantify here, so select [all] here. You can then examine the lmdeploy package again, as shown in the following figure
```
pip install 'lmdeploy[all]==v0.1.0'
```
However, the 0.1.0 version of lmdeploy does not support the Turbomind conversion of InternLM2-7B-chat
Note that the version of lmdeploy needs to be updated:  
```
# We used version 0.2.4 of lmdeploy
pip install --upgrade lmdeploy
```

## 2.Model transformation
To use TurboMind inference model, it is necessary to convert the model into TurboMind format first, which supports online conversion and offline conversion. Online conversion can directly load the Huggingface model, and offline conversion needs to save the model before loading.

TurboMind is an efficient inference engine for LLM inference, based on Nvidia's FasterTransformer. Its main features include: LLaMa structural model support, persistent batch inference mode and scalable KV cache manager.
### 2.1 Online conversion
lmdeploy supports direct reading of Huggingface model weights. Currently, three types are supported:

The models quantified by lmdeploy on huggingface.co are llama2-70b-4bit and internlm-chat-20b-4bit
Other LM models on huggingface.co, such as Qwen/ QWEN-7B-chat
An example is as follows:
```
# Requires a network environment with access to Huggingface
lmdeploy chat turbomind internlm/internlm-chat-20b-4bit --model-name internlm-chat-20b
lmdeploy chat turbomind Qwen/Qwen-7B-Chat --model-name qwen-7b
```
The above two lines show how to directly load Huggingface's model, the first to load the version quantified using lmdeploy, and the second to load the other LLM models.

We can also launch the local Huggingface model directly, as shown below.
```
lmdeploy chat turbomind /EmoLLM  --model-name internlm2-chat-7b
```
The preceding commands start a local dialog interface. You can use Bash to talk to LLM.
### 2.2 Offline conversion
The offline transformation requires converting the model to the lmdeploy TurboMind format before starting the service, as shown below.
```
#  Transform model（FastTransformer格式） TurboMind
lmdeploy convert internlm2-chat-7b /EmoLLM
```
Upon completion, a workspace folder will be generated in the current directory. These are the files that TurboMind and Triton need for "model inference."
## 3.Run locally
### 3.1 TurboMind Inference + Command line local dialog
After the model transformation is complete, we have the conditions to use model inference, and then we can proceed to the real model inference.

Let's try Bash Local Chat first, and then use Local Chat to call TurboMind instead of API Server. In simple terms, TurboMind is executed directly by command line code. So, there is a difference between the actual architecture diagram and the previous one.

There are several ways to run it, such as Turbomind, PyTorch, DeepSpeed. But PyTorch and DeepSpeed are actually Huggingface's Transformers package, PyTorch means the native Transformer package, DeepSpeed means the use of DeepSpeed as an inference framework. Pytorch/DeepSpeed is currently weak and does not have production capacity, so it is not recommended to use.

Run the following command.
```
# Turbomind + Bash Local Chat
lmdeploy chat turbomind ./workspace
```
To exit, enter exit and press enter twice. At this point, the Server is the locally run model (TurboMind), and the command line can be seen as the front end.
### 3.2 TurboMind Inference + API service
In the above part, we tried to start the Client directly using the command line. Next, we tried how to use lmdepoy to service it.
First, start the service with the following command.
```
lmdeploy serve api_server ./workspace --server-name 0.0.0.0 --server-port ${server_port} --tp 1
```
Details please see [documents](https://lmdeploy.readthedocs.io/zh-cn/stable/serving/restful_api.html)
