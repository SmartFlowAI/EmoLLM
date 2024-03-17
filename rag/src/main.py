import os
import json
import pickle
import numpy as np
from typing import Tuple
from sentence_transformers import SentenceTransformer

from config.config import knowledge_json_path, knowledge_pkl_path, model_repo
from util.encode import load_embedding, encode_qa
from util.pipeline import EmoLLMRAG

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st
from openxlab.model import download

download(
    model_repo=model_repo, 
    output='model'
)


"""
读取知识库
"""
def load_knowledge() -> Tuple[list, list]:
    # 如果 pkl 不存在，则先编码存储
    if not os.path.exists(knowledge_pkl_path):
        encode_qa(knowledge_json_path, knowledge_pkl_path)

    # 加载 json 和 pkl
    with open(knowledge_json_path, 'r', encoding='utf-8') as f1, open(knowledge_pkl_path, 'rb') as f2:
        knowledge = json.load(f1)
        encoded_knowledge = pickle.load(f2)
    return knowledge, encoded_knowledge


"""
召回 top_k 个相关的文本段
"""
def find_top_k(
    emb: SentenceTransformer,
    query: str,
    knowledge: list,
    encoded_knowledge: list,
    k=3
) -> list[str]:
    # 编码 query
    query_embedding = emb.encode(query)

    # 查找 top_k
    scores = query_embedding @ encoded_knowledge.T
    # 使用 argpartition 找出每行第 k 个大的值的索引，第 k 个位置左侧都是比它大的值，右侧都是比它小的值
    top_k_indices = np.argpartition(scores, -k)[-k:]
    # 由于 argpartition 不保证顺序，我们需要对提取出的 k 个索引进行排序
    top_k_values_sorted_indices = np.argsort(scores[top_k_indices])[::-1]
    top_k_indices = top_k_indices[top_k_values_sorted_indices]

    # 返回
    contents = [knowledge[index] for index in top_k_indices]
    return contents
    

def main():
    emb = load_embedding()
    knowledge, encoded_knowledge = load_knowledge()
    query = "认知心理学研究哪些心理活动？"
    contents = find_top_k(emb, query, knowledge, encoded_knowledge, 2)
    print('召回的 top-k 条相关内容如下：')
    print(json.dumps(contents, ensure_ascii=False, indent=2))
    # 这里我没实现 LLM 部分，如果有 LLM
    ## 1. 读取 LLM
    ## 2. 将 contents 拼接为 prompt，传给 LLM，作为 {已知内容}
    ## 3. 要求 LLM 根据已知内容回复

@st.cache_resource
def load_model():
    model = (
        AutoModelForCausalLM.from_pretrained("model", trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained("model", trust_remote_code=True)
    return model, tokenizer

if __name__ == '__main__':
    #main()
    query = ''
    model, tokenizer = load_model()
    rag_obj = EmoLLMRAG(model)
    response = rag_obj.main(query)