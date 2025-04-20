#!/usr/bin/env python3
"""
AI新闻摘要系统主入口
"""
import logging
import sys
import os
from dotenv import load_dotenv

from utils.logger import setup_logger
from core.crawler.crawler_factory import CrawlerFactory
from core.ai.ai_factory import AIFactory
from core.storage.storage_factory import StorageFactory
from config.site_config import SITES


def load_environment():
    """加载环境变量"""
    # 尝试加载.env文件
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        logging.info(f"已加载环境变量文件: {env_file}")
    else:
        logging.warning(f"环境变量文件不存在: {env_file}")


def main():
    """主函数"""
    # 设置日志
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("AI新闻摘要系统启动")

    # 加载环境变量
    load_environment()

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

        logger.info("所有站点处理处理完成")

        return 0

    except Exception as e:
        logger.error(f"系统运行出错: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
