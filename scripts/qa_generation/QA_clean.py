import os
import json
import time
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import numpy as np

from config.config import result_dir, clean_dir, storage_interval, window_size, overlap_size, multi_process_num
from model.qwen import call_qwen_single_turn, call_qwen_Psychology_QA_Pairs
from util.logger import get_logger
from util.data_loader import get_jsonl_file_paths, get_file_list, get_QA_pairs, get_txt_content, capture_qa, merge_sub_qa_generation, save_to_file

logger = get_logger()


def single_thread_generate(thread_num, interval, model_caller, storage_jsonl_path, contents):

    storage_counter = 0
    judge_list = []
    for content in tqdm(contents):
        # print('content: ', content)
        try:
            # model_caller 函数的作用是调用某个预训练的问答生成模型，传递输入内容 content 给模型，然后获取模型的输出 response
            response = model_caller(content)
            # print('response: ', response)

            if response == '1':
                content = json.loads(content)
                judge_list.append(content)
                storage_counter += 1
            else:
                continue

            # 在达到指定的 interval 后，将 storage_list 中的内容保存到指定的文件 storage_jsonl_path 中
            if storage_counter % interval == 0:
                save_to_file(storage_jsonl_path, judge_list)
                storage_counter = 0
                judge_list = []

        except Exception as exc:
            logger.error("QA generation error : %s" % (exc))

    # 最后，如果 storage_list 中还有剩余内容，也会将其保存到文件中。
    if judge_list:
        save_to_file(storage_jsonl_path, judge_list)
        judge_list = []
   
 
"""
生成 QA 对
model_name: 可调用的模型名称，暂时只实现了 qwen
interval: 存储间隔，即每隔多少条存一次文件，过密的间隔会增大 IO 开销
"""
def clean_qa(
    model_name: str = 'qwen',
    interval: int = 10,
):
    # current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if model_name == 'qwen':
        model_caller = call_qwen_Psychology_QA_Pairs
    else:
        logger.warning('This model is currently not supported and will call the default model - qwen.')
        model_caller = call_qwen_Psychology_QA_Pairs
        model_name = 'qwen'
    
    logger.info(f'The called model is: {model_name}.')
    logger.info(f'The storage interval is: {interval}.')

    file_lists = get_jsonl_file_paths()  # 数据整合文件夹下所有.jsonl文件的地址

    for file_path in file_lists:
        # 一个jsonl文件的所有QA Pairs
        contents = get_QA_pairs(file_path)
        # print(contents)

        file_name = os.path.basename(file_path)
        print(file_name)
        storage_jsonl_path = os.path.join(
            clean_dir, f'{file_name}')

        logger.info(f'The generated QA will be stored in {storage_jsonl_path}.')

        contents_array = np.array(contents)
        chunks = np.array_split(contents_array, multi_process_num)

        # 构建并发参数 list
        parameters_list = list()
        for thread_num, chunk in enumerate(chunks):
            parameters_list.append(
                    [thread_num, interval, model_caller, storage_jsonl_path, list(chunk)]
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=multi_process_num) as executor:
            # 循环调用 single_thread_generate 函数，每次赋予参数 parameters
            futures = [executor.submit(single_thread_generate, *parameters) for parameters in parameters_list]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    logger.error("Thread generated an exception: %s" % (exc))
        
        merge_sub_qa_generation(result_dir, storage_jsonl_path)


if __name__ == '__main__':
    # 创建washed文件夹
    os.makedirs('./data/cleaned', exist_ok=True)
    clean_qa(interval=storage_interval)
