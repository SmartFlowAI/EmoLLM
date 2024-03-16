import dashscope
from http import HTTPStatus
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

from config.config import DASHSCOPE_API_KEY
from util.logger import get_logger
from util.prompt_loader import load_system_prompt, load_wash_prompt


dashscope.api_key = DASHSCOPE_API_KEY

logger = get_logger()


def call_qwen_single_turn(query: str) -> str:
    messages = [
        {
            'role': Role.SYSTEM,
            'content': load_system_prompt()
        },
        {
            'role': Role.USER,
            'content': query
        }
    ]
    response = Generation.call(
        model='qwen-max-1201',
        messages=messages,
        result_format='message',
        stream=False,
        incremental_output=False
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]['message']['content']
    else:
        logger.error('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return ""


def call_qwen_Psychology_QA_Pairs(query: str) -> str:
    messages = [
        {
            'role': Role.SYSTEM,
            'content': load_wash_prompt()
        },
        {
            'role': Role.USER,
            'content': query
        }
    ]
    response = Generation.call(
        model='qwen-max-1201',
        messages=messages,
        result_format='message',
        stream=False,
        incremental_output=False
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]['message']['content']
    else:
        logger.error('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return ""
