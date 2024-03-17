from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from transformers.utils import logging

from config.config import retrieval_num, select_num

logger = logging.get_logger(__name__)


class EmoLLMRAG(object):
    """
        EmoLLM RAG Pipeline
            1. 根据 query 进行 embedding
            2. 从 vector DB 中检索数据
            3. rerank 检索后的结果
            4. 将 query 和检索回来的 content 传入 LLM 中
    """

    def __init__(self, model) -> None:
        """
            输入 Model 进行初始化 

            DataProcessing obj: 进行数据处理，包括数据 embedding/rerank
            vectorstores: 加载vector DB。如果没有应该重新创建
            system prompt: 获取预定义的 system prompt
            prompt template: 定义最后的输入到 LLM 中的 template

        """
        self.model = model
        self.vectorstores = self._load_vector_db()
        self.system_prompt = self._get_system_prompt()
        self.prompt_template = self._get_prompt_template()

        # 等待 embedding team 封装对应接口
        #self.data_process_obj = DataProcessing()

    def _load_vector_db(self):
        """
            调用 embedding 模块给出接口 load vector DB
        """
        return 
    
    def _get_system_prompt(self) -> str:
        """
            加载 system prompt
        """
        return ''

    def _get_prompt_template(self) -> str:
        """
            加载 prompt template
        """
        return ''

    def get_retrieval_content(self, query, rerank_flag=False) -> str:
        """
            Input: 用户提问, 是否需要rerank
            ouput: 检索后并且 rerank 的内容        
        """
    
        content = ''
        documents = self.vectorstores.similarity_search(query, k=retrieval_num)

        # 如果需要rerank，调用接口对 documents 进行 rerank
        if rerank_flag:
            pass
            # 等后续调用接口
            #documents = self.data_process_obj.rerank_documents(documents, select_num)

        for doc in documents:
            content += doc.page_content

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
                input_variables=["query", "content", "system_prompt"],
                )

        # 定义 chain
        # output格式为 string
        rag_chain = prompt | self.model | StrOutputParser()

        # Run
        generation = rag_chain.invoke(
                {
                    "query": query,
                    "content": content,
                    "system_prompt": self.system_prompt
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
