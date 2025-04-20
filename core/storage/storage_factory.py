"""
存储工厂，负责创建不同类型的存储实例
"""
import logging
from typing import Dict, Any

from core.storage.base_storage import BaseStorage
from core.storage.providers.file_storage import FileStorage

logger = logging.getLogger(__name__)


class StorageFactory:
    """存储工厂类，用于创建不同类型的存储实例"""

    @staticmethod
    def create_storage(storage_type: str, config: Dict[str, Any] = None) -> BaseStorage:
        """
        创建存储实例

        Args:
            storage_type: 存储类型
            config: 存储配置信息

        Returns:
            存储实例
        """
        logger.info(f"创建存储 - 类型: {storage_type}")

        # 根据类型创建对应的存储
        if storage_type == "file":
            return FileStorage(config)
        # 可以在这里添加更多存储类型
        # elif storage_type == "database":
        #     return DatabaseStorage(config)
        else:
            logger.warning(f"未知存储类型 {storage_type}，使用文件存储")
            return FileStorage(config)