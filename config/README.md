# EmoLLM_Scientist微调指南

## 数据 
微调数据共包含3800段对话，借助LLM自动生成，后续进行人工校验。数据路径：'datasets\scientist.json'

## 基座 
基座模型采用InternLM2-Chat-7B，模型介绍请见[InternLM](https://github.com/InternLM/InternLM)

## 训练方式 
基于xtuner的微调，使用xtuner的train命令行工具，使用命令如下：
### 安装依赖

```bash
cd xtuner_config/
pip3 install -r requirements.txt
```

---
### 运行微调脚本
```bash
cd xtuner_config/
xtuner train internlm2_7b_chat_qlora_e3_scienctist.py --deepspeed deepspeed_zero2
```

---
### 模型转换

将得到的 PTH 模型转换为 HuggingFace 模型，生成 Adapter 文件夹

```bash
cd xtuner_config/
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1
#这里假设训练了3个epoch
xtuner convert pth_to_hf internlm2_7b_chat_qlora_e3_scienctist.py ./work_dirs/internlm2_7b_chat_qlora_e3_scienctist/epoch_3.pth ./hf
```

---

### 将 HuggingFace adapter 合并到大语言模型

```bash
xtuner convert merge ./internlm2-chat-7b ./hf ./merged --max-shard-size 2GB
# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
#     --max-shard-size 2GB
```

---

### 测试

```
cd demo/
python cli_internlm2_scientist.py
```

---

## 模型上传
完成测试后可将模型上传到ModelScope和Openxlab平台
### ModelScope
脚本：'scripts/upload_modelscope.py'
[Openxlab模型上传](https://openxlab.org.cn/docs/models/%E4%B8%8A%E4%BC%A0%E6%A8%A1%E5%9E%8B.html)

### Openxlab
[ModelScope模型上传](https://modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%88%9B%E5%BB%BA%E4%B8%8E%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

## 其他

欢迎大家给[xtuner](https://github.com/InternLM/xtuner)和[EmoLLM](https://github.com/aJupyter/EmoLLM)点点star~

🎉🎉🎉🎉🎉
