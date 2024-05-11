import gradio as gr
import os
import torch
from transformers import GemmaTokenizer, AutoModelForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread


DESCRIPTION = '''
<div>
<h1 style="text-align: center;">EmoLLM Llama3 心理咨询室 V4.0</h1>

<p align="center">
  <a href="https://github.com/SmartFlowAI/EmoLLM/">
    <img src="https://st-app-center-006861-9746-jlroxvg.openxlab.space/media/cda6c1a05dc8ba5b19ad3e7a24920fdf3750c917751202385a6dbc51.png" alt="Logo" width="20%">
  </a>
</p>

<div align="center">

<!-- PROJECT SHIELDS -->
[![OpenXLab_Model][OpenXLab_Model-image]][OpenXLab_Model-url] 

<h2 style="text-align: center;"> EmoLLM是一系列能够支持 理解用户-支持用户-帮助用户 心理健康辅导链路的 心理健康大模型 ，欢迎大家star~⭐⭐</h2>
<p>https://github.com/SmartFlowAI/EmoLLM</p>
</div>

</div>

[OpenXLab_Model-image]: https://cdn-static.openxlab.org.cn/header/openxlab_models.svg
[OpenXLab_Model-url]: https://openxlab.org.cn/models/detail/chg0901/EmoLLM-Llama3-8B-Instruct3.0

'''

LICENSE = """
<p align="center"> Built with Meta Llama 3 </>
"""

PLACEHOLDER = """
<div style="padding: 30px; text-align: center; display: flex; flex-direction: column; align-items: center;">

</div>
"""


css = """
h1 {
  text-align: center;
  display: block;
}
<!--
#duplicate-button {
  margin: auto;
  color: white;
  background: #1565c0;
  border-radius: 100vh;
}
-->
"""

# download internlm2 to the base_path directory using git tool
base_path = './EmoLLM-Llama3-8B-Instruct3.0'
os.system(f'git clone https://code.openxlab.org.cn/chg0901/EmoLLM-Llama3-8B-Instruct3.0.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')


# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(base_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(base_path,trust_remote_code=True, device_map="auto", torch_dtype=torch.float16).eval()  # to("cuda:0") 
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

def chat_llama3_8b(message: str, 
              history: list, 
              temperature: float, 
              max_new_tokens: int,
              top_p: float
             ) -> str:
    """
    Generate a streaming response using the llama3-8b model.
    Args:
        message (str): The input message.
        history (list): The conversation history used by ChatInterface.
        temperature (float): The temperature for generating the response.
        max_new_tokens (int): The maximum number of new tokens to generate.
    Returns:
        str: The generated response.
    """
    conversation = []
    
    for user, assistant in history:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    conversation.append({"role": "user", "content": message})

    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt").to(model.device)
    
    streamer = TextIteratorStreamer(tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)

    generate_kwargs = dict(
        input_ids= input_ids,
        streamer=streamer,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p = top_p,
        eos_token_id=terminators,
    )
    # This will enforce greedy generation (do_sample=False) when the temperature is passed 0, avoiding the crash.             
    if temperature == 0:
        generate_kwargs['do_sample'] = False
        
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    outputs = []
    for text in streamer:
        outputs.append(text)
        yield "".join(outputs)

        

# Gradio block
chatbot=gr.Chatbot(height=450, placeholder=PLACEHOLDER, label='EmoLLM Chat')

with gr.Blocks(fill_height=True, css=css) as demo:
    
    gr.Markdown(DESCRIPTION)
    # gr.DuplicateButton(value="Duplicate Space for private use", elem_id="duplicate-button")
    gr.ChatInterface(
        fn=chat_llama3_8b,
        chatbot=chatbot,
        fill_height=True,
        additional_inputs_accordion=gr.Accordion(label="⚙️ Parameters", open=False, render=False),
        additional_inputs=[
            gr.Slider(minimum=0,
                      maximum=1, 
                      step=0.1,
                      value=0.95, 
                      label="Temperature", 
                      render=False),
            gr.Slider(minimum=128, 
                      maximum=4096,
                      step=1,
                      value=4096, 
                      label="Max new tokens", 
                      render=False ),
            gr.Slider(minimum=0.0, 
                      maximum=1,
                      step=0.01,
                      value=0.8, 
                      label="Top P", 
                      render=False ),
            # gr.Slider(minimum=128, 
            #           maximum=4096,
            #           step=1,
            #           value=512, 
            #           label="Max new tokens", 
            #           render=False ),
            ],
        examples=[
            ['请介绍你自己。'],
            ['我觉得我在学校的学习压力好大啊，虽然我真的很喜欢我的专业，但最近总是担心自己无法达到自己的期望，这让我有点焦虑。'],
            ['我最近总觉得自己在感情上陷入了困境，我喜欢上了我的朋友，但又害怕表达出来会破坏我们现在的关系...'],
            ['我感觉自己像是被困在一个无尽的循环中。每天醒来都感到身体沉重，对日常活动提不起兴趣，工作、锻炼甚至是我曾经喜欢的事物都让我觉得厌倦'],
            ['最近工作压力特别大，还有一些家庭矛盾']
            ],
        cache_examples=False,
                     )
    
    gr.Markdown(LICENSE)
    
if __name__ == "__main__":
    demo.launch()
    
    