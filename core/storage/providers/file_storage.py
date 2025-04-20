"""
文件存储，将数据保存到文件系统
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

from core.storage.base_storage import BaseStorage
from config.settings import OUTPUT_DIR
from utils.helpers import get_file_path

logger = logging.getLogger(__name__)


class FileStorage(BaseStorage):
    """文件存储，将数据保存到文件系统"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化文件存储

        Args:
            config: 存储配置信息
        """
        super().__init__(config)
        self.output_dir = self.config.get("output_dir", OUTPUT_DIR)

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"文件存储初始化成功，输出目录: {self.output_dir}")

    def save(self, data: Dict[str, Any]) -> bool:
        """
        将数据保存到文件

        Args:
            data: 要保存的数据

        Returns:
            保存结果
        """
        try:
            # 获取文件名
            source = data.get("source", "unknown")
            file_path = get_file_path(self.output_dir, source)

            # 添加时间戳
            data["saved_at"] = datetime.now().isoformat()

            # 读取已有数据
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        logger.warning(f"解析文件失败，创建新文件: {file_path}")
                        existing_data = []

            # 追加新数据
            existing_data.append(data)

            # 保存数据
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)

            logger.info(f"数据已保存到文件: {file_path}")
            return True

        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            return False

    def load(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        从文件加载数据

        Args:
            query: 查询条件，可以包含source、date等

        Returns:
            加载的数据列表
        """
        results = []

        try:
            # 如果指定了源，只加载该源的文件
            if query and "source" in query:
                source = query["source"]
                file_path = get_file_path(self.output_dir, source)

                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        results.extend(data)
            else:
                # 加载所有文件
                for file_name in os.listdir(self.output_dir):
                    if file_name.endswith('.json'):
                        file_path = os.path.join(self.output_dir, file_name)

                        with open(file_path, 'r', encoding='utf-8') as f:
                            try:
                                data = json.load(f)
                                results.extend(data)
                            except json.JSONDecodeError:
                                logger.warning(f"解析文件失败: {file_path}")

            # 应用查询过滤
            if query:
                filtered_results = []
                for item in results:
                    match = True
                    for key, value in query.items():
                        if key == "source":
                            continue  # 已经在文件级别过滤过了
                        if key not in item or item[key] != value:
                            match = False
                            break
                    if match:
                        filtered_results.append(item)
                results = filtered_results

            logger.info(f"已加载 {len(results)} 条数据")
            return results

        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            return []