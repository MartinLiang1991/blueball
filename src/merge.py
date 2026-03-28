import logging
from typing import List, Tuple, Optional
from collections import defaultdict

from .detector import NPCInfo

logger = logging.getLogger(__name__)

MAX_STAR = 4  # 最高星级


class MergeModule:
    """合成模块：找到可合成的 NPC 配对并执行拖拽合成"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self.merge_wait = int(config.timing.merge_wait * 1000)

    def find_merge_pairs(self, npcs: List[NPCInfo]) -> List[Tuple[NPCInfo, NPCInfo]]:
        """
        从 NPC 列表中找到所有可合成的配对。
        
        同种类 + 同星级 + 星级 < 4 的 NPC 两两配对。

        Args:
            npcs: YOLO 检测到的 NPC 列表

        Returns:
            配对列表 [(npc1, npc2), ...]，优先高星级配对
        """
        groups = defaultdict(list)
        for npc in npcs:
            if npc.star < MAX_STAR:
                groups[(npc.name, npc.star)].append(npc)

        pairs = []
        for (name, star), group in groups.items():
            # 每两个相同 NPC 组成一个配对
            for i in range(0, len(group) - 1, 2):
                pairs.append((group[i], group[i + 1]))

        # 优先合成高星级的（三星 > 二星 > 一星）
        pairs.sort(key=lambda p: p[0].star, reverse=True)

        if pairs:
            logger.info(f"找到 {len(pairs)} 组可合成配对")
            for n1, n2 in pairs:
                logger.info(f"  {n1.name} {n1.star}星 -> 合成")

        return pairs

    def execute_merge(self, npc1: NPCInfo, npc2: NPCInfo) -> bool:
        """
        执行合成操作：拖拽 npc1 到 npc2 上。

        Returns:
            是否执行成功
        """
        try:
            logger.info(f"合成: {npc1.name} {npc1.star}星 ({npc1.cx},{npc1.cy}) -> ({npc2.cx},{npc2.cy})")
            self.ola.drag(
                npc1.cx, npc1.cy, npc2.cx, npc2.cy,
                down_delay=50, move_delay=80, up_delay=50
            )
            self.ola.delay(self.merge_wait)
            logger.info("合成完成，等待动画")
            return True
        except Exception as e:
            logger.error(f"合成操作异常: {e}")
            return False

    def merge_all(self, npcs: List[NPCInfo]) -> int:
        """
        执行所有可合成的配对。

        Args:
            npcs: 当前 NPC 列表

        Returns:
            本次执行的合成次数
        """
        pairs = self.find_merge_pairs(npcs)
        count = 0
        for npc1, npc2 in pairs:
            if self.execute_merge(npc1, npc2):
                count += 1
        return count
