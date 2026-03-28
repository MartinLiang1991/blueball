import logging
from typing import Optional, Tuple

from .detector import NPCInfo

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
        summon_btn = buttons.get("summon", {})
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
        """获取当前 NPC 数量"""
        return len(npcs)

    def can_summon(self, gold: int, npcs: list) -> Tuple[bool, str]:
        """
        判断是否可以召唤。

        Args:
            gold: 当前金钱
            npcs: 当前 NPC 列表

        Returns:
            (是否可召唤, 原因说明)
        """
        cost = self.get_cost()
        if gold < cost:
            return False, f"金钱不足: {gold} < {cost}"

        npc_count = self.get_current_npc_count(npcs)
        max_slots = self.get_max_slots()
        if npc_count >= max_slots:
            return False, f"格位已满: {npc_count}/{max_slots}"

        return True, f"可召唤: 费用={cost}, 格位={npc_count}/{max_slots}"

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
