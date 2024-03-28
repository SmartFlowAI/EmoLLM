import os

"""
文件夹路径
"""
cur_dir = os.path.dirname(os.path.abspath(__file__))                        # config
base_dir = os.path.dirname(cur_dir)                                         # base

# model
model_dir = os.path.join(base_dir, 'model')                                 # model

# data
data_dir = os.path.join(base_dir, 'data')
clean_dir = os.path.join(data_dir, 'cleaned')
judge_dir = os.path.join(data_dir, 'generated')
result_dir = os.path.join(data_dir, 'generated')                            # result

# log
log_dir = os.path.join(base_dir, 'log')                                     # log
log_file_path = os.path.join(log_dir, 'log.log')                            # file

# system prompt
# Prompt内容
system_prompt_file_path = os.path.join(base_dir, 'system_prompt_v2.md')     # system prompt
wash_prompt_file_path = os.path.join(base_dir, 'choose_prompt.md')


"""
环境变量
"""
# api-keys
DASHSCOPE_API_KEY = 'sk-4295ec893e9c413abb0551b85e84f39f'


"""
控制参数
"""
storage_interval = 10
window_size = 8
overlap_size = 2
multi_process_num = 3

