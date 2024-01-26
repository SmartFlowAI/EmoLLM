# 微调指南

- 本项目不仅在心理健康数据集上进行了微调，同时也对模型进行了自我认知微调，下面是微调的详细指南。

## 一、基于xtuner的微调🎉🎉🎉🎉🎉

### 环境准备

```markdown
datasets==2.16.1
deepspeed==0.13.1
einops==0.7.0
flash_attn==2.5.0
mmengine==0.10.2
openxlab==0.0.34
peft==0.7.1
sentencepiece==0.1.99
torch==2.1.2
transformers==4.36.2
xtuner==0.1.11
```

也可以一键安装

```bash
cd xtuner_config/
pip3 install -r requirements.txt
```

---

### 微调

```bash
cd xtuner_config/
xtuner train internlm2_7b_chat_qlora_e3.py --deepspeed deepspeed_zero2
```

---

### 将得到的 PTH 模型转换为 HuggingFace 模型

**即：生成 Adapter 文件夹**

```bash
cd xtuner_config/
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1

xtuner convert pth_to_hf internlm2_7b_chat_qlora_e3.py ./work_dirs/internlm_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth ./hf
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
python cli_internlm2.py
```

---

## 二、基于Transformers的微调🎉🎉🎉🎉🎉

- 请查看[ChatGLM3-6b lora微调指南](ChatGLM3-6b-ft.md)

---

## 其他

欢迎大家给[xtuner](https://github.com/InternLM/xtuner)和[EmoLLM](https://github.com/aJupyter/EmoLLM)点点star~

🎉🎉🎉🎉🎉
