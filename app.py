import os

os.system('streamlit run web_demo-Llama3.py --server.address=0.0.0.0 --server.port 7860')

model = "EmoLLM_aiwei"
# model = "EmoLLM_Model"
# model = "Llama3_Model"

if model == "EmoLLM_aiwei":
    os.system("python download_model.py ajupyter/EmoLLM_aiwei")
    os.system('streamlit run web_demo-aiwei.py --server.address=0.0.0.0 --server.port 7860')
elif model == "EmoLLM_Model":
    os.system("python download_model.py jujimeizuo/EmoLLM_Model")
    os.system('streamlit run web_internlm2.py --server.address=0.0.0.0 --server.port 7860')
elif model == "Llama3_Model":
    os.system("python download_model.py chg0901/EmoLLM-Llama3-8B-Instruct3.0")
    os.system('streamlit run web_demo_Llama3.py --server.address=0.0.0.0 --server.port 7860')
else:
    print("Please select one model")
