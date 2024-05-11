import copy
import os
import warnings
from dataclasses import asdict, dataclass
from typing import Callable, List, Optional

import streamlit as st
import torch
from torch import nn
from transformers.generation.utils import LogitsProcessorList, StoppingCriteriaList
from transformers.utils import logging

from transformers import AutoTokenizer, AutoModelForCausalLM  # isort: skip


# warnings.filterwarnings("ignore")
logger = logging.get_logger(__name__)


@dataclass
class GenerationConfig:
    # this config is used for chat to provide more diversity
    max_length: int = 32768
    top_p: float = 0.8
    temperature: float = 0.8
    do_sample: bool = True
    repetition_penalty: float = 1.005


@torch.inference_mode()
def generate_interactive(
    model,
    tokenizer,
    prompt,
    generation_config: Optional[GenerationConfig] = None,
    logits_processor: Optional[LogitsProcessorList] = None,
    stopping_criteria: Optional[StoppingCriteriaList] = None,
    prefix_allowed_tokens_fn: Optional[Callable[[int, torch.Tensor], List[int]]] = None,
    additional_eos_token_id: Optional[int] = None,
    **kwargs,
):
    inputs = tokenizer([prompt], padding=True, return_tensors="pt")
    input_length = len(inputs["input_ids"][0])
    for k, v in inputs.items():
        inputs[k] = v.cuda()
    input_ids = inputs["input_ids"]
    batch_size, input_ids_seq_length = input_ids.shape[0], input_ids.shape[-1]  # noqa: F841  # pylint: disable=W0612
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
    has_default_max_length = kwargs.get("max_length") is None and generation_config.max_length is not None
    if has_default_max_length and generation_config.max_new_tokens is None:
        warnings.warn(
            f"Using `max_length`'s default ({generation_config.max_length}) to control the generation length. "
            "This behaviour is deprecated and will be removed from the config in v5 of Transformers -- we"
            " recommend using `max_new_tokens` to control the maximum length of the generation.",
            UserWarning,
        )
    elif generation_config.max_new_tokens is not None:
        generation_config.max_length = generation_config.max_new_tokens + input_ids_seq_length
        if not has_default_max_length:
            logger.warn(  # pylint: disable=W4902
                f"Both `max_new_tokens` (={generation_config.max_new_tokens}) and `max_length`(="
                f"{generation_config.max_length}) seem to have been set. `max_new_tokens` will take precedence. "
                "Please refer to the documentation for more information. "
                "(https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)",
                UserWarning,
            )

    if input_ids_seq_length >= generation_config.max_length:
        input_ids_string = "input_ids"
        logger.warning(
            f"Input length of {input_ids_string} is {input_ids_seq_length}, but `max_length` is set to"
            f" {generation_config.max_length}. This can lead to unexpected behavior. You should consider"
            " increasing `max_new_tokens`."
        )

    # 2. Set generation parameters if not already defined
    logits_processor = logits_processor if logits_processor is not None else LogitsProcessorList()
    stopping_criteria = stopping_criteria if stopping_criteria is not None else StoppingCriteriaList()

    logits_processor = model._get_logits_processor(
        generation_config=generation_config,
        input_ids_seq_length=input_ids_seq_length,
        encoder_input_ids=input_ids,
        prefix_allowed_tokens_fn=prefix_allowed_tokens_fn,
        logits_processor=logits_processor,
    )

    stopping_criteria = model._get_stopping_criteria(
        generation_config=generation_config, stopping_criteria=stopping_criteria
    )
    logits_warper = model._get_logits_warper(generation_config)

    unfinished_sequences = input_ids.new(input_ids.shape[0]).fill_(1)
    scores = None
    while True:
        model_inputs = model.prepare_inputs_for_generation(input_ids, **model_kwargs)
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
        model_kwargs = model._update_model_kwargs_for_generation(outputs, model_kwargs, is_encoder_decoder=False)
        unfinished_sequences = unfinished_sequences.mul((min(next_tokens != i for i in eos_token_id)).long())

        output_token_ids = input_ids[0].cpu().tolist()
        output_token_ids = output_token_ids[input_length:]
        for each_eos_token_id in eos_token_id:
            if output_token_ids[-1] == each_eos_token_id:
                output_token_ids = output_token_ids[:-1]
        response = tokenizer.decode(output_token_ids)

        yield response
        # stop when each sentence is finished, or if we exceed the maximum length
        if unfinished_sequences.max() == 0 or stopping_criteria(input_ids, scores):
            break


def on_btn_click():
    del st.session_state.messages


@st.cache_resource
def load_model():
    
    # model_name0 = "./EmoLLM-Llama3-8B-Instruct3.0"
    # print(model_name0)

    # print('pip install modelscope websockets')
    # os.system(f'pip install modelscope websockets==11.0.3')
    # from modelscope import snapshot_download

    # #模型下载
    # model_name = snapshot_download('chg0901/EmoLLM-Llama3-8B-Instruct3.0',cache_dir=model_name0)
    # print(model_name)
    
    # model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True, torch_dtype=torch.float16).eval()
    # # model.eval()
    # tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    base_path = './EmoLLM-Llama3-8B-Instruct3.0'
    os.system(f'git clone https://code.openxlab.org.cn/chg0901/EmoLLM-Llama3-8B-Instruct3.0.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    

    model = AutoModelForCausalLM.from_pretrained(base_path, device_map="auto", trust_remote_code=True, torch_dtype=torch.float16).eval()
    # model.eval()
    tokenizer = AutoTokenizer.from_pretrained(base_path, trust_remote_code=True)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    return model, tokenizer


def prepare_generation_config():
    with st.sidebar:
        # 使用 Streamlit 的 markdown 函数添加 Markdown 文本
        st.image('assets/EmoLLM_logo_L.png', width=1, caption='EmoLLM Logo', use_column_width=True)
        st.markdown("[访问 **EmoLLM** 官方repo: **SmartFlowAI/EmoLLM**](https://github.com/SmartFlowAI/EmoLLM)")

        max_length = st.slider("Max Length", min_value=8, max_value=32768, value=32768)
        top_p = st.slider("Top P", 0.0, 1.0, 0.8, step=0.01)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.01)
        st.button("Clear Chat History", on_click=on_btn_click)

    generation_config = GenerationConfig(max_length=max_length, top_p=top_p, temperature=temperature)

    return generation_config


user_prompt = '<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|>'
robot_prompt = '<|start_header_id|>assistant<|end_header_id|>\n\n{robot}<|eot_id|>'
cur_query_prompt = '<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n'


def combine_history(prompt):
    messages = st.session_state.messages
    meta_instruction = (
        "你是心理健康助手EmoLLM, 由EmoLLM团队打造\n\n"
    )
    total_prompt =f"<|start_header_id|>system<|end_header_id|>\n\n{meta_instruction}<|eot_id|>\n\n"
    for message in messages:
        cur_content = message["content"]
        if message["role"] == "user":
            cur_prompt = user_prompt.format(user=cur_content)
        elif message["role"] == "robot":
            cur_prompt = robot_prompt.format(robot=cur_content)
        else:
            raise RuntimeError
        total_prompt += cur_prompt
    total_prompt = total_prompt + cur_query_prompt.format(user=prompt)
    return total_prompt


def main():

    # torch.cuda.empty_cache()
    print("load model begin.")
    model, tokenizer = load_model()
    print("load model end.")

    user_avator = "assets/user.png"
    robot_avator = "assets/EmoLLM.png"

    st.title("EmoLLM Llama3心理咨询室V3.0")

    generation_config = prepare_generation_config()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("我在这里，准备好倾听你的心声了。"):
        # Display user message in chat message container
        with st.chat_message("user", avatar=user_avator):
            st.markdown(prompt)
            
        real_prompt = combine_history(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_avator})

        with st.chat_message("robot", avatar=robot_avator):
            message_placeholder = st.empty()
            for cur_response in generate_interactive(
                model=model,
                tokenizer=tokenizer,
                prompt=real_prompt,
                additional_eos_token_id=128009, 
                **asdict(generation_config),
            ):
                # Display robot response in chat message container
                message_placeholder.markdown(cur_response + "▌")
            message_placeholder.markdown(cur_response)  # pylint: disable=undefined-loop-variable
        # Add robot response to chat history
        st.session_state.messages.append(
            {
                "role": "robot",
                "content": cur_response,  # pylint: disable=undefined-loop-variable
                "avatar": robot_avator,
            }
        )
        torch.cuda.empty_cache()


if __name__ == '__main__':
    main()
