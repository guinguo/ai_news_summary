"""
AI服务基类，定义AI服务的通用接口和方法
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from config.settings import TITLE_MAX_LENGTH, CONTENT_MAX_LENGTH

logger = logging.getLogger(__name__)


class BaseAI(ABC):
    """AI服务基类，定义AI服务的通用接口和方法"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化AI服务

        Args:
            config: AI服务配置信息
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        logger.info(f"初始化AI服务 - {self.name}")

    @abstractmethod
    def summarize(self, title: str, content: str) -> Optional[Dict[str, str]]:
        """
        对新闻内容进行摘要

        Args:
            title: 新闻标题
            content: 新闻内容

        Returns:
            摘要信息，包含title和content，或None（如果摘要失败）
        """
        pass

    def validate_summary(self, summary: Dict[str, str]) -> bool:
        """
        验证摘要是否符合要求

        Args:
            summary: 摘要信息，包含title和content

        Returns:
            验证结果
        """
        if not summary:
            return False

        title = summary.get("title", "")
        content = summary.get("content", "")

        if not title or not content:
            logger.warning("摘要标题或内容为空")
            return False

        if len(title) > TITLE_MAX_LENGTH:
            logger.warning(f"摘要标题超过最大长度: {len(title)} > {TITLE_MAX_LENGTH}")
            summary["title"] = title[:TITLE_MAX_LENGTH]

        if len(content) > CONTENT_MAX_LENGTH:
            logger.warning(f"摘要内容超过最大长度: {len(content)} > {CONTENT_MAX_LENGTH}")
            summary["content"] = content[:CONTENT_MAX_LENGTH]

        return True