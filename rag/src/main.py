import os
import json
import pickle
import numpy as np
from typing import Tuple
from sentence_transformers import SentenceTransformer

from config.config import knowledge_json_path, knowledge_pkl_path, model_repo, model_dir, base_dir
from util.encode import load_embedding, encode_qa
from util.pipeline import EmoLLMRAG
from loguru import logger
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st
from openxlab.model import download
from data_processing import load_index_and_knowledge, create_index_cpu, create_index_gpu, find_top_k, rerank
from config.config import embedding_path, doc_dir, qa_dir, knowledge_pkl_path, data_dir

'''
	1）构建完整的 RAG pipeline。输入为用户 query，输出为 answer
	2）调用 embedding 提供的接口对 query 向量化
	3）下载基于 FAISS 预构建的 vector DB ，并检索对应信息
	4）调用 rerank 接口重排序检索内容
	5）调用 prompt 接口获取 system prompt 和 prompt template
	6）拼接 prompt 并调用模型返回结果

'''
# download(
#     model_repo=model_repo, 
#     output='model'
# )

@st.cache_resource
def load_model():
    model_dir = os.path.join(base_dir,'../model') 
    logger.info(f'Loading model from {model_dir}')
    model = (
        AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    return model, tokenizer

def get_prompt():
    pass

def get_prompt_template():
    pass

def main(query, system_prompt):
    model, tokenizer = load_model()
    model = model.eval()
    if not os.path.exists(data_dir):
         os.mkdir(data_dir)
    # 下载基于 FAISS 预构建的 vector DB 以及原始知识库
    faiss_index, knowledge_chunks = load_index_and_knowledge()
    distances, indices = find_top_k(query, faiss_index, 5)
    rerank_results = rerank(query, indices, knowledge_chunks)
    messages = [(system_prompt, rerank_results['rerank_passages'][0])]
    logger.info(f'messages:{messages}')
    response, history = model.chat(tokenizer, query, history=messages)
    messages.append((query, response))
    print(f"robot >>> {response}")  
    
if __name__ == '__main__':
    # query = '你好' 
    query = "心理咨询师，我觉得我的胸闷症状越来越严重了，这让我很害怕"
    #TODO system_prompt = get_prompt()
    system_prompt = "你是一个由aJupyter、Farewell、jujimeizuo、Smiling&Weeping研发（排名按字母顺序排序，不分先后）、散步提供技术支持、上海人工智能实验室提供支持开发的心理健康大模型。现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。"
    main(query, system_prompt)