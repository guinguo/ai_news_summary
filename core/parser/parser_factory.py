"""
解析器工厂，负责创建不同类型的解析器
"""
import logging
from typing import Dict, Any

from core.parser.base_parser import BaseParser
from core.parser.site_parsers.common_parser import CommonParser

logger = logging.getLogger(__name__)


class ParserFactory:
    """解析器工厂类，用于创建不同类型的解析器"""

    @staticmethod
    def create_parser(site_config: Dict[str, Any]) -> BaseParser:
        """
        根据站点配置创建对应的解析器实例

        Args:
            site_config: 站点配置信息

        Returns:
            解析器实例
        """
        parser_type = site_config.get("parser_type", "common")

        logger.info(f"创建解析器 - {site_config['name']} - 类型: {parser_type}")

        # 根据parser_type创建对应的解析器
        if parser_type == "common":
            return CommonParser(site_config)

        # 如果需要自定义解析器，可以在这里添加更多的条件判断
        # elif parser_type == "custom_type":
        #     return CustomParser(site_config)

        else:
            logger.warning(f"未知解析器类型 {parser_type}，使用通用解析器")
            return CommonParser(site_config)