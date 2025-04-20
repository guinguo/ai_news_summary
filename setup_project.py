#!/usr/bin/env python3
"""
项目初始化脚本，用于创建项目的目录结构和基本文件
"""
import os
import sys
from pathlib import Path


def create_directory(path):
    """创建目录"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"创建目录: {path}")
    except Exception as e:
        print(f"创建目录失败 {path}: {e}")
        sys.exit(1)


def create_file(path, content=""):
    """创建文件"""
    try:
        # 确保父目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 创建文件并写入内容
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"创建文件: {path}")
    except Exception as e:
        print(f"创建文件失败 {path}: {e}")
        sys.exit(1)


def setup_project():
    """设置项目目录结构"""
    # 获取项目根目录
    base_dir = Path(__file__).resolve().parent

    # 创建主要目录
    directories = [
        "config",
        "core/crawler",
        "core/crawler/site_crawlers",
        "core/parser",
        "core/parser/site_parsers",
        "core/ai",
        "core/ai/providers",
        "core/storage",
        "core/storage/providers",
        "utils",
        "data/output",
        "logs",
        "tests",
    ]

    for directory in directories:
        create_directory(os.path.join(base_dir, directory))

    # 创建__init__.py文件
    init_py_dirs = [
        "config",
        "core",
        "core/crawler",
        "core/crawler/site_crawlers",
        "core/parser",
        "core/parser/site_parsers",
        "core/ai",
        "core/ai/providers",
        "core/storage",
        "core/storage/providers",
        "utils",
        "tests",
    ]

    for directory in init_py_dirs:
        create_file(os.path.join(base_dir, directory, "__init__.py"),
                    '"""{}模块"""'.format(directory.replace("/", ".")))

    # 创建基本文件
    create_file(os.path.join(base_dir, "main.py"), """#!/usr/bin/env python3
\"\"\"
AI新闻摘要系统主入口
\"\"\"
import logging
import sys
from utils.logger import setup_logger
from core.crawler.crawler_factory import CrawlerFactory
from core.ai.ai_factory import AIFactory
from core.storage.storage_factory import StorageFactory
from config.site_config import SITES


def main():
    \"\"\"主函数\"\"\"
    # 设置日志
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("AI新闻摘要系统启动")

    try:
        # 初始化存储
        storage = StorageFactory.create_storage("file")

        # 初始化AI服务
        ai_service = AIFactory.create_ai_service("openai")

        # 爬取每个站点的新闻
        for site_config in SITES:
            logger.info(f"开始处理站点: {site_config['name']}")

            # 创建爬虫
            crawler = CrawlerFactory.create_crawler(site_config)

            # 爬取新闻
            news_list = crawler.crawl()

            for news in news_list:
                # 使用AI进行内容摘要
                summary = ai_service.summarize(news['title'], news['content'])

                # 存储摘要
                if summary:
                    news['summary'] = summary
                    storage.save(news)

        logger.info("所有站点处理完成")

    except Exception as e:
        logger.error(f"系统运行出错: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
""")

    create_file(os.path.join(base_dir, "run.py"), """#!/usr/bin/env python3
\"\"\"
运行脚本，支持定时运行和手动运行
\"\"\"
import sys
import time
import schedule
import logging
import argparse
from utils.logger import setup_logger
from main import main


def setup_scheduler(interval):
    \"\"\"设置定时任务\"\"\"
    logger = logging.getLogger(__name__)
    logger.info(f"设置定时任务，每 {interval} 小时运行一次")

    schedule.every(interval).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    # 设置日志
    setup_logger()
    logger = logging.getLogger(__name__)

    # 命令行参数
    parser = argparse.ArgumentParser(description='AI新闻摘要系统')
    parser.add_argument('--schedule', type=int, help='定时运行间隔（小时）')
    args = parser.parse_args()

    try:
        if args.schedule:
            setup_scheduler(args.schedule)
        else:
            sys.exit(main())
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        logger.error(f"运行出错: {e}")
        sys.exit(1)
""")

    # 创建utils文件
    create_file(os.path.join(base_dir, "utils", "logger.py"), """\"\"\"
日志工具模块
\"\"\"
import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_FILE, LOG_DIR


def setup_logger():
    \"\"\"设置日志\"\"\"
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
""")

    create_file(os.path.join(base_dir, "utils", "helpers.py"), """\"\"\"
辅助函数模块
\"\"\"
import os
import re
import json
from datetime import datetime
from urllib.parse import urlparse


def normalize_url(url):
    \"\"\"
    标准化URL，去除查询参数
    \"\"\"
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def clean_text(text):
    \"\"\"
    清理文本，去除多余空白字符
    \"\"\"
    if not text:
        return ""
    # 替换多个连续空白字符为单个空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_file_path(base_dir, source_name, file_type="json"):
    \"\"\"
    获取文件保存路径
    \"\"\"
    # 安全的文件名
    safe_name = re.sub(r'[^\w\-_.]', '_', source_name)
    date_str = datetime.now().strftime("%Y%m%d")
    return os.path.join(base_dir, f"{safe_name}_{date_str}.{file_type}")


def save_json(data, file_path):
    \"\"\"
    保存JSON数据
    \"\"\"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path):
    \"\"\"
    加载JSON数据
    \"\"\"
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
""")

    print("\n项目目录结构创建完成！")
    print("接下来，您可以运行以下命令完成项目设置：")
    print("1. pip install -r requirements.txt  # 安装依赖")
    print("2. python setup_project.py          # 创建项目结构")
    print("3. python main.py                   # 运行主程序")


if __name__ == "__main__":
    setup_project()