import time
import jwt
from langchain_openai import ChatOpenAI
from config.config import glm_key


def get_glm(
        model_name='glm-4',
        api_base="https://open.bigmodel.cn/api/paas/v4",
        temprature=0.7,
        streaming=False,
    ):
    """

    """

    llm = ChatOpenAI(
        model_name=model_name,
        openai_api_base=api_base,
        openai_api_key=generate_token(glm_key),
        streaming=streaming,
        temperature=temprature
    )

    return llm 

def generate_token(apikey: str, exp_seconds: int=100):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)
 
    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
 
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )
