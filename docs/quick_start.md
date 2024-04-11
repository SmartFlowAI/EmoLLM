### 1、部署环境
- 操作系统：Ubuntu 22.04.4 LTS
- CPU：Intel (R) Xeon (R) CPU E 5-2650，32G（在线 GPU 服务器）
- 显卡：NVIDIA RTX 4060Ti 16G，NVIDIA-SMI 535.104.05             Driver Version: 535.104.05   CUDA Version: 12.2
- Python 3.11.5

### 2、默认部署步骤
- 1、Clone 代码或者手动下载代码放置服务器：
```
git clone https://github.com/SmartFlowAI/EmoLLM.git
```
- 2、安装 Python 依赖库：
```
# cd EmoLLM
# pip install -r requirements.txt
```
- 3、下载模型文件，可手动下载，也可运行download_model.py 脚本自动下载模型文件。
- 3.1、自动下载模型文件，运行脚本：
```
# python download_model.py <model_repo>

# 运行 web_demo-aiwei.py 脚本对应的模型仓库地址是 ajupyter/EmoLLM_aiwei，即：
# python download_model.py ajupyter/EmoLLM_aiwei

# 运行 web_internlm2.py 脚本对应的模型仓库地址是 jujimeizuo/EmoLLM_Model，即：
# python download_model.py jujimeizuo/EmoLLM_Model

# 也可用该脚本自动下载其他模型。该脚本当前仅支持openxlab平台的模型自动下载，其他平台的模型需要手动下载。下载成功后可看到EmoLLM目录下新增 model 目录，即模型文件目录。
```
- 3.2、手动下载模型文件目录，去 openxlab、Huggingface等平台下载完整的模型目录文件，将全部文件放在 `EmoLLM/model` 目录下。注意，模型文件目录打包下载时并不会下载 LFS 文件（如 pytorch_model-00001-of-00008.bin），需要挨个下载完整的 LFS 文件。
![model](../assets/model.png)
- 4、运行脚本，app.py仅用于调用web_demo-aiwei.py 或者 web_internlm2.py 文件，想运行哪一个脚本就下载对应脚本的模型文件，然后在app.py中注释另一个脚本即可。然后运行脚本：
```
python app.py
```
5、运行 app.py 后通过浏览器访问： http://0.0.0.0:7860 地址访问模型 web 页面。可修改 app.py 文件修改 web 页面访问端口，即可正常体验该模型。如果在服务器上部署，需要配置本地端口映射。
6、替换模型，EmoLLM 提供了多种开源模型，分别上传至 openxlab、Huggingface 平台，有[爹系男友心理咨询师 ](https://openxlab.org.cn/models/detail/chg0901/EmoLLM_Daddy-like_BF)、[老母亲心理咨询师](https://huggingface.co/brycewang2018/EmoLLM-mother/tree/main)、[温柔御姐心理医生艾薇](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei)等角色，有 EmoLLM_internlm2_7b_full、EmoLLM-InternLM7B-base-10e 等多个模型可选择。可重复步骤 3、4手动或自动下载相关模型放在 `EmoLLM/model` 目录下，然后运行体验。