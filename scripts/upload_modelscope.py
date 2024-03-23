
from modelscope.hub.api import HubApi

YOUR_ACCESS_TOKEN = '' #输入你的modelscope access token

api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
api.push_model(
            model_id="zealot5209/EmoLLM-Scientist",  #your_name/model_id
                model_dir="./merged" # 本地模型目录，要求目录中必须包含configuration.json
                )
