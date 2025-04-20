#!/usr/bin/env python3
"""
运行脚本，支持定时运行和手动运行
"""
import sys
import time
import schedule
import logging
import argparse
from utils.logger import setup_logger
from main import main


def setup_scheduler(interval):
    """设置定时任务"""
    logger = logging.getLogger(__name__)
    logger.info(f"设置定时任务，每 {interval} 小时运行一次")

    schedule.every(interval).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    # 设置日志
    setup_logger()
    logger = logging.getLogger(__name__)

    # 命令行参数
    parser = argparse.ArgumentParser(description='AI新闻摘要系统')
    parser.add_argument('--schedule', type=int, help='定时运行间隔（小时）')
    args = parser.parse_args()

    try:
        if args.schedule:
            setup_scheduler(args.schedule)
        else:
            sys.exit(main())
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        logger.error(f"运行出错: {e}")
        sys.exit(1)