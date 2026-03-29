import json
import logging
import re
import time
from typing import Optional, Tuple, List, Dict

logger = logging.getLogger(__name__)


class EnhanceModule:
    """强化模块：执行强化操作并选择卡牌"""

    # 强化解锁所需召唤次数
    UNLOCK_SUMMON_COUNT = 7

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self._enhance_count = 0  # 已强化次数

        # 从配置获取强化费用表
        self.cost_table = config.enhance_cost_table or [100, 200, 400, 600, 1000, 1500, 1800, 2500, 3000, 3500]

        # 词条优先级
        self.card_priority = config.card_priority or {}

        # 获取按钮坐标
        self.enhance_btn = config.get_button("强化")
        self.middle_card_btn = config.get_button("中间卡牌")

        # 获取 OCR 区域
        self.draw_region = config.get_region("开始抽卡识别")
        self.card_region = config.get_region("强化卡牌识别")

    @property
    def enhance_count(self) -> int:
        return self._enhance_count

    def reset_count(self):
        """重置强化计数（新副本开始时调用）"""
        self._enhance_count = 0
        logger.info("强化计数已重置")

    def get_cost(self) -> int:
        """获取下一次强化费用"""
        if self._enhance_count >= len(self.cost_table):
            return 0
        return self.cost_table[self._enhance_count]

    def is_unlocked(self, summon_count: int) -> bool:
        """检查强化是否已解锁"""
        return summon_count >= self.UNLOCK_SUMMON_COUNT

    def is_max_level(self) -> bool:
        """检查是否已达到强化上限"""
        return self._enhance_count >= len(self.cost_table)

    def can_enhance(self, summon_count: int, gold: int) -> Tuple[bool, str]:
        """
        判断是否可以强化。

        Args:
            summon_count: 当前召唤次数
            gold: 当前金钱

        Returns:
            (是否可强化, 原因说明)
        """
        # 1. 检查是否解锁
        if not self.is_unlocked(summon_count):
            return False, f"强化未解锁: 召唤 {summon_count} < {self.UNLOCK_SUMMON_COUNT}"

        # 2. 检查是否已达上限
        if self.is_max_level():
            return False, f"强化已达上限: {self._enhance_count} >= {len(self.cost_table)}"

        # 3. 检查金币是否足够
        cost = self.get_cost()
        if gold < cost:
            return False, f"金币不足: {gold} < {cost}"

        return True, f"可强化: 费用 {cost}"

    def execute_enhance(self) -> bool:
        """
        执行强化操作。

        Returns:
            是否强化成功
        """
        try:
            # 1. 点击强化按钮
            if self.enhance_btn[0] <= 0 and self.enhance_btn[1] <= 0:
                logger.error("未配置强化按钮坐标")
                return False

            logger.info(f"点击强化按钮 {self.enhance_btn}")
            self.ola.left_click(self.enhance_btn[0], self.enhance_btn[1])
            self.ola.delay(500)  # 等待 0.5 秒

            # 2. OCR 检测"开始抽卡识别"区域，判断是否出现"请选择"
            text = self.ola.ocr(
                self.draw_region.x1, self.draw_region.y1,
                self.draw_region.x2, self.draw_region.y2
            )
            text = text.strip() if text else ""

            if "请选择" not in text:
                logger.warning(f"强化失败: OCR 结果为 '{text}'，未检测到'请选择'")
                return False

            logger.info("强化成功，进入抽卡阶段")

            # 3. 选择卡牌
            if not self.select_card():
                logger.warning("抽卡选择失败")
                return False

            # 4. 等待抽卡完成
            self.ola.delay(500)

            # 5. 确认抽卡完成（OCR 不到"请选择"）
            for _ in range(5):
                text = self.ola.ocr(
                    self.draw_region.x1, self.draw_region.y1,
                    self.draw_region.x2, self.draw_region.y2
                )
                text = text.strip() if text else ""
                if "请选择" not in text:
                    logger.info("抽卡完成")
                    self._enhance_count += 1
                    logger.info(f"强化完成，累计强化 {self._enhance_count} 次")
                    return True
                time.sleep(0.3)

            logger.warning("抽卡完成后未能确认")
            return True  # 假定成功

        except Exception as e:
            logger.error(f"强化操作异常: {e}")
            return False

    def select_card(self) -> bool:
        """
        选择卡牌：优先选择暴风词条，否则选择中间卡牌。

        Returns:
            是否选择成功
        """
        try:
            # 1. OCR 获取所有卡牌的文字和坐标
            result = self.ola.ocr_details(
                self.card_region.x1, self.card_region.y1,
                self.card_region.x2, self.card_region.y2
            )

            if not result:
                logger.warning("卡牌 OCR 结果为空，使用默认选择")
                return self._click_default_card()

            # 2. 解析 OCR 结果
            # result 可能是 JSON 字符串或字典
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    logger.warning(f"卡牌 OCR JSON 解析失败: {result}")
                    return self._click_default_card()

            # 调试日志：输出 OCR 原始结果
            logger.info(f"卡牌 OCR 原始结果: {result}")

            # 3. 查找匹配的词条和最高优先级
            best_card = self._find_best_card(result)

            if best_card:
                logger.info(f"选择卡牌: {best_card['text']} at ({best_card['x']}, {best_card['y']})")
                self.ola.left_click(best_card['x'], best_card['y'])
                return True
            else:
                logger.info("未找到暴风词条，使用默认选择")
                return self._click_default_card()

        except Exception as e:
            logger.error(f"选择卡牌异常: {e}")
            return self._click_default_card()

    def _find_best_card(self, ocr_result: dict) -> Optional[dict]:
        """
        从 OCR 结果中查找优先级最高的卡牌。

        Args:
            ocr_result: OCR 识别结果

        Returns:
            最优卡牌信息或 None
        """
        # 提取文字块列表
        words = ocr_result.get("words", [])
        if not words:
            # 尝试其他可能的数据格式
            words = ocr_result.get("detected_texts", [])

        # 如果还是没有，尝试 Regions 格式（OLAPlug OCR 格式）
        if not words:
            regions = ocr_result.get("Regions", [])
            if regions:
                # 转换为 words 格式
                words = []
                for region in regions:
                    text = region.get("Text", "")
                    center = region.get("Center", {})
                    x = center.get("x", 0)
                    y = center.get("y", 0)
                    if text and x and y:
                        words.append({
                            "text": text,
                            "x": x,
                            "y": y
                        })

        if not words:
            return None

        if isinstance(words, list) and words:
            # 可能是字符串列表
            if isinstance(words[0], str):
                # 只有文字没有坐标，无法点击
                return None

        # 遍历文字块，查找匹配的词条
        best_priority = 999
        best_card = None

        for word_info in words:
            # 兼容不同格式
            if isinstance(word_info, dict):
                text = word_info.get("text", "")
                # 尝试获取坐标
                x = word_info.get("x", 0) or word_info.get("cx", 0)
                y = word_info.get("y", 0) or word_info.get("cy", 0)
                # 尝试从区域计算中心点
                if x == 0 and y == 0:
                    box = word_info.get("box", [])
                    if len(box) >= 4:
                        x = (box[0] + box[2]) // 2
                        y = (box[1] + box[3]) // 2
                if x == 0 and y == 0:
                    continue
            else:
                continue

            # 检查是否包含优先级词条
            matched = False
            for keyword, priority in self.card_priority.items():
                if keyword in text:
                    logger.info(f"卡牌匹配成功: '{text}' 包含关键词 '{keyword}' (优先级={priority})")
                    matched = True
                    if priority < best_priority:
                        best_priority = priority
                        best_card = {"text": text, "x": x, "y": y, "priority": priority}
                    break
            if not matched:
                logger.info(f"卡牌未匹配优先级词条: '{text}'")

        return best_card

    def _click_default_card(self) -> bool:
        """点击默认中间卡牌"""
        if self.middle_card_btn[0] <= 0 and self.middle_card_btn[1] <= 0:
            logger.error("未配置中间卡牌按钮坐标")
            return False

        logger.info(f"点击中间卡牌 {self.middle_card_btn}")
        self.ola.left_click(self.middle_card_btn[0], self.middle_card_btn[1])
        return True
