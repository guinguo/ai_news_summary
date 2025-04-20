"""
测试用AI提供者，不调用实际API，用于开发和测试
"""
import logging
from typing import Dict, Any, Optional

from core.ai.base_ai import BaseAI

logger = logging.getLogger(__name__)


class DummyProvider(BaseAI):
    """测试用AI提供者，不调用实际API，用于开发和测试"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化测试提供者

        Args:
            config: 配置信息
        """
        super().__init__(config)
        logger.info("初始化测试AI提供者")

    def summarize(self, title: str, content: str) -> Optional[Dict[str, str]]:
        """
        生成测试摘要

        Args:
            title: 新闻标题
            content: 新闻内容

        Returns:
            测试摘要
        """
        logger.info(f"生成测试摘要 - 标题: {title[:30]}...")

        # 简单处理，截取原标题和内容的一部分作为摘要
        summary_title = f"[摘要] {title[:40]}" if len(title) > 40 else f"[摘要] {title}"

        # 取内容的前200字符作为摘要
        content_preview = content[:200] if content else "无内容"
        summary_content = f"{content_preview}... (这是一个由测试AI生成的摘要，不反映实际内容质量)"

        summary = {
            "title": summary_title,
            "content": summary_content
        }

        return summary if self.validate_summary(summary) else None