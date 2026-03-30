import logging
from typing import List, Tuple, Optional
from collections import defaultdict

from .detector import NPCInfo

logger = logging.getLogger(__name__)


class MergeModule:
    """合成模块：找到可合成的 NPC 配对并执行拖拽合成"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola
        self.merge_wait = int(config.timing.merge_wait * 1000)

    def _is_protected(self, npc: NPCInfo) -> bool:
        """检查 NPC 是否受保护"""
        return self.config.merge_strategy.is_protected(npc.name, npc.star)

    def find_merge_pairs(self, npcs: List[NPCInfo], include_protected: bool = False, max_merge_star: int = 0) -> List[Tuple[NPCInfo, NPCInfo]]:
        """
        从 NPC 列表中找到所有可合成的配对。

        同种类 + 同星级 + 星级 < max_star 的 NPC 两两配对。

        Args:
            npcs: YOLO 检测到的 NPC 列表
            include_protected: 是否包含受保护的 NPC。False 时排除受保护的 NPC。
            max_merge_star: 允许合并的保护 NPC 的最高星级（0 表示不限制）

        Returns:
            配对列表 [(npc1, npc2), ...]，优先高星级配对
        """
        max_star = self.config.merge_strategy.max_star

        # 过滤可合成的 NPC（排除空位 kongwei）
        groups = defaultdict(list)
        for npc in npcs:
            # 跳过空位
            if npc.name == "kongwei":
                continue
            if npc.star < max_star:
                # 根据 include_protected 决定是否跳过受保护的 NPC
                if not include_protected and self._is_protected(npc):
                    logger.debug(f"跳过受保护 NPC: {npc.name} {npc.star}星")
                    continue
                # 保护合成时，只允许合成不超过 max_merge_star 的保护 NPC
                if include_protected and max_merge_star > 0:
                    if self._is_protected(npc) and npc.star > max_merge_star:
                        logger.debug(f"跳过高星级保护 NPC: {npc.name} {npc.star}星")
                        continue
                groups[(npc.name, npc.star)].append(npc)

        pairs = []
        for (name, star), group in groups.items():
            # 每两个相同 NPC 组成一个配对
            for i in range(0, len(group) - 1, 2):
                pairs.append((group[i], group[i + 1]))

        # 优先合成高星级的（三星 > 二星 > 一星）
        pairs.sort(key=lambda p: p[0].star, reverse=True)

        if pairs:
            logger.info(f"找到 {len(pairs)} 组可合成配对 (include_protected={include_protected})")
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

    def merge_all(self, npcs: List[NPCInfo], include_protected: bool = False, max_merge_star: int = 0, max_count: int = 1) -> int:
        """
        执行可合成的配对。

        Args:
            npcs: 当前 NPC 列表
            include_protected: 是否包含受保护的 NPC
            max_merge_star: 允许合并的保护 NPC 的最高星级（0 表示不限制）
            max_count: 最多合成几对，默认 1（合成结果随机，保守合成）

        Returns:
            本次执行的合成次数
        """
        pairs = self.find_merge_pairs(npcs, include_protected, max_merge_star)
        count = 0
        for npc1, npc2 in pairs:
            if count >= max_count:
                break
            if self.execute_merge(npc1, npc2):
                count += 1
        return count
