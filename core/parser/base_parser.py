"""
解析器基类，定义解析器的通用接口和方法
"""
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """解析器基类，定义解析器的通用接口和方法"""

    def __init__(self, site_config: Dict[str, Any]):
        """
        初始化解析器

        Args:
            site_config: 站点配置信息
        """
        self.site_config = site_config
        self.name = site_config["name"]
        logger.info(f"初始化解析器 - {self.name}")

    @abstractmethod
    def parse(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析原始数据

        Args:
            raw_data: 原始数据，包含标题、URL和内容

        Returns:
            解析后的数据或None（如果解析失败）
        """
        pass