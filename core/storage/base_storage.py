"""
存储基类，定义存储的通用接口和方法
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class BaseStorage(ABC):
    """存储基类，定义存储的通用接口和方法"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化存储

        Args:
            config: 存储配置信息
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        logger.info(f"初始化存储 - {self.name}")

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> bool:
        """
        保存数据

        Args:
            data: 要保存的数据

        Returns:
            保存结果
        """
        pass

    @abstractmethod
    def load(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        加载数据

        Args:
            query: 查询条件

        Returns:
            加载的数据列表
        """
        pass