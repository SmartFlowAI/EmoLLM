import json
import pickle
from loguru import logger
from sentence_transformers import SentenceTransformer

from config.config import embedding_path


"""
加载向量模型
"""
def load_embedding() -> SentenceTransformer:
    logger.info('Loading embedding...')
    emb = SentenceTransformer(embedding_path)
    logger.info('Embedding loaded.')
    return emb


"""
文本编码
"""
def encode_raw_corpus(file_path: str, store_path: str) -> None:
    emb = load_embedding()
    with open(file_path, 'r', encoding='utf-8') as f:
        read_lines = f.readlines()
    
    """
    对文本分割（例如：按句子分割）
    """
    lines = []
    # 分割好后的存入 lines 中

    # 编码（转换为向量）
    encoded_knowledge = emb.encode(lines)
    with open(store_path, 'wb') as f:
        pickle.dump(encoded_knowledge, f)


"""
QA 对编码
暂时只实现了加载 json，csv和txt先没写
"""
def encode_qa(file_path: str, store_path: str) -> None:
    emb = load_embedding()
    with open(file_path, 'r', encoding='utf-8') as f:
        qa_list = json.load(f)
    
    # 将 QA 对拼起来作为完整一句来编码，也可以只编码 Q
    lines = []
    for qa in qa_list:
        question = qa['question']
        answer = qa['answer']
        lines.append(question + answer)

    encoded_knowledge = emb.encode(lines)
    with open(store_path, 'wb') as f:
        pickle.dump(encoded_knowledge, f)
