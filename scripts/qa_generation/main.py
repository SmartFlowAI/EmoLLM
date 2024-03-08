import os
import json
from tqdm import tqdm
from datetime import datetime

from config.config import result_dir
from model.qwen import call_qwen_single_turn
from util.logger import get_logger
from util.data_loader import get_file_list, get_txt_content, capture_qa

logger = get_logger()

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
    for file_name in file_list:
        contents = get_txt_content(file_name)
        storage_list = []
        
        file_name = file_name.split('/')[-1]
        storage_jsonl_path = os.path.join(
            result_dir, f'{current_time}-{file_name}-{model_name}.jsonl')
        logger.info(f'The generated QA will be stored in {storage_jsonl_path}.')
        
        for content in tqdm(contents):
            response = model_caller(content)
            # print(response) # 打印输出
            captured_qa = capture_qa(response)
            # print(captured_qa) # 打印QA对
            if captured_qa is None:
                continue
            
            storage_list.extend(captured_qa)
            storage_counter += 1
            if storage_counter % interval == 0:
                storage_counter = 0
                with open(storage_jsonl_path, 'a', encoding='utf-8') as f:
                    for item in storage_list:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                    storage_list = []
    
        # 如果有剩余，存入
        if storage_list:
            with open(storage_jsonl_path, 'a', encoding='utf-8') as f:
                for item in storage_list:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
                storage_list = []


if __name__ == '__main__':

    # 创建generated文件夹
    os.makedirs('./data/generated', exist_ok=True)
    generate_qa()
