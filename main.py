import sys
import os
import argparse
import logging

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.bot import GameBot


def setup_logging(level: str = "INFO"):
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )


def main():
    parser = argparse.ArgumentParser(description="永远的蔚蓝星球 - 自动化工具")
    parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="配置文件路径 (默认: config.json)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="启用详细日志 (DEBUG 级别)"
    )
    args = parser.parse_args()

    # 加载配置
    config = Config(args.config)
    log_level = "DEBUG" if args.verbose else config.log_level
    setup_logging(log_level)

    logger = logging.getLogger(__name__)
    logger.info("永远的蔚蓝星球 - 自动化工具")
    logger.info(f"配置文件: {args.config}")

    # 初始化并运行 Bot
    bot = GameBot(config)
    if not bot.init():
        logger.error("初始化失败，请检查配置和游戏状态")
        sys.exit(1)

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("收到 Ctrl+C，正在停止...")
        bot.stop()
    finally:
        bot._cleanup()


if __name__ == "__main__":
    main()
