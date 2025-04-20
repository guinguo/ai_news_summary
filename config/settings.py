"""
全局设置模块，定义系统运行所需的全局配置
"""
import os
import logging
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 日志配置
LOG_LEVEL = logging.INFO
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'ai_news_summary.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 数据存储路径
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# 爬虫配置
CRAWLER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 代理配置 (可选)
PROXY = None  # 例如: 'http://user:pass@proxy.example.com:8080'

# 爬取间隔时间 (秒)
CRAWL_DELAY = 2

# AI提供商配置
DEFAULT_AI_PROVIDER = 'openai'  # 'openai', 'grok', 'gemini', 'qwen'

# 摘要长度限制
TITLE_MAX_LENGTH = 50
CONTENT_MAX_LENGTH = 500

# 爬取层级
MAX_CRAWL_DEPTH = 2
MAX_NEWS_PER_SITE = 5  # 每个网站最多爬取的新闻数量

# 创建必要的目录
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)