"""
通用解析器，适用于大部分网站的内容解析
"""
import logging
import re
from typing import Dict, Any, Optional

from bs4 import BeautifulSoup

from core.parser.base_parser import BaseParser
from utils.helpers import clean_text

logger = logging.getLogger(__name__)


class CommonParser(BaseParser):
    """通用解析器实现，适用于大部分标准网站布局"""

    def __init__(self, site_config):
        super().__init__(site_config)
        self.article_selector = site_config.get("article_selector", {})

    def parse(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析原始数据

        Args:
            raw_data: 原始数据，包含标题、URL和内容

        Returns:
            解析后的数据或None（如果解析失败）
        """
        try:
            # 获取原始数据
            title = raw_data.get("title", "")
            url = raw_data.get("url", "")
            content = raw_data.get("content", "")
            source = raw_data.get("source", self.name)

            # 清理内容
            cleaned_content = self._clean_content(content)

            # 验证解析结果
            if not title or not cleaned_content:
                logger.warning(f"解析结果无效 - {url}")
                return None

            # 构建解析结果
            parsed_data = {
                "title": title,
                "url": url,
                "content": cleaned_content,
                "source": source
            }

            logger.info(f"成功解析内容 - {title}")
            return parsed_data

        except Exception as e:
            logger.error(f"解析数据失败: {e}")
            return None

    def _clean_content(self, content: str) -> str:
        """
        清理内容，去除广告、导航等无关内容

        Args:
            content: 原始内容

        Returns:
            清理后的内容
        """
        # 清理基本的HTML标签和空白字符
        content = clean_text(content)

        # 移除常见的广告和无关文本
        patterns_to_remove = [
            r"相关[推荐|阅读].*?(?=\n|$)",
            r"本文来源.*?(?=\n|$)",
            r"原标题.*?(?=\n|$)",
            r"编辑.*?(?=\n|$)",
            r"记者.*?(?=\n|$)",
            r"点击查看.*?(?=\n|$)",
            r".*?版权声明.*?(?=\n|$)",
            r".*?版权所有.*?(?=\n|$)",
            r".*?责任编辑.*?(?=\n|$)",
            r".*?文章来源.*?(?=\n|$)"
        ]

        for pattern in patterns_to_remove:
            content = re.sub(pattern, "", content)

        # 限制内容长度
        if len(content) > 5000:
            content = content[:5000] + "..."

        return content.strip()