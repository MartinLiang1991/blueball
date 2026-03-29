import logging
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)


class DecisionModule:
    """
    决策模块：根据游戏状态决定下一步操作

    决策模型 v5：
    - 初始期（7格）：只召唤+合成
    - 早期（8-9格）：强化优先，剩余召唤
    - 中期（10-11格）：优先强化，暴风>=8则停召唤
    - 后期（12+格）：全力强化，暴风>=8则停召唤

    阶段判断：
    - 初始期: max_slots < 9
    - 早期: 9 <= max_slots < 10
    - 中期: 10 <= max_slots < 12
    - 后期: max_slots >= 12
    """

    # 阶段阈值
    EARLY_THRESHOLD = 9    # 早期上限
    MIDDLE_THRESHOLD = 10  # 中期下限
    LATE_THRESHOLD = 12    # 后期下限

    # 强化间隔：每召唤N次才强化1次（保证召唤次数）
    ENHANCE_INTERVAL = 3

    # 操作类型
    ACTION_ENHANCE = "enhance"       # 强化
    ACTION_SUMMON = "summon"         # 召唤
    ACTION_MERGE = "merge"           # 合成（非保护）
    ACTION_MERGE_PROTECTED = "merge_protected"  # 合成保护
    ACTION_WAIT = "wait"             # 等待

    def __init__(self, config, summon_module, enhance_module, merge_module):
        self.config = config
        self.summon_module = summon_module
        self.enhance_module = enhance_module
        self.merge_module = merge_module
        self.merge_strategy = config.merge_strategy

    def get_phase(self, max_slots: int) -> str:
        """获取当前阶段"""
        if max_slots < self.EARLY_THRESHOLD:
            return "initial"   # 初始期
        elif max_slots < self.MIDDLE_THRESHOLD:
            return "early"     # 早期
        elif max_slots < self.LATE_THRESHOLD:
            return "middle"   # 中期
        else:
            return "late"      # 后期

    def is_save_mode(self, phase: str, enhance_unlocked: bool, enhance_count: int) -> bool:
        """
        判断是否进入存钱模式。

        Args:
            phase: 当前阶段
            enhance_unlocked: 强化是否已解锁
            enhance_count: 已强化次数

        Returns:
            是否进入存钱模式
        """
        # 仅后期阶段且强化可用时进入存钱模式
        if phase == "late":
            return enhance_unlocked and not self.enhance_module.is_max_level()
        return False

    def calc_protected_total_star(self, npcs) -> int:
        """计算受保护 NPC 的总星级"""
        total = 0
        stop_npc = self.merge_strategy.stop_summon_npc
        if not stop_npc:
            return 0
        for npc in npcs:
            if npc.name == stop_npc and self.merge_strategy.is_protected(npc.name, npc.star):
                total += npc.star
        return total

    def calc_npc_total_star(self, npcs, npc_name: str) -> int:
        """计算指定 NPC 的总星级"""
        total = 0
        for npc in npcs:
            if npc.name == npc_name:
                total += npc.star
        return total

    def can_summon_check(self, npcs) -> Tuple[bool, str]:
        """
        检查是否可以召唤（不包括金币检查）。

        Returns:
            (是否可以召唤, 原因)
        """
        # 检查空位
        kongwei_count = self.summon_module.get_kongwei_count(npcs)
        if kongwei_count <= 0:
            return False, "格位已满"

        # 检查星级阈值
        stop_npc = self.merge_strategy.stop_summon_npc
        stop_star = self.merge_strategy.stop_summon_total_star
        if stop_npc and stop_star > 0:
            total_star = self.calc_npc_total_star(npcs, stop_npc)
            if total_star >= stop_star:
                return False, f"{stop_npc}总星 {total_star}>={stop_star}"

        return True, "可召唤"

    def decide(
        self,
        gold: int,
        summon_count: int,
        npcs: List,
        merge_result: dict = None
    ) -> Tuple[str, dict]:
        """
        根据当前游戏状态做出决策。

        Args:
            gold: 当前金钱
            summon_count: 召唤次数
            npcs: 当前 NPC 列表（包含 kongwei）
            merge_result: 上一次合成的结果（可选），用于避免重复合成

        Returns:
            (操作类型, 详情字典)
        """
        # 获取当前状态
        max_slots = self.summon_module.get_max_slots()
        phase = self.get_phase(max_slots)

        # 强化相关状态
        enhance_unlocked = self.enhance_module.is_unlocked(summon_count)
        enhance_count = self.enhance_module.enhance_count
        enhance_cost = self.enhance_module.get_cost()

        # 召唤相关状态
        summon_cost = self.summon_module.get_cost()
        kongwei_count = self.summon_module.get_kongwei_count(npcs)
        can_summon, summon_reason = self.can_summon_check(npcs)

        # 暴风星级
        stop_npc = self.merge_strategy.stop_summon_npc
        stop_star = self.merge_strategy.stop_summon_total_star
        baofeng_star = self.calc_npc_total_star(npcs, stop_npc) if stop_npc else 0

        # 强化间隔检查：每召唤N次才强化1次（暴风>=8星时忽略间隔，全力强化）
        summon_since_enhance = summon_count - enhance_count
        baofeng_ready = stop_npc and stop_star > 0 and baofeng_star >= stop_star
        can_enhance_by_interval = baofeng_ready or summon_since_enhance >= self.ENHANCE_INTERVAL

        # 存钱模式判断
        save_mode = self.is_save_mode(phase, enhance_unlocked, enhance_count)

        # 蜘蛛数量检测
        zhizhu_count = self.calc_npc_total_star(npcs, "zhizhu")

        logger.info(
            f"决策输入: 金币={gold}, 召唤={summon_count}, 强化={enhance_count}, "
            f"格位={len([n for n in npcs if n.name != 'kongwei'])}/{max_slots}, "
            f"阶段={phase}, 存钱={save_mode}, baofeng星={baofeng_star}, "
            f"蜘蛛={zhizhu_count}, 强化间隔={summon_since_enhance}/{self.ENHANCE_INTERVAL}"
        )

        # ========== 决策流程 ==========

        # ① 检查是否可强化（需满足强化间隔）
        if enhance_unlocked and can_enhance_by_interval and not self.enhance_module.is_max_level():
            if gold >= enhance_cost:
                logger.info(f"决策: 强化 (金币{gold}>={enhance_cost})")
                return self.ACTION_ENHANCE, {"phase": phase, "cost": enhance_cost}

        # ①.5 蜘蛛合成检查：优先保留3个以下，超过3个则优先合成
        if zhizhu_count > 3:
            # 尝试合成蜘蛛
            can_merge_zhizhu, merge_zhizhu = self._check_merge_zhizhu(npcs)
            if can_merge_zhizhu:
                logger.info(f"决策: 合成蜘蛛 (当前{zhizhu_count}个>3)")
                return self.ACTION_MERGE, {"phase": phase, "npc": merge_zhizhu, "reason": "zhizhu_overflow"}

        # ② 检查是否可以召唤
        # 初始阶段（max_slots < 9）：即使金币不足也允许召唤（金币识别可能为0）
        # 其他阶段：需要金币 >= 召唤费用
        init_phase = phase == "initial"
        if can_summon and (init_phase or gold >= summon_cost):
            # 检查暴风星级阻断
            if stop_npc and stop_star > 0 and baofeng_star >= stop_star:
                logger.info(f"决策: 暴风星级阻断不召唤 (baofeng={baofeng_star}>={stop_star})")
            else:
                logger.info(f"决策: 召唤 (金币{gold}>={summon_cost})")
                return self.ACTION_SUMMON, {"phase": phase, "cost": summon_cost}

        # ③ 检查是否需要合成腾空位后召唤
        if not can_summon and "格位已满" in summon_reason:
            # 检查合成后是否能召唤（需要金币够 + 星级未达标）
            if gold >= summon_cost:
                if stop_npc and stop_star > 0 and baofeng_star >= stop_star:
                    # 星级已达标，不合成
                    logger.info(f"决策: 暴风星级阻断，不合成 (baofeng={baofeng_star}>={stop_star})")
                else:
                    # 尝试非保护合成
                    can_merge, merge_npc = self._check_merge(npcs, include_protected=False)
                    if can_merge:
                        logger.info(f"决策: 合成非保护腾空位 -> 召唤")
                        return self.ACTION_MERGE, {"phase": phase, "npc": merge_npc}

                    # 尝试保护合成
                    can_merge, merge_npc = self._check_merge(npcs, include_protected=True)
                    if can_merge:
                        logger.info(f"决策: 合成保护腾空位 -> 召唤")
                        return self.ACTION_MERGE_PROTECTED, {"phase": phase, "npc": merge_npc}

        # ④ 等待
        logger.info("决策: 等待")
        return self.ACTION_WAIT, {"reason": "nothing_possible"}

    def _check_merge(self, npcs: List, include_protected: bool = False) -> Tuple[bool, Optional[dict]]:
        """
        检查是否有可合成的 NPC 对。

        Args:
            npcs: NPC 列表
            include_protected: 是否包含保护 NPC

        Returns:
            (是否有可合成, NPC信息)
        """
        # 统计同名同星的 NPC
        npc_counts = {}
        for npc in npcs:
            if npc.name == "kongwei":
                continue
            key = (npc.name, npc.star)
            if key not in npc_counts:
                npc_counts[key] = []
            npc_counts[key].append(npc)

        # 查找可合并的对
        for (name, star), items in npc_counts.items():
            if len(items) >= 2:
                # 检查是否允许合成
                is_protected = self.merge_strategy.is_protected(name, star)

                if not is_protected:
                    # 非保护 NPC，直接允许
                    return True, {"name": name, "star": star}

                if include_protected and is_protected:
                    # 保护 NPC，仅允许低星级（1星）
                    if star == 1:
                        return True, {"name": name, "star": star}

        return False, None

    def _check_merge_zhizhu(self, npcs: List) -> Tuple[bool, Optional[dict]]:
        """
        检查是否有可合成的蜘蛛对（不限星级）。

        Args:
            npcs: NPC 列表

        Returns:
            (是否有可合成, NPC信息)
        """
        # 统计同名同星的 NPC
        npc_counts = {}
        for npc in npcs:
            if npc.name == "kongwei":
                continue
            key = (npc.name, npc.star)
            if key not in npc_counts:
                npc_counts[key] = []
            npc_counts[key].append(npc)

        # 查找可合并的蜘蛛
        for (name, star), items in npc_counts.items():
            if name == "zhizhu" and len(items) >= 2:
                return True, {"name": name, "star": star}

        return False, None
