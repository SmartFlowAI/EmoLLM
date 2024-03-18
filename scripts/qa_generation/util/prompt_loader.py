from config.config import system_prompt_file_path


def load_system_prompt() -> str:
    with open(system_prompt_file_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    return system_prompt
