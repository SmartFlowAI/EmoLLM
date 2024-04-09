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
- 3、安装 oss2 库用于自动下载模型（requirements.txt 文件缺少该库） 
```
# pip install oss2
```
- 4、【重要】下载模型目录，选择你想要使用的模型，手动下载去 openxlab（如 [EmoLLM_Model](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model)） 或者 Huggingface 等其他平台下载模型目录，将全部文件放在 `EmoLLM/model` 目录下。注意，这一步必须要有，否则自动下载会报错，打包下载时并不会下载 LFS（如 pytorch_model-00001-of-00008.bin）文件的完整文件只是一个引用而已。
- 5、下载模型，特指模型中的 pytorch_model-XXX.bin 文件，可通过手动或者自动方式下载模型。 
- 5.1、模型手动下载则去 openxlab（如 [EmoLLM_Model](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model)） 或者其他平台下载模型，将全部文件放在 `EmoLLM/model` 目录下，然后修改 web_demo-aiwei.py 或者 web_internlm2.py 文件（app. Py 调用哪一个就修改哪一个文件）注释掉开头的下面代码，防止脚本自动重新下载模型： 
```
# download(model_repo='ajupyter/EmoLLM_aiwei',
#        output='model')
```
- 5.2、模型自动下载，进入 EmoLLM 目录后有三个文件，分别是 app.py、web_demo-aiwei.py、web_internlm2.py。app.py 是调用后面两个脚本的。想要调用哪一个脚本就注释掉另外一个脚本。并运行如下
```
# python ./app.py
```
- 注意：默认情况下 web_demo-aiwei.py 自动下载的是 openxlab 平台的 ajupyter/EmoLLM_aiwei 模型，web_internlm2.py 下载的是 jujimeizuo/EmoLLM_Model 模型。脚本会自动将模型下载到 EmoLLM/model 目录，下载完成成功运行后，按照 5.1 的手动下载的操作修改 web_demo-aiwei.py 或者 web_internlm2.py 文件注释掉下载代码，防止下次运行重新下载。
6、运行 app.py 后等待模型下载并且加载完毕，可通过浏览器访问： http://0.0.0.0:7860 地址访问模型 web 页面。可修改 app.py 文件修改 web 页面访问端口。
7、替换模型，EmoLLM 提供了多种开源模型，分别上传至 openxlab、Huggingface 平台，有[爹系男友心理咨询师 ](https://openxlab.org.cn/models/detail/chg0901/EmoLLM_Daddy-like_BF)、[老母亲心理咨询师](https://huggingface.co/brycewang2018/EmoLLM-mother/tree/main)、[温柔御姐心理医生艾薇](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei)等角色，有 EmoLLM_internlm2_7b_full、EmoLLM-InternLM7B-base-10e 等多个模型可选择，目前评测 [EmoLLM_internlm2_7b_ful](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full) 模型效果较好。可重复步骤 4、5手动或自动下载相关模型放在 `EmoLLM/model` 目录下或者修改 web_demo-aiwei.py 或者 web_internlm2.py 文件的 download 函数仓库地址自动下载。