from config.config import system_prompt_file_path
from config.config import wash_prompt_file_path


def load_system_prompt() -> str:
    with open(system_prompt_file_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    return system_prompt


def load_wash_prompt() -> str:
    with open(wash_prompt_file_path, 'r', encoding='utf-8') as f:
        wash_prompt = f.read()
    return wash_prompt
