### 1. Deployment Environment
- Operating system: Ubuntu 22.04.4 LTS
- CPU: Intel (R) Xeon (R) CPU E 5-2650, 32G
- Graphics card: NVIDIA RTX 4060Ti 16G, NVIDIA-SMI 535.104.05  Driver Version: 535.104.05  CUDA Version: 12.2
- Python 3.11.5

### 2. Default Deployment Steps
- 1. Clone the code or manually download the code and place it on the server:
```
git clone https://github.com/SmartFlowAI/EmoLLM.git
```
- 2. Install Python dependencies:
```
# cd EmoLLM
# pip install -r requirements.txt
```
- 3. Install the oss2 library for automatic model download (missing from the requirements.txt file):
```
# pip install oss2
```
- 4. Important:Download the model catalog, select the model you want to use, to download the model catalog manually, go to openxlab (like [EmoLLM_Model](https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model)) or Huggingface or other platforms, Place all files in the `EmoLLM/model` directory. Note that this step is mandatory, otherwise the automatic download will report an error, The package download does not download the full LFS (like pytorch_model-00001-of-00008.bin) file, just a reference to it.
- 5. Download the model, specifically the pytorch_model-XXX.bin file in the model,  
models can be downloaded manually or automatically. 
- 5.1. Models can be downloaded manually from openxlab or other platforms, put all the files in the `EmoLLM/model` directory, and then modify the web_demo-aiwei.py or web_internlm2.py files (whichever one is called by app.py) by commenting out the following code at the beginning, to prevent the script from automatically re-downloading the model： 
```
# download(model_repo='ajupyter/EmoLLM_aiwei',
#        output='model')
```
- 5.2. Automatic model download, There are three files in the EmoLLM directory, app.py、web_demo-aiwei.py、web_internlm2.py, app.py calls the last two scripts. Comment out the other script if you want to call it. Run:
```
# python ./app.py
```
- Note: By default, web_demo-aiwei.py automatically downloads the ajupyter/EmoLLM_aiwei model of openxlab platform, and web_internlm2.py downloads the jujimeizuo/EmoLLM_Model model. The script will automatically download the model to EmoLLM/model directory, after the download is completed and run successfully, follow the manual download operation in 5.1 to modify the web_demo-aiwei.py or web_internlm2.py file to comment out the download code, so as to prevent re-downloading in the next run.
6、 Run app.py and wait for the model to download and load. Then access the model web page through your browser by going to: http://0.0.0.0:7860 address. You can modify the app.py file to change the web page access port.
7. Use of other models,  EmoLLM offers several versions of the open source model, uploaded to openxlab、Huggingface, and other platforms. There are roles such as the [father's boyfriend counselor](https://openxlab.org.cn/models/detail/chg0901/EmoLLM_Daddy-like_BF), [the old mother's counselor](https://huggingface.co/brycewang2018/EmoLLM-mother/tree/main), and [the gentle royal psychiatrist](https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_aiwei). There are several models to choose from such as EmoLLM_internlm2_7b_full, EmoLLM-InternLM7B-base-10e and so on.
Current review [EmoLLM_internlm2_7b_ful] (https://openxlab.org.cn/models/detail/ajupyter/EmoLLM_internlm2_7b_full) model works better. You can repeat steps 4 and 5 to download the model manually or automatically in the `EmoLLM/model` directory or modify the download function in web_demo-aiwei.py or web_internlm2.py to download the model automatically.