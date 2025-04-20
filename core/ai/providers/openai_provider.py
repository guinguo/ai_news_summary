"""
OpenAI提供者，使用OpenAI API进行新闻摘要
"""
import os
import logging
from typing import Dict, Any, Optional

import openai

from core.ai.base_ai import BaseAI
from config.settings import TITLE_MAX_LENGTH, CONTENT_MAX_LENGTH

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAI):
    """OpenAI提供者，使用OpenAI API进行新闻摘要"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化OpenAI提供者

        Args:
            config: 配置信息
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        self.model = self.config.get("model", "gpt-3.5-turbo")

        if not self.api_key:
            logger.warning("未设置OpenAI API密钥，将无法使用OpenAI服务")
        else:
            openai.api_key = self.api_key
            logger.info(f"OpenAI服务初始化成功，使用模型: {self.model}")

    def summarize(self, title: str, content: str) -> Optional[Dict[str, str]]:
        """
        使用OpenAI API对新闻内容进行摘要

        Args:
            title: 新闻标题
            content: 新闻内容

        Returns:
            摘要信息，包含title和content，或None（如果摘要失败）
        """
        if not self.api_key:
            logger.error("未设置OpenAI API密钥，无法进行摘要")
            return None

        try:
            # 构建提示词
            prompt = f"""请根据以下新闻内容进行摘要：

原标题：{title}

原内容：
{content[:3000]}  # 限制内容长度，避免token过多

请提供以下格式的摘要：
1. 新标题：（不超过{TITLE_MAX_LENGTH}个字符）
2. 内容摘要：（不超过{CONTENT_MAX_LENGTH}个字符）

要求：
- 新标题应简洁明了，突出新闻重点
- 内容摘要应保留关键信息，用简洁的语言概括新闻内容
- 保持客观中立的语气
"""

            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的新闻编辑，擅长提炼新闻重点并进行简明扼要的总结。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,  # 较低的temperature使输出更加确定性
                max_tokens=1000
            )

            # 解析回复
            ai_response = response.choices[0].message.content.strip()

            # 提取标题和内容
            new_title = ""
            new_content = ""

            title_match = re.search(r"新标题：(.*?)(?:\n|$)", ai_response)
            if title_match:
                new_title = title_match.group(1).strip()

            content_match = re.search(r"内容摘要：([\s\S]*?)(?:\n\n|$)", ai_response)
            if content_match:
                new_content = content_match.group(1).strip()

            if not new_title or not new_content:
                # 如果正则匹配失败，尝试按行分割
                lines = ai_response.split('\n')
                for line in lines:
                    if line.startswith("1. 新标题：") or line.startswith("新标题："):
                        new_title = line.split('：', 1)[1].strip()
                    elif line.startswith("2. 内容摘要：") or line.startswith("内容摘要："):
                        new_content = line.split('：', 1)[1].strip()

            summary = {
                "title": new_title[:TITLE_MAX_LENGTH] if new_title else title[:TITLE_MAX_LENGTH],
                "content": new_content[:CONTENT_MAX_LENGTH] if new_content else content[:100] + "..."
            }

            if self.validate_summary(summary):
                logger.info(f"成功生成摘要 - 标题: {summary['title']}")
                return summary
            else:
                logger.warning("摘要验证失败")
                return None

        except Exception as e:
            logger.error(f"OpenAI API调用失败: {e}")
            return None