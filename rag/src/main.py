import os
import time
import jwt

from config.config import base_dir, data_dir
from data_processing import Data_process
from pipeline import EmoLLMRAG

from langchain_openai import ChatOpenAI
from loguru import logger
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st
from openxlab.model import download
'''
	1）构建完整的 RAG pipeline。输入为用户 query，输出为 answer
	2）调用 embedding 提供的接口对 query 向量化
	3）下载基于 FAISS 预构建的 vector DB ，并检索对应信息
	4）调用 rerank 接口重排序检索内容
	5）调用 prompt 接口获取 system prompt 和 prompt template
	6）拼接 prompt 并调用模型返回结果

'''
def get_glm(temprature):
    llm = ChatOpenAI(
        model_name="glm-4",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4",
        openai_api_key=generate_token("api-key"),
        streaming=False,
        temperature=temprature
    )
    return llm 

def generate_token(apikey: str, exp_seconds: int=100):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)
 
    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
 
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

@st.cache_resource
def load_model():
    model_dir = os.path.join(base_dir,'../model') 
    logger.info(f'Loading model from {model_dir}')
    model = (
        AutoModelForCausalLM.from_pretrained('model', trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained('model', trust_remote_code=True)
    return model, tokenizer

def main(query, system_prompt=''):
    logger.info(data_dir)
    if not os.path.exists(data_dir):
         os.mkdir(data_dir)   
    dp = Data_process()
    vector_db = dp.load_vector_db()
    docs, retriever = dp.retrieve(query, vector_db, k=10)
    logger.info(f'Query: {query}')
    logger.info("Retrieve results===============================")
    for i, doc in enumerate(docs):
        logger.info(doc)
    passages,scores = dp.rerank(query, docs)
    logger.info("After reranking===============================")
    for i in range(len(scores)):
        logger.info(passages[i])
        logger.info(f'score: {str(scores[i])}')

if __name__ == "__main__":
    query = "我现在处于高三阶段，感到非常迷茫和害怕。我觉得自己从出生以来就是多余的，没有必要存在于这个世界。无论是在家庭、学校、朋友还是老师面前，我都感到被否定。我非常难过，对高考充满期望但成绩却不理想"
    main(query)
    #model = get_glm(0.7)
    #rag_obj = EmoLLMRAG(model, 3)
    #res = rag_obj.main(query)
    #logger.info(res)

