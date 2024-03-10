import os
import json
import time
from tqdm import tqdm
import concurrent.futures
from datetime import datetime
import numpy as np

from config.config import result_dir, storage_interval, window_size, overlap_size, multi_process_num
from model.qwen import call_qwen_single_turn
from util.logger import get_logger
from util.data_loader import get_file_list, get_txt_content, capture_qa, merge_sub_qa_generation, save_to_file

logger = get_logger()

"""
每个线程产生 QA 对以及存储到子文件中
"""
def single_thread_generate(thread_num, interval, model_caller, storage_jsonl_path, contents):

    storage_counter = 0
    storage_list = []

    for content in tqdm(contents):
        try:
            response = model_caller(content)
            captured_qa = capture_qa(response)

            if captured_qa is None:
                continue

            storage_list.extend(captured_qa)
            storage_counter += 1

            if storage_counter % interval == 0:
                save_to_file(storage_jsonl_path, storage_list)
                storage_counter = 0
                storage_list = []
        except Exception as exc:
            logger.error("QA generation error : %s" % (exc))

    if storage_list:
        save_to_file(storage_jsonl_path, storage_list)
        storage_list = []
   
 
"""
生成 QA 对
model_name: 可调用的模型名称，暂时只实现了 qwen
interval: 存储间隔，即每隔多少条存一次文件，过密的间隔会增大 IO 开销
"""
def generate_qa(
    model_name: str = 'qwen',
    interval: int = 10,
):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if model_name == 'qwen':
        model_caller = call_qwen_single_turn
    else:
        logger.warning('This model is currently not supported and will call the default model - qwen.')
        model_caller = call_qwen_single_turn
        model_name = 'qwen'
    
    logger.info(f'The called model is: {model_name}.')
    logger.info(f'The storage interval is: {interval}.')

    file_list = get_file_list()
    storage_counter = 0
    storage_list = []
    for file_path in file_list:
        contents = get_txt_content(file_path, window_size=window_size, overlap_size=overlap_size)
        storage_list = []
        
        _, file_name = os.path.split(file_path)
        storage_jsonl_path = os.path.join(
            result_dir, f'{current_time}-{file_name}-{model_name}.jsonl')
        logger.info(f'The generated QA will be stored in {storage_jsonl_path}.')

        # 基于并发个数切分 contents 内容
        contents_array = np.array(contents)
        chunks = np.array_split(contents_array, multi_process_num)

        # 构建并发参数 list
        parameters_list = list()
        for thread_num, chunk in enumerate(chunks):
            parameters_list.append(
                    [thread_num, interval, model_caller, storage_jsonl_path + f'-{thread_num}', list(chunk)]
            )

        # 并发生成 QA 对
        with concurrent.futures.ThreadPoolExecutor(max_workers=multi_process_num) as executor:
            # 创建一个Future列表，它们将对应每个worker_function的结果
            futures = [executor.submit(single_thread_generate, *parameters) for parameters in parameters_list]
        
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    logger.error("Thread generated an exception: %s" % (exc))

        merge_sub_qa_generation(result_dir, storage_jsonl_path)

if __name__ == '__main__':

    # 创建generated文件夹
    os.makedirs('./data/generated', exist_ok=True)
    generate_qa(interval=storage_interval)
