# EmoLLM RAG

## **模块目的** 

根据用户的问题，检索对应信息以增强回答的专业性, 使EmoLLM的回答更加专业可靠。检索内容包括但不限于以下几点：
- 心理学相关理论
- 心理学方法论
- 经典案例
- 客户背景知识

## **环境准备**

```python

langchain==0.1.13
langchain_community==0.0.29
langchain_core==0.1.33
langchain_openai==0.0.8
langchain_text_splitters==0.0.1
FlagEmbedding==1.2.8
unstructured==0.12.6
PyJWT
faiss-gpu  # faiss-cpu for device without gpu
```

```python

cd rag
pip3 install -r requirements.txt

```

## **使用指南** 

### 准备数据

#### 搭建自己的 Vector DB

##### TXT 数据

将需要构建的知识库转化为 Txt 文件放入到 src.data.txt 目录下

##### JSON 数据

构建 QA 对并生成 JSON 文件（多轮对话），放入到 src.data.json 目录下

数据格式如下

```python
[
    {
        "conversation": [
            {
                "input": "（微微皱眉）艾薇，我觉得我在学校的学习压力好大啊，虽然我真的很喜欢我的专业，但最近总是担心自己无法达到自己的期望，这让我有点焦虑。",
                "output": "（微笑）😊 我完全理解你的感受，亲爱的。学习是我们生活的一部分，尤其是在我们热爱的专业里，期待自己做得更好是再正常不过了。你知道吗？这种对成功的渴望其实是一种积极的动力源呢！但是，当它开始影响到我们的心理健康时，我们就需要学会调整和应对了。你可以先试着跟我分享一下，具体是什么样的学习任务或者目标让你感到压力山大呢？"
            },
            {
                "input": "主要是下个月的一场重要考试，我总觉得自己复习得不够充分，而且害怕失败...",
                "output": "💖 噢，明白了。面对重大考试的紧张和担忧是很普遍的现象。首先，我要肯定你对自己的高标准要求，这是你对自己负责的表现。不过，我们可以尝试制定一个更为实际可行的学习计划，将大目标分解成小目标，每天完成一部分，这样既能提升自信心又能减轻焦虑感。同时，也要记得适时放松，合理安排休息时间哦！比如学习45分钟后，可以适当休息10分钟，做些自己喜欢的事情，劳逸结合才是长久之计呢！💪📚\n另外，也可以尝试一些深呼吸、冥想等放松技巧来缓解焦虑情绪。如果你愿意的话，下次咨询我们可以一起练习，看看哪种方式最适合帮助你应对压力。现在，让我们一步步来，先从细化学习计划开始，你觉得怎么样呢？🌸"
            }
        ]
    },
] 
```

会根据准备的数据构建 vector DB，最终会在 data 文件夹下产生名为 vector_db 的文件夹包含 index.faiss 和 index.pkl。如果已经有 vector DB 则会直接加载对应数据库

- 可以直接从 xlab 下载对应 DB（请在rag文件目录下执行对应 code）

```python
# https://openxlab.org.cn/models/detail/Anooyman/EmoLLMRAGTXT/tree/main
git lfs install
git clone https://code.openxlab.org.cn/Anooyman/EmoLLMRAGTXT.git
```

- 也可以从魔塔社区下载对应数据集
  
```python
# https://www.modelscope.cn/datasets/Anooyman/EmoLLMRAGTXT/summary
git clone https://www.modelscope.cn/datasets/Anooyman/EmoLLMRAGTXT.git
```


### 配置 config 文件

根据需要改写 config.config 文件：

```python

# 存放所有 model
model_dir = os.path.join(base_dir, 'model')

# embedding model 路径以及 model name
embedding_path = os.path.join(model_dir, 'embedding_model')
embedding_model_name = 'BAAI/bge-small-zh-v1.5'


# rerank model 路径以及 model name
rerank_path = os.path.join(model_dir, 'rerank_model')
rerank_model_name = 'BAAI/bge-reranker-large'


# select num: 代表rerank 之后选取多少个 documents 进入 LLM
select_num = 3

# retrieval num： 代表从 vector db 中检索多少 documents。（retrieval num 应该大于等于 select num）
retrieval_num = 10

# 智谱 LLM 的 API key。目前 demo 仅支持智谱 AI api 作为最后生成
glm_key = ''

# Prompt template: 定义
prompt_template = """
	你是一个拥有丰富心理学知识的温柔邻家温柔大姐姐艾薇，我有一些心理问题，请你用专业的知识和温柔、可爱、俏皮、的口吻帮我解决，回复中可以穿插一些可爱的Emoji表情符号或者文本符号。\n

	根据下面检索回来的信息，回答问题。

	{content}

	问题：{query}
"""
```

### 本地调用

*注意*
由于 RAG code 已经集成到 `web_internlm2.py` 中，import 路径不再适用于本地调用
因此需要如下调整对应 import 路径

- src/data_processing.py
```python
#from rag.src.config.config import (
#    embedding_path,
#    embedding_model_name,
#    doc_dir, qa_dir,
#    knowledge_pkl_path,
#    data_dir,
#    vector_db_dir,
#    rerank_path,
#    rerank_model_name,
#    chunk_size,
#    chunk_overlap
#)
from config.config import (
    embedding_path,
    embedding_model_name,
    doc_dir, qa_dir,
    knowledge_pkl_path,
    data_dir,
    vector_db_dir,
    rerank_path,
    rerank_model_name,
    chunk_size,
    chunk_overlap
)
```

- src/pipeline.py
```python
#from rag.src.data_processing import Data_process
#from rag.src.config.config import prompt_template 

from data_processing import Data_process
from config.config import prompt_template 
```

修改 import 路径之后通过以下 code 执行

```python
cd rag/src
python main.py
```


## **数据集**

- 经过清洗的QA对: 每一个QA对作为一个样本进行 embedding
- 经过清洗的对话: 每一个对话作为一个样本进行 embedding
- 经过筛选的TXT文本
	- 直接对TXT文本生成embedding (基于token长度进行切分)
	- 过滤目录等无关信息后对TXT文本生成embedding (基于token长度进行切分)
	- 过滤目录等无关信息后, 对TXT进行语意切分生成embedding
	- 按照目录结构对TXT进行拆分，构架层级关系生成embedding

数据集合构建的详情，请参考 [qa_generation_README](https://github.com/SmartFlowAI/EmoLLM/blob/ccfa75c493c4685e84073dfbc53c50c09a2988e3/scripts/qa_generation/README.md)

## **相关组件**

这里我们提供了BGE和BCEmbedding两种组合方式，更加推荐性能更加优异的BGE

### [BGE Github](https://github.com/FlagOpen/FlagEmbedding)

- [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5): embedding 模型，用于构建 vector DB
- [BAAI/bge-reranker-large](https://huggingface.co/BAAI/bge-reranker-large): rerank 模型，用于对检索回来的文章段落重排

### [BCEmbedding](https://github.com/netease-youdao/BCEmbedding?tab=readme-ov-file)

- [bce-embedding-base_v1](https://hf-mirror.com/maidalun1020/bce-embedding-base_v1): embedding 模型，用于构建 vector DB
- [bce-reranker-base_v1](https://hf-mirror.com/maidalun1020/bce-reranker-base_v1): rerank 模型，用于对检索回来的文章段落重排

### [Langchain](https://python.langchain.com/docs/get_started)

LangChain 是一个开源框架，用于构建基于大型语言模型（LLM）的应用程序。LangChain 提供各种工具和抽象，以提高模型生成的信息的定制性、准确性和相关性。

### [FAISS](https://faiss.ai/)

Faiss是一个用于高效相似性搜索和密集向量聚类的库。它包含的算法可以搜索任意大小的向量集。由于langchain已经整合过FAISS，因此本项目中不在基于原生文档开发[FAISS in Langchain](https://python.langchain.com/docs/integrations/vectorstores/faiss)


### [RAGAS](https://github.com/explodinggradients/ragas) (TODO)

RAG的经典评估框架，通过以下三个方面进行评估:

- Faithfulness: 给出的答案应该是以给定上下文为基础生成的。
- Answer Relevance: 生成的答案应该可以解决提出的实际问题。
- Context Relevance: 检索回来的信息应该是高度集中的，尽量少的包含不相关信息。

后续增加了更多的评判指标，例如：context recall 等


## **方案细节**

### RAG具体流程

- 根据数据集构建 vector DB
- 对用户输入的问题进行 embedding
- 基于 embedding 结果在向量数据库中进行检索
- 对召回数据重排序
- 依据用户问题和召回数据生成最后的结果

**Note**: 当用户选择使用RAG时才会进行上述流程

### 后续增强

- 将RAGAS评判结果加入到生成流程中。例如，当生成结果无法解决用户问题时，需要重新生成
- 增加web检索以处理vector DB中无法检索到对应信息的问题
- 增加多路检索以增加召回率。即根据用户输入生成多个类似的query进行检索


