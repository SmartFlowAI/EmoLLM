# Copyright (c) OpenMMLab. All rights reserved.
import torch
from datasets import load_dataset
from mmengine.dataset import DefaultSampler
from mmengine.hooks import (CheckpointHook, DistSamplerSeedHook, IterTimerHook,
                            LoggerHook, ParamSchedulerHook)
from mmengine.optim import AmpOptimWrapper, CosineAnnealingLR, LinearLR
from peft import LoraConfig
from torch.optim import AdamW
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          BitsAndBytesConfig)

from xtuner.dataset import process_hf_dataset
from xtuner.dataset.collate_fns import default_collate_fn
from xtuner.dataset.map_fns import alpaca_map_fn, template_map_fn_factory
from xtuner.engine.hooks import (DatasetInfoHook, EvaluateChatHook,
                                 VarlenAttnArgsToMessageHubHook,ThroughputHook)
from xtuner.engine.runner import TrainLoop
from xtuner.model import SupervisedFinetune
from xtuner.parallel.sequence import SequenceParallelSampler
from xtuner.utils import PROMPT_TEMPLATE, SYSTEM_TEMPLATE

#######################################################################
#                          PART 1  Settings                           #
#######################################################################
# Model
pretrained_model_name_or_path = '/root/share/new_models/meta-llama/Meta-Llama-3-8B-Instruct'
use_varlen_attn = True  # new

# Data
data_path = '../datasets/processed/combined_sc_ruozhi.jsonl'
prompt_template = PROMPT_TEMPLATE.llama3_chat
max_length = 4096
pack_to_max_length = True

# parallel
sequence_parallel_size = 1

# Scheduler & Optimizer
batch_size = 1  # per_device
max_epochs = 3

accumulative_counts = 1
accumulative_counts *= sequence_parallel_size
dataloader_num_workers = 0

optim_type = AdamW
lr = 1e-4
betas = (0.9, 0.999)
weight_decay = 0
max_norm = 1  # grad clip
warmup_ratio = 0.03

# Save
save_steps = 1000
save_total_limit = 5  # Maximum checkpoints to keep (-1 means unlimited)

# Evaluate the generation performance during the training
evaluation_freq = 500
# SYSTEM = "现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。"
# SYSTEM = "你是心理健康助手EmoLLM，由EmoLLM团队打造。你旨在通过专业心理咨询，协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术，一步步帮助来访者解决心理问题。"
# SYSTEM = "你由EmoLLM团队打造的中文领域心理健康助手, 是一个研究过无数具有心理健康问题的病人与心理健康医生对话的心理专家, 在心理方面拥有广博的知识储备和丰富的研究咨询经验，接下来你将只使用中文来回答和咨询问题。"
# evaluation_inputs = [
#     '我最近总是感到很焦虑，尤其是在学业上。我有个特别崇拜的同学，他好像在各方面都比我优秀，我总觉得自己怎么努力也追不上他，这让我压力特别大。', 
#     '我知道应该理性看待，但就是忍不住会去比较。我甚至晚上会因为这个睡不着觉，总想着怎样才能像他那样出色。',
#     '我今天心情不好，感觉不开心，很烦。'
# ]

SYSTEM = "你由EmoLLM团队打造的中文领域心理健康助手, 是一个研究过无数具有心理健康问题的病人与心理健康医生对话的心理专家, 在心理方面拥有广博的知识储备和丰富的研究咨询经验，你旨在通过专业心理咨询, 协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术, 一步步帮助来访者解决心理问题, 接下来你将只使用中文来回答和咨询问题。"
evaluation_inputs = [
    '躲在云朵下面就不怕淋雨了', # ruozhi train
    '李白如果告语文书侵权的话能赔不少钱吧', # ruozhi test
    '雨天，我走进水坑里，不小心踩碎了天空。', # ruozhi test
    '请介绍你自己', # self cognition
    '你好',
    '我今天心情不好，感觉不开心，很烦。',
    '我最近总是感到很焦虑，尤其是在学业上。我有个特别崇拜的同学，他好像在各方面都比我优秀，我总觉得自己怎么努力也追不上他，这让我压力特别大。', 
]

# "这是一句富有想象力和幽默感的表达。在现实生活中，躲在云朵下面并不能避免淋雨，因为云朵实际上是由水蒸气凝结形成的，而雨就是由这些水滴凝结而成的。\n\n这样的表达可能是在夸张和幽默的语境中，通过一种天马行空的方式来表达逃避现实或者寻找避难的愿望。在文学或口语表达中，常常会运用夸张和幽默来传达情感或者引起共鸣。",

# "如果李白（701年2月28日—762年12月）真的能就侵权诉讼获得赔偿，那确实可能是一笔不小的金额。然而，这种想法主要是一种有趣的假设，因为现实中有几个关键因素使这种情况不可能发生：\n\n1. **时间差异**：李白生活在唐朝，距今大约1200多年前。那 个时代的法律体系与现代的知识产权法律截然不同，当时没有现代意义上的版权法。\n\n2. **版权法的适用范围**：即使在现代，版权 法也有一定的时效限制。在大多数国家，版权保护通常在作者去世后一定年数内有效（如我国是作者去世后50年）。李白去世已超过1250年，因此其作品已经进入公共领域，任何人都可以自由使用而无需支付版权费用。\n\n3. **历史与现实的区别**：历史人物无法在现代 法律体系中提起诉讼，因为他们不再是活跃的法律主体。\n\n所以，虽然这是一个有趣的想法，但在现实中，李白或其他古代作者无法因其作品被现代出版物使用而获得赔偿。",

# "这个描述似乎是一个修辞手法，比喻性地描述了雨天的场景。在这个描述中，说“我走进水坑里，不小心踩碎了天空”，实际上并非字面意义上的发生，而是一种用词语来比喻雨天的场景。\n\n通常情况下，当雨水落在水坑或者蓄水池时，水面会泛起涟漪或者波纹，可能会反射天空的颜色或者天空的倒影。因此，这句话可能是通过“踩碎了天空”的说法来比喻雨天时踩进水坑的情景，描述雨水落在水坑中形成的波纹或者涟漪，产生了一种倒映天空的效果。\n\n这种形象化的表达方式可能是为了更生动地描述一个平常的场景，赋予它一些诗意或者意境。",


#######################################################################
#                      PART 2  Model & Tokenizer                      #
#######################################################################
tokenizer = dict(
    type=AutoTokenizer.from_pretrained,
    pretrained_model_name_or_path=pretrained_model_name_or_path,
    trust_remote_code=True,
    padding_side='right')

model = dict(
    type=SupervisedFinetune,
    use_varlen_attn=use_varlen_attn,
    llm=dict(
        type=AutoModelForCausalLM.from_pretrained,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        quantization_config=dict(
            type=BitsAndBytesConfig,
            load_in_4bit=True,
            load_in_8bit=False,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4')),
    lora=dict(
        type=LoraConfig,
        r=32,
        lora_alpha=64,
        lora_dropout=0.1,
        bias='none',
        task_type='CAUSAL_LM'))

#######################################################################
#                      PART 3  Dataset & Dataloader                   #
#######################################################################
alpaca_en = dict(
    type=process_hf_dataset,
    dataset=dict(type=load_dataset, path='json', data_files=dict(train=data_path)),
    tokenizer=tokenizer,
    max_length=max_length,
    dataset_map_fn=None,
    template_map_fn=dict(
        type=template_map_fn_factory, template=prompt_template),
    remove_unused_columns=True,
    shuffle_before_pack=True,
    pack_to_max_length=pack_to_max_length,
    use_varlen_attn=use_varlen_attn)

sampler = SequenceParallelSampler \
    if sequence_parallel_size > 1 else DefaultSampler
train_dataloader = dict(
    batch_size=batch_size,
    num_workers=dataloader_num_workers,
    dataset=alpaca_en,
    sampler=dict(type=DefaultSampler, shuffle=True),
    collate_fn=dict(type=default_collate_fn, 
                    use_varlen_attn=use_varlen_attn))

#######################################################################
#                    PART 4  Scheduler & Optimizer                    #
#######################################################################
# optimizer
optim_wrapper = dict(
    type=AmpOptimWrapper,
    optimizer=dict(
        type=optim_type, lr=lr, betas=betas, weight_decay=weight_decay),
    clip_grad=dict(max_norm=max_norm, error_if_nonfinite=False),
    accumulative_counts=accumulative_counts,
    loss_scale='dynamic',
    dtype='float32')

# learning policy
# More information: https://github.com/open-mmlab/mmengine/blob/main/docs/en/tutorials/param_scheduler.md  # noqa: E501
param_scheduler = [
    dict(
        type=LinearLR,
        start_factor=1e-5,
        by_epoch=True,
        begin=0,
        end=warmup_ratio * max_epochs,
        convert_to_iter_based=True),
    dict(
        type=CosineAnnealingLR,
        eta_min=0.0,
        by_epoch=True,
        begin=warmup_ratio * max_epochs,
        end=max_epochs,   # T_max=max_epochs,
        convert_to_iter_based=True)
]

# train, val, test setting
train_cfg = dict(type=TrainLoop, max_epochs=max_epochs)
# train_cfg = dict(by_epoch=True, max_epochs=max_epochs, val_interval=1)

#######################################################################
#                           PART 5  Runtime                           #
#######################################################################
# Log the dialogue periodically during the training process, optional
custom_hooks = [
    dict(type=DatasetInfoHook, tokenizer=tokenizer),
    dict(
        type=EvaluateChatHook,
        tokenizer=tokenizer,
        every_n_iters=evaluation_freq,
        evaluation_inputs=evaluation_inputs,
        system=SYSTEM,
        prompt_template=prompt_template),
    dict(type=ThroughputHook)
]

if use_varlen_attn:
    custom_hooks += [dict(type=VarlenAttnArgsToMessageHubHook)]

# configure default hooks
default_hooks = dict(
    # record the time of every iteration.
    timer=dict(type=IterTimerHook),
    # print log every 10 iterations.
    logger=dict(type=LoggerHook, interval=10, 
                log_metric_by_epoch=False),
    # enable the parameter scheduler.
    param_scheduler=dict(type=ParamSchedulerHook),
    # save checkpoint per `save_steps`.
    checkpoint=dict(
        type=CheckpointHook,
        by_epoch=False,
        interval=save_steps,
        # interval=1,
        max_keep_ckpts=save_total_limit),
    # set sampler seed in distributed evrionment.
    sampler_seed=dict(type=DistSamplerSeedHook),
)

# configure environment
env_cfg = dict(
    # whether to enable cudnn benchmark
    cudnn_benchmark=False,
    # set multi process parameters
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    # set distributed parameters
    dist_cfg=dict(backend='nccl'),
)

# set visualizer
visualizer = None

# set log level
log_level = 'INFO'

# load from which checkpoint
load_from = None

# whether to resume training from the loaded checkpoint
resume = False

# Defaults to use random seed and disable `deterministic`
randomness = dict(seed=None, deterministic=False)

# set log processor
log_processor = dict(by_epoch=False)
