# QA Generation Pipeline

## 1. Use method

1. Check whether the dependencies in  `requirements.txt` are satisfied.
2. Adjust the `system_prompt`in the code to ensure that it is consistent with the latest version of the repo to ensure the diversity and stability of the generated QA.
3. Put the txt file into the `data` folder in the same directory as `model`.
4. Configure the required API KEY in `config/config.py` and start from `main.py`. The generated QA pairs are stored in the jsonl format under `data/generated`.

### 1.1 API KEY obtaining method

Currently only qwen is included.

#### 1.1.1 Qwen

To[model service spirit product - API - KEY management (aliyun.com)](https://dashscope.console.aliyun.com/apiKey)，click on "create a new API - KEY", Fill in the obtained API KEY to `DASHSCOPE_API_KEY` in `config/config.py`.

## 2. Precautions

### 2.1 The System Prompt is displayed

Note that the current parsing scheme is based on the premise that the model generates json blocks of markdown wraps, and you need to make sure that this remains the case when you change the system prompt.

### 2.2 Sliding Window

Both `window_size` and `overlap_size` of the sliding window can be changed in the `get_txt_content` function in `util/data_loader.py.` Currently it is a sliding window divided by sentence.

### 2.3 Corpus Format

At present, only txt format is supported, and the cleaned book text can be placed under the `data` folder, and the program will recursively retrieve all txt files under the folder.

## TODO

1. Support more models (Gemini, GPT, ChatGLM...)
2. Support multi-threaded call model
3. Support more text formats (PDF...)
4. Support more ways to split text
