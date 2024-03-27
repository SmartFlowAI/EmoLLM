from pipeline import EmoLLMRAG
from util.llm import get_glm
from loguru import logger
'''
	1）构建完整的 RAG pipeline。输入为用户 query，输出为 answer
	2）调用 embedding 提供的接口对 query 向量化
	3）下载基于 FAISS 预构建的 vector DB ，并检索对应信息
	4）调用 rerank 接口重排序检索内容
	5）调用 prompt 接口获取 system prompt 和 prompt template
	6）拼接 prompt 并调用模型返回结果

'''

if __name__ == "__main__":
    query = """
        我现在经常会被别人催眠，做一些我不愿意做的事情，是什么原因？
    """

    """
    输入:
        model_name='glm-4',
        api_base="https://open.bigmodel.cn/api/paas/v4",
        temprature=0.7,
        streaming=False,
    输出：
        LLM Model
    """
    model = get_glm()

    """
    输入:
        LLM model
        retrieval_num=3 
        rerank_flag=False
        select_num-3
    """
    rag_obj = EmoLLMRAG(model)

    res = rag_obj.main(query)

    logger.info(res)

