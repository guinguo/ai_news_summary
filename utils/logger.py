"""
日志工具模块
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE, LOG_DIR


def setup_logger():
    """设置日志"""
    # 创建日志目录
    os.makedirs(LOG_DIR, exist_ok=True)

    # 设置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # 创建文件处理器
    file_handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # 添加处理器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
