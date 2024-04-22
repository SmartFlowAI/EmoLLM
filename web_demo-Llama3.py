
# isort: skip_file
import copy
import os
import warnings
from dataclasses import asdict, dataclass
from typing import Callable, List, Optional

import streamlit as st
import torch
from torch import nn
from transformers.generation.utils import (LogitsProcessorList,
                                           StoppingCriteriaList)
from transformers.utils import logging

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig  # isort: skip
from peft import PeftModel


warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)
logger = logging.get_logger(__name__)

if not os.path.isdir("model"):
    print("[ERROR] not find model dir")
    exit(0)

# online = True

## running on local to test online function
# if online:
#     from openxlab.model import download
#     download(model_repo='chg0901/EmoLLM-Llama3-8B-Instruct2.0', 
#             output='model')

@dataclass
class GenerationConfig:
    # this config is used for chat to provide more diversity
    max_length: int = 500
    top_p: float = 0.9
    temperature: float = 0.6
    do_sample: bool = True
    repetition_penalty: float = 1.1


@torch.inference_mode()
def generate_interactive(
    model,
    tokenizer,
    prompt,
    generation_config: Optional[GenerationConfig] = None,
    logits_processor: Optional[LogitsProcessorList] = None,
    stopping_criteria: Optional[StoppingCriteriaList] = None,
    prefix_allowed_tokens_fn: Optional[Callable[[int, torch.Tensor],
                                                List[int]]] = None,
    additional_eos_token_id: Optional[int] = None,
    **kwargs,
):
    inputs = tokenizer([prompt], return_tensors='pt')
    input_length = len(inputs['input_ids'][0])
    for k, v in inputs.items():
        inputs[k] = v.cuda()
    input_ids = inputs['input_ids']
    _, input_ids_seq_length = input_ids.shape[0], input_ids.shape[-1]
    if generation_config is None:
        generation_config = model.generation_config
    generation_config = copy.deepcopy(generation_config)
    model_kwargs = generation_config.update(**kwargs)
    bos_token_id, eos_token_id = (  # noqa: F841  # pylint: disable=W0612
        generation_config.bos_token_id,
        generation_config.eos_token_id,
    )
    if isinstance(eos_token_id, int):
        eos_token_id = [eos_token_id]
    if additional_eos_token_id is not None:
        eos_token_id.append(additional_eos_token_id)
    has_default_max_length = kwargs.get(
        'max_length') is None and generation_config.max_length is not None
    if has_default_max_length and generation_config.max_new_tokens is None:
        warnings.warn(
            f"Using 'max_length''s default ({repr(generation_config.max_length)}) \
                to control the generation length. "
            'This behaviour is deprecated and will be removed from the \
                config in v5 of Transformers -- we'
            ' recommend using `max_new_tokens` to control the maximum \
                length of the generation.',
            UserWarning,
        )
    elif generation_config.max_new_tokens is not None:
        generation_config.max_length = generation_config.max_new_tokens + \
            input_ids_seq_length
        if not has_default_max_length:
            logger.warn(  # pylint: disable=W4902
                f"Both 'max_new_tokens' (={generation_config.max_new_tokens}) "
                f"and 'max_length'(={generation_config.max_length}) seem to "
                "have been set. 'max_new_tokens' will take precedence. "
                'Please refer to the documentation for more information. '
                '(https://huggingface.co/docs/transformers/main/'
                'en/main_classes/text_generation)',
                UserWarning,
            )

    if input_ids_seq_length >= generation_config.max_length:
        input_ids_string = 'input_ids'
        logger.warning(
            f"Input length of {input_ids_string} is {input_ids_seq_length}, "
            f"but 'max_length' is set to {generation_config.max_length}. "
            'This can lead to unexpected behavior. You should consider'
            " increasing 'max_new_tokens'.")

    # 2. Set generation parameters if not already defined
    logits_processor = logits_processor if logits_processor is not None \
        else LogitsProcessorList()
    stopping_criteria = stopping_criteria if stopping_criteria is not None \
        else StoppingCriteriaList()

    logits_processor = model._get_logits_processor(
        generation_config=generation_config,
        input_ids_seq_length=input_ids_seq_length,
        encoder_input_ids=input_ids,
        prefix_allowed_tokens_fn=prefix_allowed_tokens_fn,
        logits_processor=logits_processor,
    )

    stopping_criteria = model._get_stopping_criteria(
        generation_config=generation_config,
        stopping_criteria=stopping_criteria)
    logits_warper = model._get_logits_warper(generation_config)

    unfinished_sequences = input_ids.new(input_ids.shape[0]).fill_(1)
    scores = None
    while True:
        model_inputs = model.prepare_inputs_for_generation(
            input_ids, **model_kwargs)
        # forward pass to get next token
        outputs = model(
            **model_inputs,
            return_dict=True,
            output_attentions=False,
            output_hidden_states=False,
        )

        next_token_logits = outputs.logits[:, -1, :]

        # pre-process distribution
        next_token_scores = logits_processor(input_ids, next_token_logits)
        next_token_scores = logits_warper(input_ids, next_token_scores)

        # sample
        probs = nn.functional.softmax(next_token_scores, dim=-1)
        if generation_config.do_sample:
            next_tokens = torch.multinomial(probs, num_samples=1).squeeze(1)
        else:
            next_tokens = torch.argmax(probs, dim=-1)

        # update generated ids, model inputs, and length for next step
        input_ids = torch.cat([input_ids, next_tokens[:, None]], dim=-1)
        model_kwargs = model._update_model_kwargs_for_generation(
            outputs, model_kwargs, is_encoder_decoder=False)
        unfinished_sequences = unfinished_sequences.mul(
            (min(next_tokens != i for i in eos_token_id)).long())

        output_token_ids = input_ids[0].cpu().tolist()
        output_token_ids = output_token_ids[input_length:]
        for each_eos_token_id in eos_token_id:
            if output_token_ids[-1] == each_eos_token_id:
                output_token_ids = output_token_ids[:-1]
        response = tokenizer.decode(output_token_ids)

        yield response
        # stop when each sentence is finished
        # or if we exceed the maximum length
        if unfinished_sequences.max() == 0 or stopping_criteria(
                input_ids, scores):
            break


def on_btn_click():
    del st.session_state.messages


# @st.cache_resource
# def load_model(arg1):
#     # model = AutoModelForCausalLM.from_pretrained(args.m).cuda()
#     # tokenizer = AutoTokenizer.from_pretrained(args.m, trust_remote_code=True)
#     model = AutoModelForCausalLM.from_pretrained(arg1, torch_dtype=torch.float16).cuda()
#     tokenizer = AutoTokenizer.from_pretrained(arg1, trust_remote_code=True)

  
#     return model, tokenizer

@st.cache_resource
def load_model():
    model = AutoModelForCausalLM.from_pretrained("model", 
                                                 device_map="auto", 
                                                 trust_remote_code=True, 
                                                 torch_dtype=torch.float16)
    model = model.eval()
    tokenizer = AutoTokenizer.from_pretrained("model", trust_remote_code=True)
    return model, tokenizer


@st.cache_resource
def load_model0(model_name_or_path, load_in_4bit=False, adapter_name_or_path=None):
    if load_in_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
        )
    else:
        quantization_config = None

    # 加载base model
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        # load_in_4bit=load_in_4bit, 
        # # ValueError: You can't pass `load_in_4bit`or `load_in_8bit` as a kwarg when passing `quantization_config` argument at the same time.
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16,
        device_map='auto',
        quantization_config=quantization_config
    )

    # 加载adapter
    if adapter_name_or_path is not None:
        model = PeftModel.from_pretrained(model, adapter_name_or_path)
        
    ## 加载tokenzier
    tokenizer = AutoTokenizer.from_pretrained(
        model_name_or_path if adapter_name_or_path is None else adapter_name_or_path,
        trust_remote_code=True,
        use_fast=False
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def prepare_generation_config():
    with st.sidebar:
        
        # 使用 Streamlit 的 markdown 函数添加 Markdown 文本
        st.image('assets/EmoLLM_logo_L.png', width=1, caption='EmoLLM Logo', use_column_width=True)
        st.markdown("[访问 **EmoLLM** 官方repo: **SmartFlowAI/EmoLLM**](https://github.com/SmartFlowAI/EmoLLM)")
        
        max_length = st.slider('Max Length',
                               min_value=8,
                               max_value=8192,
                               value=500)
        top_p = st.slider('Top P', 0.0, 1.0, 0.9, step=0.01)
        temperature = st.slider('Temperature', 0.0, 1.0, 0.6, step=0.01)
        repetition_penalty = st.slider('Repetition penalty', 0.0, 1.5, 1.1, step=0.01)
        st.button('Clear Chat History', on_click=on_btn_click)

    generation_config = GenerationConfig(max_length=max_length,
                                         top_p=top_p,
                                         temperature=temperature,
                                         repetition_penalty=repetition_penalty,
                                         do_sample=True)

    return generation_config


user_prompt = '<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|>'
robot_prompt = '<|start_header_id|>assistant<|end_header_id|>\n\n{robot}<|eot_id|>'
cur_query_prompt = '<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n'


def combine_history(prompt):
    messages = st.session_state.messages
    
    meta_instruction = (
        "你是心理健康助手EmoLLM, 由EmoLLM团队打造, 是一个研究过无数具有心理健康问题的病人与心理健康医生对话的心理专家, 在心理方面拥有广博的知识储备和丰富的研究咨询经验。你旨在通过专业心理咨询, 协助来访者完成心理诊断。请充分利用专业心理学知识与咨询技术, 一步步帮助来访者解决心理问题。。"
    )
    total_prompt = f"<|start_header_id|>system<|end_header_id|>\n{meta_instruction}<|eot_id|>\n"
    
    for message in messages:
        cur_content = message['content']
        if message['role'] == 'user':
            cur_prompt = user_prompt.format(user=cur_content)
        elif message['role'] == 'robot':
            cur_prompt = robot_prompt.format(robot=cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.format(user=prompt)
    return total_prompt


def main():
    
    st.markdown("我在这里，准备好倾听你的心声了。", unsafe_allow_html=True)
    model_name_or_path = 'model'
    adapter_name_or_path = None
    # if online:
    #     model_name_or_path = 'model'
    #     adapter_name_or_path = None
    # else:
    #     # model_name_or_path = "./xtuner_config/merged_Llama3_8b_instruct_e3"
    #     # adapter_name_or_path = './xtuner_config/hf_llama3_e1_sc2'
    
    #     model_name_or_path = "./xtuner_config/merged_Llama3_8b_instruct_e1_sc"
    #     adapter_name_or_path = None

    # 若开启4bit推理能够节省很多显存，但效果可能下降
    load_in_4bit = False # True  # 6291MiB
    
    # torch.cuda.empty_cache()
    print('load model begin.')
    # 加载模型
    print(f'Loading model from: {model_name_or_path}')
    print(f'adapter_name_or_path: {adapter_name_or_path}')
    # model, tokenizer = load_model(arg1)
    
    model, tokenizer = load_model()
    
    # model, tokenizer = load_model(
    #     # arg1 if arg1 is not None else model_name_or_path,
    #     model_name_or_path,
    #     load_in_4bit=load_in_4bit,
    #     adapter_name_or_path=adapter_name_or_path
    #     )
    model.eval()
    print('load model end.')
    
    user_avator = "assets/user.png"
    robot_avator = "assets/EmoLLM.png"

    st.title('EmoLLM Llama3心理咨询室V2.0')

    generation_config = prepare_generation_config()

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar=message.get("avatar")):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('你好，欢迎来到Llama3 EmoLLM 心理咨询室'):
        # Display user message in chat message container
        with st.chat_message('user', avatar=user_avator):
            st.markdown(prompt)
        real_prompt = combine_history(prompt)
        # Add user message to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
            'avatar': user_avator
        })


        with st.chat_message('robot', avatar=robot_avator):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=real_prompt,
                    additional_eos_token_id=128009,  # <|eot_id|>
                    eos_token_id=128009, 
                    pad_token_id=128009,
                    **asdict(generation_config),
            ):
                # Display robot response in chat message container
                message_placeholder.markdown(cur_response + '▌')
            message_placeholder.markdown(cur_response)
        # Add robot response to chat history
        st.session_state.messages.append({
            'role': 'robot',
            'content': cur_response,  # pylint: disable=undefined-loop-variable
            "avatar": robot_avator,
        })
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
