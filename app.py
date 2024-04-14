import os

#model = "EmoLLM_aiwei"
model = "EmoLLM_Model"

if model == "EmoLLM_aiwei":
    os.system("python download_model.py ajupyter/EmoLLM_aiwei")
    os.system('streamlit run web_demo-aiwei.py --server.address=0.0.0.0 --server.port 7860')
elif model == "EmoLLM_Model":
    os.system("python download_model.py jujimeizuo/EmoLLM_Model")
    os.system('streamlit run web_internlm2.py --server.address=0.0.0.0 --server.port 7860')
else:
    print("Please select one model")

