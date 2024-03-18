import os

cur_dir = os.path.dirname(os.path.abspath(__file__))                # config
src_dir = os.path.dirname(cur_dir)                                  # src
base_dir = os.path.dirname(src_dir)                                 # base
model_repo = 'ajupyter/EmoLLM_aiwei'

# model
model_dir = os.path.join(base_dir, 'model')                         # model
embedding_path = os.path.join(model_dir, 'gte-small-zh')            # embedding
llm_path = os.path.join(model_dir, 'pythia-14m')                    # llm

# data
data_dir = os.path.join(base_dir, 'data')                           # data
knowledge_json_path = os.path.join(data_dir, 'knowledge.json')      # json
knowledge_pkl_path = os.path.join(data_dir, 'knowledge.pkl')        # pkl
doc_dir = os.path.join(data_dir, 'txt')   
qa_dir = os.path.join(data_dir, 'json')   

# log
log_dir = os.path.join(base_dir, 'log')                             # log
log_path = os.path.join(log_dir, 'log.log')                         # file

# vector DB
vector_db_dir = os.path.join(data_dir, 'vector_db.pkl')

select_num = 3
retrieval_num = 10