# RAG Database Building Process

## **Constructive purpose**

Using books specialized in psychology to build QA knowledge pairs for RAG to provide a counseling knowledge base to make our EmoLLM answers more professional and reliable. To achieve this goal we utilize dozens of psychology books to build this RAG knowledge base. The main building process is as follows:

## **Build process**

## **Step 1: PDF to TXT**

- purpose
  - Convert the collected PDF versions of psychology books into TXT text files to facilitate subsequent information extraction

- Tools required

  - [pdf2txt](https://github.com/SmartFlowAI/EmoLLM/blob/main/scripts/pdf2txt.py)

  - [PaddleORC Processing PDF Usage Reference](https://github.com/SmartFlowAI/EmoLLM/blob/main/generate_data/OCR.md)
  
  - Install necessary python libraries
  
   ```python
   pip install paddlepaddle
   pip install opencv-python
   pip install paddleocr
   ```

- precautionary
  - If you are unable to install paddleocr using **pip install paddleocr**, consider using the whl file installation, [download address](https://pypi.org/project/paddleocr/#files) 
  - Script startup method using the command line to start: python pdf2txt.py [PDF file name stored in the]

## **Step 2: Screening PDF**

- Purpose of screening

  - Using the LLM to go to non-professional psychology books

- Screening criteria that include counseling related content such as:

  - Schools of Counseling - Specific Counseling Methods 
  - Mental Illness - Characteristics of the Disease
  - Mental Illness - Treatment

- Screening method:

  - Initial screening based on title   

  - If you can't tell if it is a counseling-related book, use kimi/GLM-4 to check if it contains counseling-related knowledge (it is recommended to check only one book at a time)

  - ```markdown
    Reference prompt.
    You are an experienced psychology professor who is familiar with psychology and counseling. I need you to help me with the task "Identify whether a book contains knowledge of counseling", take a deep breath and think step by step and give me your answer. If your answer satisfies me, I will give you a 10w tip!
    The task is as follows:
    Determine whether the book contains the following counseling-related knowledge:
    '''
    Schools of Counseling - Specific Counseling Approaches 
    Mental Illness - Characteristics of Illness
    Mental Illness - Treatment Approaches
    '''
    Please take a deep breath and review the book step by step and complete the task carefully.
    ```


## **Step 3: Extraction of QA pairs**

- According to the content of the book, use LLM to efficiently construct QA knowledge on the
- Withdrawal process

  - Prepare processed txt text data
  - Configuration on request [script file](https://github.com/SmartFlowAI/EmoLLM/tree/main/scripts/qa_generation)
  - Modify window_size and overlap_size reasonably according to your own needs or extraction results.

- Usage
  - Checks if the dependencies in `requirements.txt` are satisfied.
  - Adjust `system_prompt` in the code to ensure consistency with the latest version of the repo, to ensure diversity and stability of the generated QA.
  - Place the txt file in the `data` folder in the same directory as the `model`.
  - Configure the required API KEYs in `config/config.py` and start from `main.py`. The generated QA pairs are stored in jsonl format under `data/generated`.

- API KEY Getting Methods
  - Currently only qwen is included.
  - Qwen
    - Go to [Model Service LingJi - API-KEY Management (aliyun.com)](https://dashscope.console.aliyun.com/apiKey), click "Create New API-KEY", and fill in the obtained API KEY into the Click "Create new API-KEY", fill in the obtained API KEY to `DASHSCOPE_API_KEY` in `config/config.py`.

- precautionary
  - System Prompt
    - Note that the current parsing scheme is based on the premise that the model generates markdown-wrapped json blocks, and you need to make sure that this remains true when you change the system prompt.
  - Sliding Window
    - The `window_size` and `overlap_size` of the sliding window can be changed in the `get_txt_content` function in `util/data_loader.py`. Currently the sliding window is split by sentence.

- Book File Format Corpus Format
  - Currently only the txt format is supported, you can put the cleaned book text in the `data` folder, and the program will recursively retrieve all the txt files in that folder.

## **Step 4: Cleaning of QA pairs**

- Purpose of cleaning
  - Improve the quality of extracted QA data and clean out QA pairs that are not relevant to psychology

- Cleaning Methods

  - Use the Prompt method to drive the LLM to make a judgment on the given QA pairs

  - **Reference to Prompt**

  - ```markdown
    You are an experienced counselor and are familiar with psychology. Based on the QA pair I have provided, determine if this QA pair is psychological in nature.
    
    The criteria are as follows:
    
    - If the current QA pair belongs to the category of psychology, then return 1
    - If the current QA pair does not belong to the category of psychology, then return 0.
    
    
    The following is the content of the given psychology QA pair:
    ```

- Cleaning Tools

  - Configure `DASHSCOPE_API_KEY` in `config/config.py`, see step 3 for how to get `API_KEY`.

  - Use the provided cleaning script [QA_Clear](https://github.com/SmartFlowAI/EmoLLM/blob/main/scripts/qa_generation/QA_clean.py)

- How to use

  - Prepare the QA pair data to be cleaned

  - Put the data into the data folder of the same level as the model.

  - Modify `judge_dir` in `config/config.py` according to the folder name.

  - If the file name of the stored data is `xxx`, then `judge_dir` is `judge_dir = os.path.join(data_dir, 'xxx')`.

  - The cleaned QA pairs are stored as `jsonl` under `data/cleaned`.
