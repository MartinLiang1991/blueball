import re
import time
import logging
from typing import Optional
from collections import Counter

logger = logging.getLogger(__name__)


class GoldDetector:
    """金钱识别模块：通过 OCR 识别当前金钱数量"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self._gold_region = config.get_region("持有金钱")

    def _parse_gold(self, text: str) -> int:
        """
        解析 OCR 文本为金钱数量。

        支持格式：
        - 纯数字: "1234" -> 1234
        - k 格式: "1.2k", "2.5k", "10k" -> 1200, 2500, 10000

        Args:
            text: OCR 识别结果

        Returns:
            金钱数量（整数）
        """
        text = text.strip().lower().replace(",", "").replace(" ", "")

        # 先处理 k 格式（如 "1.2k" -> 1200），保留小数点
        match_k = re.search(r'([\d.]+)k', text)
        if match_k:
            try:
                val = float(match_k.group(1))
                return int(val * 1000)
            except ValueError:
                pass

        # 再清理其他字符，处理纯数字
        text = text.replace(".", "").replace("-", "")
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])

        return 0

    def detect(self) -> int:
        """
        识别当前金钱数量（多次 OCR 取众数提高准确度）。

        Returns:
            金钱数量（整数），识别失败返回 0
        """
        try:
            # 安全检查：确保必要对象存在
            if not self.ola or not self._gold_region:
                logger.warning("金钱识别: ola 或 gold_region 未初始化")
                return 0

            results = []
            ocr_attempts = 3  # OCR 次数
            x1, y1, x2, y2 = self._gold_region.x1, self._gold_region.y1, self._gold_region.x2, self._gold_region.y2

            for attempt in range(ocr_attempts):
                # 优先使用 ocr_v5，失败则回退到 ocr
                text = None
                try:
                    ocr_v5_func = getattr(self.ola, 'ocr_v5', None)
                    if ocr_v5_func:
                        text = ocr_v5_func(x1, y1, x2, y2)
                except Exception as e:
                    logger.debug(f"ocr_v5 调用失败: {e}")

                if not text:
                    try:
                        ocr_func = getattr(self.ola, 'ocr', None)
                        if ocr_func:
                            text = ocr_func(x1, y1, x2, y2)
                    except Exception as e:
                        logger.debug(f"ocr 调用失败: {e}")

                if text:
                    gold = self._parse_gold(text)
                    if gold > 0:
                        results.append(gold)
                        logger.debug(f"金钱 OCR 第{attempt+1}次: '{text}' -> {gold}")

                if attempt < ocr_attempts - 1:
                    time.sleep(0.3)  # 间隔避免截同一帧

            if not results:
                logger.debug(f"金钱 OCR {ocr_attempts}次均未识别到有效数字")
                return 0

            # 取众数
            counter = Counter(results)
            best = counter.most_common(1)[0][0]
            logger.debug(f"金钱识别结果: {results}, 取众数: {best}")
            return best

        except Exception as e:
            logger.error(f"金钱识别异常: {e}")
            return 0
