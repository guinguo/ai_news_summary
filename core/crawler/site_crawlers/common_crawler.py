"""
通用爬虫，适用于大部分网站的爬取
"""
import logging
from typing import List, Dict, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from core.crawler.base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class CommonCrawler(BaseCrawler):
    """通用爬虫实现，适用于大部分标准网站布局"""

    def __init__(self, site_config):
        super().__init__(site_config)
        self.article_selector = site_config.get("article_selector", {})

    def extract_news_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        提取新闻链接和标题

        Args:
            soup: BeautifulSoup对象

        Returns:
            新闻链接列表，每个元素包含title和url
        """
        news_links = []
        list_selector = self.article_selector.get("list", "")
        title_selector = self.article_selector.get("title", "")
        link_selector = self.article_selector.get("link", "")

        if not list_selector:
            # 如果没有定义列表选择器，尝试直接查找链接
            logger.info(f"使用直接链接选择器 - {self.name}")
            link_elements = soup.select(link_selector) if link_selector else []

            for link in link_elements:
                title = link.text.strip()
                url = link.get('href', '')

                if url and title:
                    # 处理相对URL
                    if not url.startswith(('http://', 'https://')):
                        url = urljoin(self.url, url)

                    news_links.append({
                        'title': title,
                        'url': url
                    })

        else:
            # 使用列表选择器
            logger.info(f"使用列表选择器 - {self.name}")
            list_items = soup.select(list_selector)

            for item in list_items:
                # 提取标题
                title_element = item.select_one(title_selector) if title_selector else None
                title = title_element.text.strip() if title_element else ""

                # 提取链接
                if link_selector:
                    link_element = item.select_one(link_selector)
                else:
                    link_element = title_element

                url = link_element.get('href', '') if link_element else ''

                # 处理相对URL
                if url and not url.startswith(('http://', 'https://')):
                    url = urljoin(self.url, url)

                if url and title:
                    news_links.append({
                        'title': title,
                        'url': url
                    })

        logger.info(f"提取到 {len(news_links)} 个新闻链接 - {self.name}")
        return news_links

    def extract_content(self, soup: BeautifulSoup) -> str:
        """
        提取新闻内容

        Args:
            soup: BeautifulSoup对象

        Returns:
            新闻内容
        """
        content_selector = self.article_selector.get("content", "")

        if not content_selector:
            # 如果没有指定内容选择器，尝试一些常用的选择器
            common_selectors = [
                "article", ".article", ".article-content", ".content",
                "#content", ".post-content", ".entry-content", ".news-content"
            ]

            for selector in common_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    return content_element.get_text(strip=True)

            # 如果以上都没找到，返回body的内容，并截取一部分
            body_text = soup.body.get_text(strip=True)
            return body_text[:2000]  # 限制长度

        # 使用指定的内容选择器
        content_element = soup.select_one(content_selector)
        if content_element:
            return content_element.get_text(strip=True)

        logger.warning(f"未找到内容元素 - {self.name}")
        return ""