from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from transformers.utils import logging

from rag.src.data_processing import Data_process
from rag.src.config.config import prompt_template 
logger = logging.get_logger(__name__)


class EmoLLMRAG(object):
    """
        EmoLLM RAG Pipeline
            1. 根据 query 进行 embedding
            2. 从 vector DB 中检索数据
            3. rerank 检索后的结果
            4. 将 query 和检索回来的 content 传入 LLM 中
    """

    def __init__(self, model, retrieval_num=3, rerank_flag=False, select_num=3) -> None:
        """
            输入 Model 进行初始化 

            DataProcessing obj: 进行数据处理，包括数据 embedding/rerank
            vectorstores: 加载vector DB。如果没有应该重新创建
            system prompt: 获取预定义的 system prompt
            prompt template: 定义最后的输入到 LLM 中的 template

        """
        self.model = model
        self.data_processing_obj = Data_process()
        self.vectorstores = self._load_vector_db()
        self.prompt_template = prompt_template
        self.retrieval_num = retrieval_num
        self.rerank_flag = rerank_flag
        self.select_num = select_num

    def _load_vector_db(self):
        """
            调用 embedding 模块给出接口 load vector DB
        """
        vectorstores = self.data_processing_obj.load_vector_db()

        return vectorstores 

    def get_retrieval_content(self, query) -> str:
        """
            Input: 用户提问, 是否需要rerank
            output: 检索后并且 rerank 的内容        
        """
    
        content = []
        documents = self.vectorstores.similarity_search(query, k=self.retrieval_num)

        for doc in documents:
            content.append(doc.page_content)

        # 如果需要rerank，调用接口对 documents 进行 rerank
        if self.rerank_flag:
            documents, _ = self.data_processing_obj.rerank(documents, self.select_num)

            content = []
            for doc in documents:
                content.append(doc)
        logger.info(f'Retrieval data: {content}')
        return content
    
    def generate_answer(self, query, content) -> str:
        """
            Input: 用户提问， 检索返回的内容
            Output: 模型生成结果
        """

        # 构建 template 
        # 第一版不涉及 history 信息，因此将 system prompt 直接纳入到 template 之中
        prompt = PromptTemplate(
                template=self.prompt_template,
                input_variables=["query", "content"],
                )

        # 定义 chain
        # output格式为 string
        rag_chain = prompt | self.model | StrOutputParser()

        # Run
        generation = rag_chain.invoke(
                {
                    "query": query,
                    "content": content,
                }
            )
        return generation
    
    def main(self, query) -> str:
        """
            Input: 用户提问
            output: LLM 生成的结果

            定义整个 RAG 的 pipeline 流程，调度各个模块
            TODO:
                加入 RAGAS 评分系统
        """
        content = self.get_retrieval_content(query)
        response = self.generate_answer(query, content)

        return response
