import os

"""
文件夹路径
"""
cur_dir = os.path.dirname(os.path.abspath(__file__))                    # config
base_dir = os.path.dirname(cur_dir)                                     # base

# model
model_dir = os.path.join(base_dir, 'model')                             # model

# data
data_dir = os.path.join(base_dir, 'data')                               # data
result_dir = os.path.join(data_dir, 'generated')                        # result

# log
log_dir = os.path.join(base_dir, 'log')                                 # log
log_file_path = os.path.join(log_dir, 'log.log')                        # file

# system prompt
system_prompt_file_path = os.path.join(base_dir, 'system_prompt.md')    # system prompt


"""
环境变量
"""
# api-keys
DASHSCOPE_API_KEY = 'sk-xxxxxxxx'
