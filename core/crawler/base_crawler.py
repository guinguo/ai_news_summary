"""
爬虫基类，定义爬虫的通用接口和方法
"""
import time
import logging
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests

from config.settings import CRAWLER_HEADERS, CRAWL_DELAY, MAX_CRAWL_DEPTH

logger = logging.getLogger(__name__)

CHROME_USER_AGENT = "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


class BaseCrawler(ABC):
    """爬虫基类，定义爬虫的通用接口和方法"""

    def __init__(self, site_config: Dict[str, Any]):
        """
        初始化爬虫

        Args:
            site_config: 站点配置信息
        """
        self.site_config = site_config
        self.name = site_config["name"]
        self.url = site_config["url"]
        self.headers = CRAWLER_HEADERS
        self.driver = None
        self.session = None
        self.current_depth = 0
        self.max_depth = MAX_CRAWL_DEPTH

        logger.info(f"初始化爬虫 - {self.name}")

    def init_headless_selenium_driver(self):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                options = webdriver.ChromeOptions()
                self.add_argument(options)
                service = ChromeService(log_output="/tmp/chrome_debug.log")
                driver = webdriver.Chrome(options=options, service=service)
                return driver
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.error(f"Attempt init_headless_selenium_driver {attempt + 1} failed. {e} Retrying...")
                    time.sleep(2)
                else:
                    raise e

    def add_argument(self, options: Union[webdriver.ChromeOptions, uc.ChromeOptions]):
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(CHROME_USER_AGENT)
        return options

    def setup_selenium(self):
        """设置Selenium WebDriver"""
        self.driver = self.init_headless_selenium_driver()

    def setup_requests(self):
        """设置Requests会话"""
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        logger.info(f"Requests会话初始化成功 - {self.name}")

    def close(self):
        """关闭资源"""
        if self.driver:
            self.driver.quit()
            logger.info(f"Selenium WebDriver 已关闭 - {self.name}")

        if self.session:
            self.session.close()
            logger.info(f"Requests会话已关闭 - {self.name}")

    def get_page_content(self, url: str) -> Optional[str]:
        """
        获取页面内容

        Args:
            url: 页面URL

        Returns:
            页面HTML内容或None（如果获取失败）
        """
        try:
            self.driver.get(url)
            time.sleep(CRAWL_DELAY)  # 添加延迟，避免频繁请求
            return self.driver.page_source
        except Exception as e:
            logger.error(f"获取页面内容失败 - {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        解析HTML

        Args:
            html: HTML内容

        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(html, 'lxml')

    @abstractmethod
    def extract_news_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        提取新闻链接

        Args:
            soup: BeautifulSoup对象

        Returns:
            新闻链接列表，每个元素包含title和url
        """
        pass

    @abstractmethod
    def extract_content(self, soup: BeautifulSoup) -> str:
        """
        提取新闻内容

        Args:
            soup: BeautifulSoup对象

        Returns:
            新闻内容
        """
        pass

    def crawl(self) -> List[Dict[str, Any]]:
        """
        爬取新闻

        Returns:
            爬取的新闻列表
        """
        logger.info(f"开始爬取 - {self.name}")

        try:
            self.setup_selenium()

            # 爬取主页
            html = self.get_page_content(self.url)
            if not html:
                logger.error(f"无法获取主页内容 - {self.name}")
                return []

            soup = self.parse_html(html)
            news_links = self.extract_news_links(soup)

            logger.info(f"从主页获取了 {len(news_links)} 个新闻链接 - {self.name}")

            results = []
            # 爬取内容页
            for news in news_links[:5]:  # 限制爬取数量
                try:
                    content_html = self.get_page_content(news['url'])
                    if content_html:
                        content_soup = self.parse_html(content_html)
                        content = self.extract_content(content_soup)

                        news_item = {
                            'title': news['title'],
                            'url': news['url'],
                            'content': content,
                            'source': self.name
                        }

                        results.append(news_item)
                        logger.info(f"成功爬取新闻: {news['title']}")
                except Exception as e:
                    logger.error(f"爬取新闻内容失败 - {news['title']}: {e}")

            return results
        except Exception as e:
            logger.error(f"爬取过程中出错 - {self.name}: {e}")
            return []
        finally:
            self.close()