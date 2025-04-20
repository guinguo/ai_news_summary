"""
爬虫工厂，负责创建不同类型的爬虫
"""
import logging
from typing import Dict, Any

from core.crawler.base_crawler import BaseCrawler
from core.crawler.site_crawlers.common_crawler import CommonCrawler

logger = logging.getLogger(__name__)


class CrawlerFactory:
    """爬虫工厂类，用于创建不同类型的爬虫"""

    @staticmethod
    def create_crawler(site_config: Dict[str, Any]) -> BaseCrawler:
        """
        根据站点配置创建对应的爬虫实例

        Args:
            site_config: 站点配置信息

        Returns:
            爬虫实例
        """
        crawler_type = site_config.get("crawler_type", "common")

        logger.info(f"创建爬虫 - {site_config['name']} - 类型: {crawler_type}")

        # 根据crawler_type创建对应的爬虫
        if crawler_type == "common":
            return CommonCrawler(site_config)

        # 如果需要自定义爬虫，可以在这里添加更多的条件判断
        # elif crawler_type == "custom_type":
        #     return CustomCrawler(site_config)

        else:
            logger.warning(f"未知爬虫类型 {crawler_type}，使用通用爬虫")
            return CommonCrawler(site_config)