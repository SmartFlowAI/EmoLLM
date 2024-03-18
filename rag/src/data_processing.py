import json
import pickle
from loguru import logger
from sentence_transformers import SentenceTransformer

from config.config import embedding_path, doc_dir, qa_dir, knowledge_pkl_path, data_dir, base_dir, vector_db_dir
import os
import faiss
import platform
from langchain_community.document_loaders import DirectoryLoader, TextLoader, JSONLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from BCEmbedding import EmbeddingModel, RerankerModel
from util.pipeline import EmoLLMRAG
import pickle
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st
from openxlab.model import download


'''
1）根据QA对/TXT 文本生成 embedding 
2）调用 langchain FAISS 接口构建 vector DB 
3）存储到 openxlab.dataset 中，方便后续调用
4）提供 embedding 的接口函数，方便后续调用
5）提供 rerank 的接口函数，方便后续调用
'''

"""
加载向量模型
"""
def load_embedding_model():
    logger.info('Loading embedding model...')
    # model = EmbeddingModel(model_name_or_path="huggingface/bce-embedding-base_v1")   
    model = EmbeddingModel(model_name_or_path="maidalun1020/bce-embedding-base_v1")
    logger.info('Embedding model loaded.')
    return model

def load_rerank_model():
    logger.info('Loading rerank_model...')
    model = RerankerModel(model_name_or_path="maidalun1020/bce-reranker-base_v1")
    # model = RerankerModel(model_name_or_path="huggingface/bce-reranker-base_v1")
    logger.info('Rerank model loaded.')
    return model


def split_document(data_path, chunk_size=1000, chunk_overlap=100):
    # text_spliter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap) 
    split_docs = []
    logger.info(f'Loading txt files from {data_path}')
    if os.path.isdir(data_path):
        # 如果是文件夹，则遍历读取
        for root, dirs, files in os.walk(data_path):
            for file in files:      
                if file.endswith('.txt'):            
                    file_path = os.path.join(root, file)
                    # logger.info(f'splitting file {file_path}')
                    text_loader = TextLoader(file_path, encoding='utf-8')        
                    text = text_loader.load()
                    
                    splits = text_spliter.split_documents(text)
                    # logger.info(f"splits type {type(splits[0])}")
                    # logger.info(f'splits size {len(splits)}')
                    split_docs += splits
    elif file.endswith('.txt'): 
        file_path = os.path.join(root, file)
        # logger.info(f'splitting file {file_path}')
        text_loader = TextLoader(file_path, encoding='utf-8')        
        text = text_loader.load()
        splits = text_spliter.split_documents(text)
        # logger.info(f"splits type {type(splits[0])}")
        # logger.info(f'splits size {len(splits)}')
        split_docs = splits
    logger.info(f'split_docs size {len(split_docs)}')
    return split_docs


##TODO 1、读取system prompt 2、限制序列长度
def split_conversation(path):
    '''
    data format:
    [
        {
            "conversation": [
                {
                    "input":  Q1
                    "output": A1
                },
                {
                    "input":  Q2
                    "output": A2
                },
            ]
        },
    ]
    '''
    qa_pairs = []
    logger.info(f'Loading json files from {path}')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for conversation in data:
            for dialog in conversation['conversation']:
                # input_text = dialog['input']
                # output_text = dialog['output']      
                # if len(input_text) > max_length or len(output_text) > max_length:
                #     continue
                qa_pairs.append(dialog)        
    elif os.path.isdir(path):
        # 如果是文件夹，则遍历读取
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.json'): 
                    file_path = os.path.join(root, file)
                    logger.info(f'splitting file {file_path}')
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for conversation in data:
                            for dialog in conversation['conversation']:
                                qa_pairs.append(dialog)
    return qa_pairs


        
# 加载本地索引
def load_index_and_knowledge():
    current_os = platform.system()
    split_doc = []
    split_qa = []
    #读取知识库
    if not os.path.exists(knowledge_pkl_path):
        split_doc = split_document(doc_dir)
        split_qa = split_conversation(qa_dir)
    # logger.info(f'split_qa size:{len(split_qa)}')
    # logger.info(f'type of split_qa:{type(split_qa[0])}')
    # logger.info(f'split_doc size:{len(split_doc)}')
    # logger.info(f'type of doc:{type(split_doc[0])}')
        knowledge_chunks = split_doc + split_qa
        with open(knowledge_pkl_path, 'wb') as file:
            pickle.dump(knowledge_chunks, file)
    else:
        with open(knowledge_pkl_path , 'rb') as f:
            knowledge_chunks = pickle.load(f)
        
    #读取vector DB
    if not os.path.exists(vector_db_dir):
        logger.info(f'Creating index...')
        emb_model = load_embedding_model()
        if not split_doc:
            split_doc = split_document(doc_dir)
        if not split_qa:
            split_qa = split_conversation(qa_dir)
        # 创建索引,windows不支持faiss-gpu
        if current_os == 'Linux':
            index = create_index_gpu(split_doc, split_qa, emb_model, vector_db_dir)
        else:
            index = create_index_cpu(split_doc, split_qa, emb_model, vector_db_dir)
    else:
        if current_os == 'Linux':
            res = faiss.StandardGpuResources()
            index = faiss.index_cpu_to_gpu(res, 0, index, vector_db_dir)
        else:
            index = faiss.read_index(vector_db_dir)
    
    return index, knowledge_chunks


def create_index_cpu(split_doc, split_qa, emb_model, knowledge_pkl_path, dimension = 768, question_only=False):
    # 假设BCE嵌入的维度是768，根据你选择的模型可能不同
    faiss_index_cpu = faiss.IndexFlatIP(dimension)  # 创建一个使用内积的FAISS索引
    # 将问答对转换为向量并添加到FAISS索引中
    for doc in split_doc:
        # type_of_docs = type(split_doc) 
        text = f"{doc.page_content}"
        vector = emb_model.encode([text])
        faiss_index_cpu.add(vector)
    for qa in split_qa:
        #仅对Q对进行编码
        text = f"{qa['input']}"
        vector = emb_model.encode([text])
        faiss_index_cpu.add(vector)
    faiss.write_index(faiss_index_cpu, knowledge_pkl_path)
    return faiss_index_cpu

def create_index_gpu(split_doc, split_qa, emb_model, knowledge_pkl_path, dimension = 768, question_only=False):
    res = faiss.StandardGpuResources()
    index = faiss.IndexFlatIP(dimension)
    faiss_index_gpu = faiss.index_cpu_to_gpu(res, 0, index)
    for doc in split_doc:
        # type_of_docs = type(split_doc)
        text = f"{doc.page_content}"
        vector = emb_model.encode([text])
        faiss_index_gpu.add(vector)
    for qa in split_qa:
        #仅对Q对进行编码
        text = f"{qa['input']}"
        vector = emb_model.encode([text])
        faiss_index_gpu.add(vector)
    faiss.write_index(faiss_index_gpu, knowledge_pkl_path)
    return faiss_index_gpu

   

# 根据query搜索相似文本
def find_top_k(query, faiss_index, k=5):
    emb_model = load_embedding_model()
    emb_query = emb_model.encode([query])
    distances, indices = faiss_index.search(emb_query, k)
    return distances, indices

def rerank(query, indices, knowledge_chunks):
    passages = []
    for index in indices[0]:
        content = knowledge_chunks[index]
        '''
        txt: 'langchain_core.documents.base.Document'
        json: dict
        '''
        # logger.info(f'retrieved content:{content}')
        # logger.info(f'type of content:{type(content)}')
        if type(content) == dict:
            content = content["input"] + '\n' + content["output"]
        else:
            content = content.page_content
        passages.append(content)
    
    model = load_rerank_model()
    rerank_results = model.rerank(query, passages)
    return rerank_results

@st.cache_resource
def load_model():
    model = (
        AutoModelForCausalLM.from_pretrained("model", trust_remote_code=True)
        .to(torch.bfloat16)
        .cuda()
    )
    tokenizer = AutoTokenizer.from_pretrained("model", trust_remote_code=True)
    return model, tokenizer

if __name__ == "__main__":
    logger.info(data_dir)
    if not os.path.exists(data_dir):
         os.mkdir(data_dir)
    faiss_index, knowledge_chunks = load_index_and_knowledge()
    # 按照query进行查询
    # query = "她要阻挠姐姐的婚姻，即使她自己的尸体在房门跟前"
    # query = "肯定的。我最近睡眠很差，总是做噩梦。而且我吃得也不好，体重一直在下降"
    # query = "序言 （一） 变态心理学是心理学本科生的必修课程之一，教材更新的问题一直在困扰着我们。"
    query = "心理咨询师，我觉得我的胸闷症状越来越严重了，这让我很害怕"
    distances, indices = find_top_k(query, faiss_index, 5)
    logger.info(f'distances==={distances}')
    logger.info(f'indices==={indices}')
   

    # rerank无法返回id，先实现按整个问答对排序
    rerank_results = rerank(query, indices, knowledge_chunks)
    for passage, score in zip(rerank_results['rerank_passages'], rerank_results['rerank_scores']):
        print(str(score)+'\n')
        print(passage+'\n')
  