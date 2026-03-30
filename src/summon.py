import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class SummonModule:
    """召唤模块：判断是否可召唤并执行点击召唤按钮"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self.summon_cfg = config.summon
        self.summon_wait = int(config.timing.summon_wait * 1000)
        self._summon_count = 0  # 累计召唤次数

        # 从配置获取固定坐标
        buttons = config.data.get("buttons", {})
        summon_btn = buttons.get("召唤", {})
        self.summon_x = summon_btn.get("x", 0)
        self.summon_y = summon_btn.get("y", 0)

    @property
    def summon_count(self) -> int:
        return self._summon_count

    def reset_count(self):
        """重置召唤计数（新副本开始时调用）"""
        self._summon_count = 0
        logger.info("召唤计数已重置")

    def get_cost(self) -> int:
        """获取下一次召唤的费用"""
        return self.summon_cfg.get_cost(self._summon_count)

    def get_max_slots(self) -> int:
        """获取当前最大格位数"""
        return self.summon_cfg.get_slot_count(self._summon_count)

    def get_current_npc_count(self, npcs) -> int:
        """获取当前 NPC 数量（排除空位 kongwei）"""
        # 过滤掉 kongwei（空位标识）
        return sum(1 for npc in npcs if npc.name != "kongwei")

    def calc_summon_count(self, npcs) -> int:
        """
        计算召唤次数：1星=1次，2星=2次，3星=4次。

        Args:
            npcs: 当前 NPC 列表（包含 kongwei）

        Returns:
            召唤次数
        """
        total = 0
        for npc in npcs:
            if npc.name != "kongwei":
                # 1星=1, 2星=2, 3星=4
                total += 2 ** (npc.star - 1)
        return total

    def get_kongwei_count(self, npcs) -> int:
        """获取空位数量（kongwei 数量）"""
        return sum(1 for npc in npcs if npc.name == "kongwei")

    def can_summon(self, gold: int, npcs: list) -> Tuple[bool, str]:
        """
        判断是否可以召唤。

        Args:
            gold: 当前金钱（当前未使用）
            npcs: 当前 NPC 列表（包含 kongwei）

        Returns:
            (是否可召唤, 原因说明)
        """
        # 1. 检查是否有空位（用 kongwei 判断）
        kongwei_count = self.get_kongwei_count(npcs)
        if kongwei_count <= 0:
            return False, f"格位已满: 无空位"

        return True, f"可召唤: 空位={kongwei_count}"

    def get_summon_button_pos(self) -> Optional[Tuple[int, int]]:
        """获取召唤按钮的固定坐标位置"""
        if self.summon_x <= 0 and self.summon_y <= 0:
            logger.warning("未配置召唤按钮坐标")
            return None
        return (self.summon_x, self.summon_y)

    def execute_summon(self, npcs: list) -> bool:
        """
        执行召唤操作。

        Args:
            npcs: 当前 NPC 列表

        Returns:
            是否召唤成功
        """
        pos = self.get_summon_button_pos()
        if not pos:
            logger.warning("未配置召唤按钮坐标")
            return False

        try:
            bx, by = pos

            logger.info(f"点击召唤按钮 ({bx}, {by})，费用: {self.get_cost()}")
            self.ola.left_click(bx, by)
            self.ola.delay(self.summon_wait)
            self._summon_count += 1

            new_slots = self.get_max_slots()
            logger.info(f"召唤完成，累计 {self._summon_count} 次，当前最大格位: {new_slots}")
            return True

        except Exception as e:
            logger.error(f"召唤操作异常: {e}")
            return False
