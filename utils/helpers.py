"""
辅助函数模块
"""
import os
import re
import json
from datetime import datetime
from urllib.parse import urlparse


def normalize_url(url):
    """
    标准化URL，去除查询参数
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def clean_text(text):
    """
    清理文本，去除多余空白字符
    """
    if not text:
        return ""
    # 替换多个连续空白字符为单个空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_file_path(base_dir, source_name, file_type="json"):
    """
    获取文件保存路径
    """
    # 安全的文件名
    safe_name = re.sub(r'[^\w\-_.]', '_', source_name)
    date_str = datetime.now().strftime("%Y%m%d")
    return os.path.join(base_dir, f"{safe_name}_{date_str}.{file_type}")


def save_json(data, file_path):
    """
    保存JSON数据
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path):
    """
    加载JSON数据
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
