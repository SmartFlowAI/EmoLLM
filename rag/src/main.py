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
        我现在处于高三阶段，感到非常迷茫和害怕。我觉得自己从出生以来就是多余的，没有必要存在于这个世界。
        无论是在家庭、学校、朋友还是老师面前，我都感到被否定。我非常难过，对高考充满期望但成绩却不理想
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

