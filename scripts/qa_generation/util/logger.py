from loguru import logger

from config.config import log_file_path

def get_logger():
    return logger

logger.add(log_file_path, rotation="500 MB")

logger.configure(
    handlers=[
        dict(sink=log_file_path, rotation="500 MB", format="{time} {level} {message}"),
    ]
)
