import os
print("downloading libs")
os.system(f"pip install faiss_gpu-1.7.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl")
os.system(f"pip install -r requirements.txt")
print("libs downloaded")
import time
import gradio as gr
import re
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, BitsAndBytesConfig
from threading import Thread
from web_search import new_conversation_id, search_web
from rag.src.pipeline import EmoLLMRAG

print("downloading model")
base_path = "model"
os.system(f"modelscope download --model haiyangpengai/careyou_7b_16bit_v3_2_qwen14_4bit --local_dir {base_path}")
os.system(f"modelscope download --model haiyangpengai/careyou_tts --local_dir ./pretrained_models/")
os.system("mv pretrained_models/heart_girl models/")
print("model downloaded")

print("loading model")

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(base_path, quantization_config=nf4_config, torch_dtype=torch.bfloat16, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(base_path, trust_remote_code=True)
tokenizer.use_default_system_prompt = False
rag_obj = EmoLLMRAG(model)
print("model loaded")

prompt_style = """
### Instruction:
你是Care，一个心理咨询AI助手，基于deepseek-r1微调模型，能够用专业的心理知识回答来访者的问题。每次回答问题前，需要结合联网搜索结果：{}以及本地知识库内容：{}进行思考，并将思考过程放在<think>和</think>之间，如果联网搜索结果和本地知识库内容均为空，则自己思考，然后再根据思考进行回答，回答放在</think>之后。请用与朋友聊天的方式来解决来访者的问题，多倾听他们的心声，多互动，不要只给答案。

### Question:
{}

### Response:
<think>
"""

def tavily_search(query, max_results=5):
    search_info = "\n搜索结果：\n"
    search_result = []
    try:
        search_results = client.search(query, search_depth="advanced")
        search_result = [{
            "index": idx + 1,
            "url": result.get("url", ""),
            "title": result.get("title", "")
        } for idx, result in enumerate(search_results.get("results", []))]
        
        for idx, result in enumerate(search_result):
            search_info += f"{idx + 1}. 标题：{result.get('title', '')}\n   链接：{result.get('url', '')}\n"
    except Exception as e:
        print(f"Tavily搜索出错: {str(e)}")
        search_info = ""
    return search_info

def format_time(seconds_float):
    total_seconds = int(round(seconds_float))
    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

DESCRIPTION = '''
# 🧠 An AI assistant with extensive knowledge in psychology, and my name is Care.

## 🚀 Overview
This model is finetuned on deepseek-r1. If this repo helps you, star and share it ❤️. This repo will be continuously merged into EmoLLM.

## ✨ Functions
✅Provide an interactive chat interface for psychological consultation seekers.

✅Integrate knowledge retrieval 

✅Integrate web searching

✅two customized tts (ISSUE: more voice models)

❌Virtual mental companion 

## ⚠️ issue status
- 2025.4.29 fix bug of clearing and stopping op.
- 2025.5.3 web search supports.
- 2025.5.5 rag supports. (demo code, needs to be checked)
- 2025.5.7 fix bug of rag.
- 2025.5.9 tts supports.
- 2025.5.10 two voice models.
- 2025.5.16 merge into EmoLLM.

## 🙏 Acknowledgments
We are grateful to Modelscope for supporting this project with resources.

The rag codes are based on [EmoLLM](https://github.com/SmartFlowAI/EmoLLM)

## 🤝 Contributing
Feel free to contribute to this project via our [github repo](https://github.com/HaiyangPeng/careyou). Grow together!
'''

CSS = """
.spinner {
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 8px;
}
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.thinking-summary {
    cursor: pointer;
    padding: 8px;
    background: #f5f5f5;
    border-radius: 4px;
    margin: 4px 0;
}
.thought-content {
    padding: 10px;
    background: #f8f9fa;
    border-radius: 4px;
    margin: 5px 0;
}
.thinking-container {
    border-left: 3px solid #facc15;
    padding-left: 10px;
    margin: 8px 0;
    background: #ffffff;
}
details:not([open]) .thinking-container {
    border-left-color: #290c15;
}
details {
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    padding: 12px !important;
    margin: 8px 0 !important;
    transition: border-color 0.2s;
}
"""

def stop_generation(active_gen):
    active_gen[0] = False
    return active_gen


def user(message, history):
    return "", history + [[message, None]]

class ParserState:
    __slots__ = ['answer', 'thought', 'in_think', 'start_time', 'last_pos', 'total_think_time']
    def __init__(self):
        self.answer = ""
        self.thought = ""
        self.in_think = False
        self.start_time = 0
        self.last_pos = 0
        self.total_think_time = 0.0

def parse_response(text, state):
    buffer = text[state.last_pos:]
    state.last_pos = len(text)
    
    while buffer:
        if not state.in_think:
            think_start = buffer.find('<think>')
            if think_start != -1:
                state.answer += buffer[:think_start]
                state.in_think = True
                state.start_time = time.perf_counter()
                buffer = buffer[think_start + 7:]
            else:
                state.answer += buffer
                break
        else:
            think_end = buffer.find('</think>')
            if think_end != -1:
                state.thought += buffer[:think_end]
                # Calculate duration and accumulate
                duration = time.perf_counter() - state.start_time
                state.total_think_time += duration
                state.in_think = False
                buffer = buffer[think_end + 8:]
            else:
                state.thought += buffer
                break
    
    elapsed = time.perf_counter() - state.start_time if state.in_think else 0
    return state, elapsed

def format_response(state, elapsed):
    answer_part = state.answer.replace('<think>', '').replace('</think>', '')
    collapsible = []
    collapsed = "<details open>"

    if state.thought or state.in_think:
        if state.in_think:
            # Ongoing think: total time = accumulated + current elapsed
            total_elapsed = state.total_think_time + elapsed
            formatted_time = format_time(total_elapsed)
            status = f"❤️ Care的思考过程 {formatted_time}"
        else:
            # Finished: show total accumulated time
            formatted_time = format_time(state.total_think_time)
            status = f"🐷 Care的回答 {formatted_time}"
            collapsed = "<details>"
        collapsible.append(
            f"{collapsed}<summary>{status}</summary>\n\n<div class='thinking-container'>\n{state.thought}\n</div>\n</details>"
        )

    return collapsible, answer_part

def generate_response(history, temperature, top_p, max_tokens, active_gen, conversation_id, search_enabled):
    user_message = history[-1][0]
    search_results = search_web(user_message, conversation_id, enabled=search_enabled,
                                cancelled=lambda: not active_gen[0])
    if not active_gen[0]:
        return
    if search_results:
        print("联网搜索结果：", search_results)
    else:
        print("未搜索到准确信息，将按照原始流程进行推理")

    conversation = []
    for user, assistant in history[:-1]:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    conversation.append({"role": "user", "content": prompt_style.format(search_results, "", user_message)})

    input_ids = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
    input_ids = tokenizer([input_ids], return_tensors="pt").to(model.device)

    streamer = TextIteratorStreamer(tokenizer, timeout=20.0, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        input_ids=input_ids.input_ids,
        streamer=streamer,
        do_sample=True,
        max_new_tokens=max_tokens,
    )

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    full_response = "<think>"
    state = ParserState()
    last_update = 0

    try:
        for chunk in streamer:
            if not active_gen[0]:
                break
            print(chunk, end="", flush=True)
            if chunk:
                full_response += chunk
                state, elapsed = parse_response(full_response, state)

                collapsible, answer_part = format_response(state, elapsed)
                history[-1][1] = "\n\n".join(collapsible + [answer_part])
                yield history

        state, elapsed = parse_response(full_response, state)
        collapsible, answer_part = format_response(state, elapsed)
        history[-1][1] = "\n\n".join(collapsible + [answer_part])
        yield history

    except Exception as e:
        history[-1][1] = f"Error: {str(e)}"
        yield history
    finally:
        active_gen[0] = False
        t.join()

def generate_response_and_tts(history, temperature, top_p, max_tokens, active_gen, 
                              audio_select, ref_text, prompt_language, text_language, how_to_cut,
                              conversation_id, search_enabled):
    user_message = history[-1][0]
    search_results = search_web(user_message, conversation_id, enabled=search_enabled,
                                cancelled=lambda: not active_gen[0])
    if not active_gen[0]:
        return
    if search_results:
        print("联网搜索结果：", search_results)
    else:
        print("未搜索到准确信息，将按照原始流程进行推理")

    conversation = []
    for user, assistant in history[:-1]:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])

    retrieval_content = rag_obj.get_retrieval_content(user_message)
    retrieval_content = " ".join(retrieval_content)
    if retrieval_content:
        print("知识库搜索结果：", retrieval_content)
    else:
        print("未搜索到准确信息，将按照原始流程进行推理")

    conversation.append({"role": "user", "content": prompt_style.format(search_results, retrieval_content, user_message)})

    input_ids = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
    input_ids = tokenizer([input_ids], return_tensors="pt").to(model.device)

    streamer = TextIteratorStreamer(tokenizer, timeout=20.0, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        input_ids=input_ids.input_ids,
        streamer=streamer,
        do_sample=True,
        max_new_tokens=max_tokens,
    )

    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    full_response = "<think>"
    state = ParserState()
    last_update = 0

    try:
        for chunk in streamer:
            if not active_gen[0]:
                break
            print(chunk, end="", flush=True)
            if chunk:
                full_response += chunk
                state, elapsed = parse_response(full_response, state)

                collapsible, answer_part = format_response(state, elapsed)
                history[-1][1] = "\n\n".join(collapsible + [answer_part])
                yield history, None 

        state, elapsed = parse_response(full_response, state)
        collapsible, answer_part = format_response(state, elapsed)
        history[-1][1] = "\n\n".join(collapsible + [answer_part])

        answer_text = answer_part.replace('<think>', '').replace('</think>', '').strip()

        audio_data = get_tts_wav(
            audio_select, 
            ref_text,
            prompt_language,
            answer_text,
            text_language,
            how_to_cut
        )
        yield history, audio_data

    except Exception as e:
        history[-1][1] = f"Error: {str(e)}"
        yield history, None
    finally:
        active_gen[0] = False
        t.join()

import pdb

gpt_path = os.environ.get(
    "gpt_path", "models/heart_girl/heartful_sister.ckpt"
)
sovits_path = os.environ.get("sovits_path", "models/heart_girl/heartful_sister.pth")
cnhubert_base_path = os.environ.get(
    "cnhubert_base_path", "pretrained_models/chinese-hubert-base"
)
bert_path = os.environ.get(
    "bert_path", "pretrained_models/chinese-roberta-wwm-ext-large"
)
infer_ttswebui = os.environ.get("infer_ttswebui", 9872)
infer_ttswebui = int(infer_ttswebui)
if "_CUDA_VISIBLE_DEVICES" in os.environ:
    os.environ["CUDA_VISIBLE_DEVICES"] = os.environ["_CUDA_VISIBLE_DEVICES"]
is_half = eval(os.environ.get("is_half", "True"))
import gradio as gr
from transformers import AutoModelForMaskedLM, AutoTokenizer
import numpy as np
import librosa,torch
from feature_extractor import cnhubert
cnhubert.cnhubert_base_path=cnhubert_base_path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import nltk
os.system("cp -r nltk_data /root/")

from module.models import SynthesizerTrn
from AR.models.t2s_lightning_module import Text2SemanticLightningModule
from text import cleaned_text_to_sequence
from text.cleaner import clean_text
from time import time as ttime
from module.mel_processing import spectrogram_torch
from my_utils import load_audio


device = "cuda" if torch.cuda.is_available() else "cpu"
is_half = eval(
    os.environ.get("is_half", "True" if torch.cuda.is_available() else "False")
)

tokenizer_bert = AutoTokenizer.from_pretrained(bert_path)
bert_model = AutoModelForMaskedLM.from_pretrained(bert_path)
if is_half == True:
    bert_model = bert_model.half().to(device)
else:
    bert_model = bert_model.to(device)


def get_bert_feature(text, word2ph):
    with torch.no_grad():
        inputs = tokenizer_bert(text, return_tensors="pt")
        for i in inputs:
            inputs[i] = inputs[i].to(device)  
        res = bert_model(**inputs, output_hidden_states=True)
        res = torch.cat(res["hidden_states"][-3:-2], -1)[0].cpu()[1:-1]
    assert len(word2ph) == len(text)
    # print("word2ph: ", word2ph)
    phone_level_feature = []
    for i in range(len(word2ph)):
        repeat_feature = res[i].repeat(word2ph[i], 1)
        phone_level_feature.append(repeat_feature)
    # print("phone_level_feature: ", phone_level_feature)
    phone_level_feature = torch.cat(phone_level_feature, dim=0)
    return phone_level_feature.T

class DictToAttrRecursive(dict):
    def __init__(self, input_dict):
        super().__init__(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, dict):
                value = DictToAttrRecursive(value)
            self[key] = value
            setattr(self, key, value)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"Attribute {item} not found")

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            value = DictToAttrRecursive(value)
        super(DictToAttrRecursive, self).__setitem__(key, value)
        super().__setattr__(key, value)

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(f"Attribute {item} not found")

ssl_model = cnhubert.get_model()
if is_half == True:
    ssl_model = ssl_model.half().to(device)
else:
    ssl_model = ssl_model.to(device)
print(333333333333333333333333)
def change_sovits_weights(sovits_path):
    global vq_model,hps
    print(os.path.isfile(sovits_path), 2222222)
    dict_s2=torch.load(sovits_path,map_location="cpu")
    hps=dict_s2["config"]
    hps = DictToAttrRecursive(hps)
    hps.model.semantic_frame_rate = "25hz"
    vq_model = SynthesizerTrn(
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model
    )
    if("pretrained"not in sovits_path):
        del vq_model.enc_q
    if is_half == True:
        vq_model = vq_model.half().to(device)
    else:
        vq_model = vq_model.to(device)
    vq_model.eval()
    print(vq_model.load_state_dict(dict_s2["weight"], strict=False))
change_sovits_weights(sovits_path)

def change_gpt_weights(gpt_path):
    global hz,max_sec,t2s_model,config
    hz = 50
    dict_s1 = torch.load(gpt_path, map_location="cpu")
    config = dict_s1["config"]
    max_sec = config["data"]["max_sec"]
    t2s_model = Text2SemanticLightningModule(config, "****", is_train=False)
    t2s_model.load_state_dict(dict_s1["weight"])
    if is_half == True:
        t2s_model = t2s_model.half()
    t2s_model = t2s_model.to(device)
    t2s_model.eval()
    total = sum([param.nelement() for param in t2s_model.parameters()])
    print("Number of parameter: %.2fM" % (total / 1e6))
change_gpt_weights(gpt_path)


def get_spepc(hps, filename):
    audio = load_audio(filename, int(hps.data.sampling_rate))
    audio = torch.FloatTensor(audio)
    audio_norm = audio
    audio_norm = audio_norm.unsqueeze(0)
    spec = spectrogram_torch(
        audio_norm,
        hps.data.filter_length,
        hps.data.sampling_rate,
        hps.data.hop_length,
        hps.data.win_length,
        center=False,
    )
    return spec


dict_language={
    ("中文"):"zh",
    ("英文"):"en",
    ("日文"):"ja"
}


def splite_en_inf(sentence, language):
    pattern = re.compile(r'[a-zA-Z. ]+')
    textlist = []
    langlist = []
    pos = 0
    for match in pattern.finditer(sentence):
        start, end = match.span()
        if start > pos:
            textlist.append(sentence[pos:start])
            langlist.append(language)
        textlist.append(sentence[start:end])
        langlist.append("en")
        pos = end
    if pos < len(sentence):
        textlist.append(sentence[pos:])
        langlist.append(language)

    return textlist, langlist


def clean_text_inf(text, language):
    phones, word2ph, norm_text = clean_text(text, language)
    phones = cleaned_text_to_sequence(phones)

    return phones, word2ph, norm_text
def get_bert_inf(phones, word2ph, norm_text, language):
    if language == "zh":
        bert = get_bert_feature(norm_text, word2ph).to(device)
    else:
        bert = torch.zeros(
            (1024, len(phones)),
            dtype=torch.float16 if is_half == True else torch.float32,
        ).to(device)

    return bert


def nonen_clean_text_inf(text, language):
    textlist, langlist = splite_en_inf(text, language)
    phones_list = []
    word2ph_list = []
    norm_text_list = []
    for i in range(len(textlist)):
        lang = langlist[i]
        phones, word2ph, norm_text = clean_text_inf(textlist[i], lang)
        phones_list.append(phones)
        if lang == "en" or "ja":
            pass
        else:
            word2ph_list.append(word2ph)
        norm_text_list.append(norm_text)
    phones = sum(phones_list, [])
    word2ph = sum(word2ph_list, [])
    norm_text = ' '.join(norm_text_list)

    return phones, word2ph, norm_text


def nonen_get_bert_inf(text, language):
    textlist, langlist = splite_en_inf(text, language)
    bert_list = []
    for i in range(len(textlist)):
        text = textlist[i]
        lang = langlist[i]
        phones, word2ph, norm_text = clean_text_inf(text, lang)
        bert = get_bert_inf(phones, word2ph, norm_text, lang)
        bert_list.append(bert)
    bert = torch.cat(bert_list, dim=1)

    return bert

def get_tts_wav(selected_text, prompt_text, prompt_language, text, text_language,how_to_cut=("不切")):
    ref_wav_path = text_to_audio_mappings.get(selected_text, "")
    if not ref_wav_path:
        print("Audio file not found for the selected text.")
        return
    t0 = ttime()
    prompt_text = prompt_text.strip("\n")
    prompt_language, text = prompt_language, text.strip("\n")
    zero_wav = np.zeros(
        int(hps.data.sampling_rate * 0.3),
        dtype=np.float16 if is_half == True else np.float32,
    )

    with torch.no_grad():
        wav16k, sr = librosa.load(ref_wav_path, sr=16000)
        wav16k = torch.from_numpy(wav16k)
        zero_wav_torch = torch.from_numpy(zero_wav)
        if is_half == True:
            wav16k = wav16k.half().to(device)
            zero_wav_torch = zero_wav_torch.half().to(device)
        else:
            wav16k = wav16k.to(device)
            zero_wav_torch = zero_wav_torch.to(device)
        print("zero_wav: ", zero_wav_torch)
        print("wav16k: ", wav16k)
        wav16k=torch.cat([wav16k,zero_wav_torch])
        ssl_content = ssl_model.model(wav16k.unsqueeze(0))[
            "last_hidden_state"
        ].transpose(
            1, 2
        )  # .float()
        codes = vq_model.extract_latent(ssl_content)
        prompt_semantic = codes[0, 0]
    t1 = ttime()
    
    prompt_language = dict_language[prompt_language]
    text_language = dict_language[text_language]
    if prompt_language == "en":
        phones1, word2ph1, norm_text1 = clean_text_inf(prompt_text, prompt_language)
    else:
        phones1, word2ph1, norm_text1 = nonen_clean_text_inf(prompt_text, prompt_language)
    if(how_to_cut==("凑五句一切")):text=cut1(text)
    elif(how_to_cut==("凑50字一切")):text=cut2(text)
    elif(how_to_cut==("按中文句号。切")):text=cut3(text)
    elif(how_to_cut==("按英文句号.切")):text=cut4(text)
    text = text.replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")
    if(text[-1]not in splits):text+="。"if text_language!="en"else "."
    texts=text.split("\n")
    audio_opt = []
    if prompt_language == "en":
        bert1 = get_bert_inf(phones1, word2ph1, norm_text1, prompt_language)
    else:
        bert1 = nonen_get_bert_inf(prompt_text, prompt_language)
    for text in texts:
        # 解决输入目标文本的空行导致报错的问题
        if (len(text.strip()) == 0):
            continue
        if text_language == "en":
            phones2, word2ph2, norm_text2 = clean_text_inf(text, text_language)
        else:
            phones2, word2ph2, norm_text2 = nonen_clean_text_inf(text, text_language)

        if text_language == "en":
            bert2 = get_bert_inf(phones2, word2ph2, norm_text2, text_language)
        else:
            bert2 = nonen_get_bert_inf(text, text_language)
        bert = torch.cat([bert1, bert2], 1)

        all_phoneme_ids = torch.LongTensor(phones1 + phones2).to(device).unsqueeze(0)
        bert = bert.to(device).unsqueeze(0)
        all_phoneme_len = torch.tensor([all_phoneme_ids.shape[-1]]).to(device)
        prompt = prompt_semantic.unsqueeze(0).to(device)
        t2 = ttime()
        with torch.no_grad():
            # pred_semantic = t2s_model.model.infer(
            pred_semantic, idx = t2s_model.model.infer_panel(
                all_phoneme_ids,
                all_phoneme_len,
                prompt,
                bert,
                # prompt_phone_len=ph_offset,
                top_k=config["inference"]["top_k"],
                early_stop_num=hz * max_sec,
            )
        t3 = ttime()
        # print(pred_semantic.shape,idx)
        pred_semantic = pred_semantic[:, -idx:].unsqueeze(
            0
        )  # .unsqueeze(0)#mq要多unsqueeze一次
        refer = get_spepc(hps, ref_wav_path)  # .to(device)
        if is_half == True:
            refer = refer.half().to(device)
        else:
            refer = refer.to(device)
        # audio = vq_model.decode(pred_semantic, all_phoneme_ids, refer).detach().cpu().numpy()[0, 0]
        audio = (
            vq_model.decode(
                pred_semantic, torch.LongTensor(phones2).to(device).unsqueeze(0), refer
            )
            .detach()
            .cpu()
            .numpy()[0, 0]
        ) 
        audio_opt.append(audio)
        audio_opt.append(zero_wav)
        t4 = ttime()
    print("%.3f\t%.3f\t%.3f\t%.3f" % (t1 - t0, t2 - t1, t3 - t2, t4 - t3))
    return hps.data.sampling_rate, (np.concatenate(audio_opt, 0) * 32768).astype(
        np.int16
    )


splits = {
    "，",
    "。",
    "？",
    "！",
    ",",
    ".",
    "?",
    "!",
    "~",
    ":",
    "：",
    "—",
    "…",
}  


def split(todo_text):
    todo_text = todo_text.replace("……", "。").replace("——", "，")
    if todo_text[-1] not in splits:
        todo_text += "。"
    i_split_head = i_split_tail = 0
    len_text = len(todo_text)
    todo_texts = []
    while 1:
        if i_split_head >= len_text:
            break 
        if todo_text[i_split_head] in splits:
            i_split_head += 1
            todo_texts.append(todo_text[i_split_tail:i_split_head])
            i_split_tail = i_split_head
        else:
            i_split_head += 1
    return todo_texts


def cut1(inp):
    inp = inp.strip("\n")
    inps = split(inp)
    split_idx = list(range(0, len(inps), 5))
    split_idx[-1] = None
    if len(split_idx) > 1:
        opts = []
        for idx in range(len(split_idx) - 1):
            opts.append("".join(inps[split_idx[idx] : split_idx[idx + 1]]))
    else:
        opts = [inp]
    return "\n".join(opts)


def cut2(inp):
    inp = inp.strip("\n")
    inps = split(inp)
    if len(inps) < 2:
        return [inp]
    opts = []
    summ = 0
    tmp_str = ""
    for i in range(len(inps)):
        summ += len(inps[i])
        tmp_str += inps[i]
        if summ > 50:
            summ = 0
            opts.append(tmp_str)
            tmp_str = ""
    if tmp_str != "":
        opts.append(tmp_str)
    if len(opts[-1]) < 50: 
        opts[-2] = opts[-2] + opts[-1]
        opts = opts[:-1]
    return "\n".join(opts)


def cut3(inp):
    inp = inp.strip("\n")
    return "\n".join(["%s。" % item for item in inp.strip("。").split("。")])
def cut4(inp):
    inp = inp.strip("\n")
    return "\n".join(["%s." % item for item in inp.strip(".").split(".")])

def scan_audio_files(folder_path):
    """ 扫描指定文件夹获取音频文件列表 """
    return [f for f in os.listdir(folder_path) if f.endswith('.wav')]

def load_audio_text_mappings(folder_path, list_file_name):
    text_to_audio_mappings = {}
    audio_to_text_mappings = {}
    with open(os.path.join(folder_path, list_file_name), 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                audio_file_name = parts[0]
                text = parts[3]
                audio_file_path = os.path.join(folder_path, audio_file_name)
                text_to_audio_mappings[text] = audio_file_path
                audio_to_text_mappings[audio_file_path] = text
    return text_to_audio_mappings, audio_to_text_mappings

audio_folder_path = 'audio/heart_girl'
text_to_audio_mappings, audio_to_text_mappings = load_audio_text_mappings(audio_folder_path, 'slicer_opt.list')

with gr.Blocks(css=CSS) as demo:
    gr.Markdown(DESCRIPTION)

    active_gen = gr.State([False])
    conversation_id = gr.State(value=new_conversation_id)
    search_enabled = gr.Checkbox(value=True, label="Web search (send message to search provider)")
    
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        height=500,
        show_label=False,
        render_markdown=True
    )

    with gr.Row():
        msg = gr.Textbox(
            label="Message",
            placeholder="Type your message...",
            container=False,
            scale=4
        )
        submit_btn = gr.Button("Send", variant='primary', scale=1)
    
    with gr.Column(scale=2):
        with gr.Row():
            clear_btn = gr.Button("Clear", variant='secondary')
            stop_btn = gr.Button("Stop", variant='stop')
        
        with gr.Accordion("Parameters", open=False):
            temperature = gr.Slider(minimum=0.1, maximum=1.5, value=0.6, label="Temperature")
            top_p = gr.Slider(minimum=0.1, maximum=1.0, value=0.95, label="Top-p")
            max_tokens = gr.Slider(minimum=2048, maximum=32768, value=4096, step=64, label="Max Tokens")

    gr.Examples(
        examples=[
            ["你是谁呀"],
            ["我很难过，爸妈不爱我"],
            ["爸妈老是说我笨"]
        ],
        inputs=msg,
        label="咨询例子"
    )

    # with gr.Row():
    #     audio_select = gr.Dropdown(label="选择参考音频（必选）", choices=list(text_to_audio_mappings.keys()))
    #     ref_audio = gr.Audio(label="参考音频试听", autoplay=False)
    #     ref_text = gr.Textbox(label="参考音频文本")
    #     text_language = gr.Dropdown(
    #         label="需要合成的语种", choices=["中文", "英文", "日文"], value="中文"
    #     )
    #     how_to_cut = gr.Radio(
    #         label=("自动切分（长文本建议切分）"),
    #         choices=[("不切"),("凑五句一切"),("凑50字一切"),("按中文句号。切"),("按英文句号.切"),],
    #         value=("不切"),
    #         interactive=True,
    #     )
    #     prompt_language = gr.Dropdown(
    #         label="参考音频语种", choices=["中文", "英文", "日文"], value="中文"
    #     )

    # def update_ref_text_and_audio(selected_text):
    #     audio_path = text_to_audio_mappings.get(selected_text, "")
    #     return selected_text, audio_path

    # audio_select.change(update_ref_text_and_audio, [audio_select], [ref_text, ref_audio])

    DEFAULT_AUDIO_SELECT = list(text_to_audio_mappings.keys())[0]  # 假设有一个默认的音频选择
    DEFAULT_REF_TEXT = list(text_to_audio_mappings.keys())[0]
    DEFAULT_PROMPT_LANGUAGE = "中文"
    DEFAULT_TEXT_LANGUAGE = "中文"
    DEFAULT_HOW_TO_CUT = "不切"

    output_audio = gr.Audio(label="converted voice", autoplay=True)

    submit_event = submit_btn.click(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        lambda: [True], outputs=active_gen
    ).then(
        generate_response_and_tts, 
        [chatbot, temperature, top_p, max_tokens, active_gen, 
         gr.State(DEFAULT_AUDIO_SELECT), gr.State(DEFAULT_REF_TEXT), 
         gr.State(DEFAULT_PROMPT_LANGUAGE), gr.State(DEFAULT_TEXT_LANGUAGE), 
         gr.State(DEFAULT_HOW_TO_CUT), conversation_id, search_enabled],
        [chatbot, output_audio]
    )

    enter_event = msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        lambda: [True], outputs=active_gen
    ).then(
        generate_response_and_tts, 
        [chatbot, temperature, top_p, max_tokens, active_gen, 
         gr.State(DEFAULT_AUDIO_SELECT), gr.State(DEFAULT_REF_TEXT), 
         gr.State(DEFAULT_PROMPT_LANGUAGE), gr.State(DEFAULT_TEXT_LANGUAGE), 
         gr.State(DEFAULT_HOW_TO_CUT), conversation_id, search_enabled],
        [chatbot, output_audio]
    )

    stop_btn.click(
        stop_generation, active_gen, active_gen, cancels=[submit_event, enter_event], queue=False
    )

    clear_btn.click(
        stop_generation, active_gen, active_gen, cancels=[submit_event, enter_event], queue=False
    ).then(
        lambda: (None, new_conversation_id()), None, [chatbot, conversation_id], queue=False
    )



if __name__ == "__main__":
    demo.queue(api_open=False, max_size=20, default_concurrency_limit=20).launch(server_name="0.0.0.0", server_port=7860, max_threads=40)
