from modelscope.hub.api import HubApi

YOUR_ACCESS_TOKEN = '请从ModelScope个人中心->访问令牌获取'

api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
api.push_model(
    model_id="yourname/your_model_id", 
    model_dir="my_model_dir" # 本地模型目录，要求目录中必须包含configuration.json
)