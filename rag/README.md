# EmoLLM RAG

## **模块目的** 

根据用户的问题，检索对应信息以增强回答的专业性, 使EmoLLM的回答更加专业可靠。检索内容包括但不限于以下几点：
- 心理学相关理论
- 心理学方法论
- 经典案例
- 客户背景知识

## **数据集**

数据构建详情参考[qa_generation_README](https://github.com/SmartFlowAI/EmoLLM/blob/ccfa75c493c4685e84073dfbc53c50c09a2988e3/scripts/qa_generation/README.md)

- 经过清洗的QA对: 每一个QA对作为一个样本进行 embedding
- 经过筛选的TXT文本
	- 直接对TXT文本生成embedding (基于token长度进行切分)
	- 过滤目录等无关信息后对TXT文本生成embedding (基于token长度进行切分)
	- 过滤目录等无关信息后, 对TXT进行语意切分生成embedding
	- 按照目录结构对TXT进行拆分，构架层级关系生成embedding

## **相关组件**

### [BCEmbedding](https://github.com/netease-youdao/BCEmbedding?tab=readme-ov-file)

- [bce-embedding-base_v1](https://hf-mirror.com/maidalun1020/bce-embedding-base_v1): embedding 模型，用于构建 vector DB
- [bce-reranker-base_v1](https://hf-mirror.com/maidalun1020/bce-reranker-base_v1): rerank 模型，用于对检索回来的文章段落重排

### [Langchain](https://python.langchain.com/docs/get_started)

LangChain 是一个开源框架，用于构建基于大型语言模型（LLM）的应用程序。LangChain 提供各种工具和抽象，以提高模型生成的信息的定制性、准确性和相关性。

### [FAISS](https://faiss.ai/)

Faiss是一个用于高效相似性搜索和密集向量聚类的库。它包含的算法可以搜索任意大小的向量集。由于langchain已经整合过FAISS，因此本项目中不在基于原生文档开发，[FAISS in Langchain](https://python.langchain.com/docs/integrations/vectorstores/faiss)


### [RAGAS](https://github.com/explodinggradients/ragas)

RAG的经典评估框架，通过以下三个方面进行评估:

- Faithfulness: 给出的答案应该是以给定上下文为基础生成的。
- Answer Relevance: 生成的答案应该可以解决提出的实际问题。
- Context Relevance: 检索回来的信息应该是高度集中的，尽量少的包含不相关信息。

后续增加了更多的评判指标，例如：context recall 等


## **方案细节**

### RAG具体流程

- 根据数据集构建vector DB
- 对用户输入的问题进行embedding
- 基于embedding结果在向量数据库中进行检索
- 对召回数据重排序
- 依据用户问题和召回数据生成最后的结果

### 后续增强

- 将RAGAS评判结果加入到生成流程中。例如，当生成结果无法解决用户问题时，需要重新生成
- 增加










