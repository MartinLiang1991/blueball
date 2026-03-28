import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class GoldDetector:
    """金钱识别模块：通过 OCR 识别当前金钱数量"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self._gold_region = config.get_region("gold_area")

    def detect(self) -> int:
        """
        识别当前金钱数量。

        Returns:
            金钱数量（整数），识别失败返回 0
        """
        try:
            text = self.ola.ocr(
                self._gold_region.x1,
                self._gold_region.y1,
                self._gold_region.x2,
                self._gold_region.y2
            )
            if not text:
                logger.debug("金钱 OCR 结果为空")
                return 0

            # 提取数字
            numbers = re.findall(r'\d+', text.replace(",", "").replace(" ", ""))
            if numbers:
                gold = int(numbers[0])
                logger.debug(f"金钱识别: '{text}' -> {gold}")
                return gold

            logger.debug(f"金钱 OCR 未能提取数字: '{text}'")
            return 0

        except Exception as e:
            logger.error(f"金钱识别异常: {e}")
            return 0
