"""
AI工厂，负责创建不同的AI服务实例
"""
import logging
from typing import Dict, Any

from core.ai.base_ai import BaseAI
from core.ai.providers.openai_provider import OpenAIProvider
from core.ai.providers.dummy_provider import DummyProvider

logger = logging.getLogger(__name__)


class AIFactory:
    """AI工厂类，用于创建不同类型的AI服务实例"""

    @staticmethod
    def create_ai_service(ai_type: str, config: Dict[str, Any] = None) -> BaseAI:
        """
        创建AI服务实例

        Args:
            ai_type: AI服务类型
            config: AI服务配置信息

        Returns:
            AI服务实例
        """
        logger.info(f"创建AI服务 - 类型: {ai_type}")

        # 根据类型创建对应的AI服务
        if ai_type == "openai":
            return OpenAIProvider(config)
        elif ai_type == "grok":
            # TODO: 实现Grok提供者
            logger.warning("Grok提供者尚未实现，使用测试提供者")
            return DummyProvider(config)
        elif ai_type == "gemini":
            # TODO: 实现Gemini提供者
            logger.warning("Gemini提供者尚未实现，使用测试提供者")
            return DummyProvider(config)
        elif ai_type == "qwen":
            # TODO: 实现Qwen提供者
            logger.warning("Qwen提供者尚未实现，使用测试提供者")
            return DummyProvider(config)
        elif ai_type == "dummy":
            return DummyProvider(config)
        else:
            logger.warning(f"未知AI服务类型 {ai_type}，使用测试提供者")
            return DummyProvider(config)