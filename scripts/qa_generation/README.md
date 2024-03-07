# QA Generation Pipeline



## 1. 使用方法

检查 `requirements.txt` 中的依赖是否满足。

而后，在 `config/config.py` 配置所需的 API KEY，从 `main.py` 启动即可。生成的 QA 对会以 jsonl 的格式存在 `data/generated` 下。

可以调整 `system_prompt`，增强生成的多样性和稳定性。

### 1.1 API KEY 获取方法

目前仅包含了 qwen。

#### 1.1.1 Qwen

前往[模型服务灵积-API-KEY管理 (aliyun.com)](https://dashscope.console.aliyun.com/apiKey)，点击”创建新的 API-KEY“，将获取的 API KEY 填至 `config/config.py` 中的 `DASHSCOPE_API_KEY` 即可。



## 2. 注意事项

### 2.1 系统提示 System Prompt

注意，目前的解析方案是基于模型会生成 markdown 包裹的 json 块的前提的，更改 system prompt 时需要保证这一点不变。

### 2.2 滑动窗口 Sliding Window

滑动窗口的 `window_size` 和 `overlap_size` 都可以在 `util/data_loader.py` 中的 `get_txt_content` 函数中更改。目前是按照句子分割的滑动窗口。

### 2.3 书本文件格式 Corpus Format

目前仅支持了 txt 格式，可以将清洗好的书籍文本放在 `data` 文件夹下，程序会递归检索该文件夹下的所有 txt 文件。



## TODO

1. 支持更多模型（Gemini、GPT、ChatGLM……）
2. 支持多线程调用模型
3. 支持更多文本格式（PDF……）
4. 支持更多切分文本的方式
