# Fine-Tuning Guide

- This project has undergone fine-tuning not only on mental health datasets but also on self-awareness, and here is the detailed guide for fine-tuning.

## I. Fine-Tuning Based on Xtuner 🎉🎉🎉🎉🎉

### Environment Setup

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

You can also install them all at once by

```bash
cd xtuner_config/
pip3 install -r requirements.txt
```

---

### Fine-Tuning

```bash
cd xtuner_config/
xtuner train internlm2_7b_chat_qlora_e3.py --deepspeed deepspeed_zero2
```

---

### Convert the Obtained PTH Model to a HuggingFace Model

**That is: Generate the Adapter folder**

```bash
cd xtuner_config/
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1

xtuner convert pth_to_hf internlm2_7b_chat_qlora_e3.py ./work_dirs/internlm_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth ./hf
```

---

### Merge the HuggingFace Adapter with the Large Language Model

```bash
xtuner convert merge ./internlm2-chat-7b ./hf ./merged --max-shard-size 2GB
# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
#     --max-shard-size 2GB
```

---

### Testing

```
cd demo/
python cli_internlm2.py
```

---

## II. Fine-Tuning Based on Transformers🎉🎉🎉🎉🎉

- Please refer to the [ChatGLM3-6b lora fine-tuning guide](ChatGLM3-6b-ft.md).

---

## Other

Feel free to give [xtuner](https://github.com/InternLM/xtuner) and [EmoLLM](https://github.com/aJupyter/EmoLLM) a star~

🎉🎉🎉🎉🎉
