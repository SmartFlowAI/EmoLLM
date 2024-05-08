# 增量预训练教程

# 增量预训练简介
增量预训练旨在提升模型在特定领域或任务的能力。


# 预训练流程
- Step1 处理数据
- Step2 配置config（全量、Lora、Qlora）
- Step3 启动训练（单卡、多卡、是否使用deepspeed）
- Step4 模型合成
- Step5 模型测试
- Step6 模型上传

# EmoLLM增量预训练教程
基于微调中的数据集[datasets](../../datasets)修改而来

- Step1 修改`ft2pt.py`中的文件路径
这里以[output2.json](../../datasets/processed/output2.json)为例，运行脚本生成[pt.json](../../datasets/pt/pt.json)

- Step2 [config](./internlm2_chat_1_8b_qlora_e3_pt.py)
注意：本config采用了**变长注意力 (Variable Length Attention)**
需要安装flash_attn
`MAX_JOBS=4 pip install flash-attn --no-build-isolation`


- Step3 训练：
```
# On a single GPU
xtuner train internlm2_chat_1_8b_qlora_e3_pt.py --deepspeed deepspeed_zero2
# On multiple GPUs
(DIST) NPROC_PER_NODE=${GPU_NUM} xtuner train internlm2_chat_1_8b_qlora_e3_pt.py --deepspeed deepspeed_zero2
(SLURM) srun ${SRUN_ARGS} xtuner train internlm2_chat_1_8b_qlora_e3_pt.py --launcher slurm --deepspeed deepspeed_zero2
```

- 其余流程请参考[微调教程](../../xtuner_config/README.md)