# RAG数据库构建流程

## **构建目的**

利用心理学专业的书籍构建QA知识对，为RAG提供心理咨询知识库，使我们的EmoLLM的回答更加专业可靠。为了实现这个目标我们利用几十本心理学书籍来构建这个RAG知识库。主要的构建流程如下：

## **构建流程**

## **步骤一：PDF to TXT**

- 目的
  - 将收集到的PDF版本的心理学书籍转化为TXT文本文件，方便后续的信息提取。

- 所需工具

  - [pdf2txt](https://github.com/SmartFlowAI/EmoLLM/blob/main/scripts/pdf2txt.py)

  - [PaddleORC处理PDF用法参考](https://github.com/SmartFlowAI/EmoLLM/blob/main/generate_data/OCR.md)
  
  - 安装必要的python库
  
   ```python
   pip install paddlepaddle
   pip install opencv-python
   pip install paddleocr
   ```

- 注意
  - 如果无法使用**pip install paddleocr**安装paddleocr，可以考虑采用whl文件安装，[下载地址](https://pypi.org/project/paddleocr/#files) 
  - 脚本启动方式采用命令行启动：python  pdf2txt.py  [PDF存放的文件名]

## **步骤二：筛选PDF**

- 筛选目的

  - 利用LLM去除非专业心理学书籍

- 筛选标准，包含心理咨询相关内容，如：

  - 心理咨询流派 - 具体咨询方法 
  - 心理疾病 - 疾病特征
  - 心理疾病 - 治疗方法

- 筛选方式：

  - 根据标题初筛   

  - 若无法判断属于心理咨询相关书籍，利用kimi/GLM-4查询是否包含心理咨询相关知识（建议一次仅查询一本书）

  - ```markdown
    参考prompt:
    你是一位经验丰富的心理学教授，熟悉心理学知识和心理咨询。我需要你协助我完成"识别书籍是否包含心理咨询知识"任务，请深呼吸并一步步思考，给出你的答案。如果你的答案让我满意，我将给你10w小费！
    具体任务如下：
    判断该书籍中是否包含以下心理咨询相关知识：
    '''
    心理咨询流派 - 具体咨询方法 
    心理疾病 - 疾病特征
    心理疾病 - 治疗方法
    '''
    请深呼吸并一步步查看该书籍，认真完成任务。
    ```


## **步骤三：提取QA对**

- 根据书籍内容，利用LLM高效构造QA知识对
- 提取流程

  - 准备处理好的txt文本数据
  - 按要求配置[脚本文件](https://github.com/SmartFlowAI/EmoLLM/tree/main/scripts/qa_generation)
  - 根据自己的需求或者提取的结果合理修改window_size和overlap_size

- 使用方法
  - 检查 `requirements.txt` 中的依赖是否满足。
  - 调整代码中 `system_prompt`，确保与repo最新版本一致，保证生成QA的多样性和稳定性。
  - 将txt文件放到与 `model`同级目录 `data`文件夹中.
  - 在 `config/config.py` 配置所需的 API KEY，从 `main.py` 启动即可。生成的 QA 对会以 jsonl 的格式存在 `data/generated` 下。

- API KEY 获取方法
  - 目前仅包含了 qwen。
  - Qwen
    - 前往[模型服务灵积-API-KEY管理 (aliyun.com)](https://dashscope.console.aliyun.com/apiKey)，点击”创建新的 API-KEY“，将获取的 API KEY 填至 `config/config.py` 中的 `DASHSCOPE_API_KEY` 即可。

- 注意事项
  - 系统提示 System Prompt
    - 注意，目前的解析方案是基于模型会生成 markdown 包裹的 json 块的前提的，更改 system prompt 时需要保证这一点不变。
  - 滑动窗口 Sliding Window
    - 滑动窗口的 `window_size` 和 `overlap_size` 都可以在 `util/data_loader.py` 中的 `get_txt_content` 函数中更改。目前是按照句子分割的滑动窗口。

- 书本文件格式 Corpus Format
  - 目前仅支持了 txt 格式，可以将清洗好的书籍文本放在 `data` 文件夹下，程序会递归检索该文件夹下的所有 txt 文件。

## **步骤四：清洗QA对**

- 清洗目的

  - 提高提取的QA数据质量，清理掉与心理学无关的QA对

- 清洗方法

  - 使用Prompt方法，驱动LLM对给出的QA对进行判断

  - **参考Prompt**

  - ```markdown
    你是一名经验丰富的心理咨询师，熟悉心理学相关知识。根据我提供的 QA 对，来判断这个 QA 对是否属于心理学范畴。
    
    标准如下：
    
    - 若当前 QA 对属于心理学范畴，则返回1
    - 若当前 QA 对不属于心理学范畴，则返回0
    
    
    以下是给定的心理学 QA 对内容：
    ```

- 清洗工具
  - 配置`config/config.py` 中的 `DASHSCOPE_API_KEY`,`API_KEY`获取方法见步骤三
  - 使用提供的清洗脚本[QA_Clear](https://github.com/SmartFlowAI/EmoLLM/blob/main/scripts/qa_generation/QA_clean.py)

- 使用方法
  - 准备好需要清洗的 QA 对数据
  - 将该数据放进 model 同级 data 文件夹下
  - 根据文件夹名去修改 `config/config.py` 中的 `judge_dir`。
  - 如存储数据的文件名为`xxx`，则`judge_dir`是 `judge_dir = os.path.join(data_dir, 'xxx')`
  - 清洗完的 QA 对会以 `jsonl` 的格式存在 `data/cleaned` 下
