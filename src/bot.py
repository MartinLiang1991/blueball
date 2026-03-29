import time
import logging
from typing import Optional

from .config import Config
from .ola import OLA
from .state import State, StateManager
from .detector import YOLODetector
from .gold import GoldDetector
from .merge import MergeModule
from .summon import SummonModule

logger = logging.getLogger(__name__)


class GameBot:
    """游戏自动化主控制器"""

    def __init__(self, config: Config):
        self.config = config
        self.state_mgr = StateManager()
        self._stop_requested = False

        # 模块（延迟初始化）
        self.ola: Optional[OLA] = None
        self.detector: Optional[YOLODetector] = None
        self.gold_detector: Optional[GoldDetector] = None
        self.merge_module: Optional[MergeModule] = None
        self.summon_module: Optional[SummonModule] = None

        # 统计
        self._battle_count = 0

    def init(self) -> bool:
        """初始化所有模块"""
        logger.info("初始化 GameBot...")

        # 初始化 OLA
        self.ola = OLA(self.config)
        if not self.ola.bind_window():
            logger.error("OLA 绑窗失败")
            return False

        # 初始化 YOLO
        try:
            self.detector = YOLODetector(self.config)
        except Exception as e:
            logger.error(f"YOLO 初始化失败: {e}")
            return False

        # 初始化子模块
        self.gold_detector = GoldDetector(self.config, self.ola)
        self.merge_module = MergeModule(self.config, self.ola)
        self.summon_module = SummonModule(self.config, self.ola)

        # 注册热键
        self._register_hotkeys()

        self.state_mgr.set_state(State.LOBBY)
        logger.info("GameBot 初始化完成")
        return True

    def _register_hotkeys(self):
        """注册全局热键"""
        from olaplug import VirtualKey
        self.ola.start_hotkey_hook()

        def on_stop(key, modifiers):
            logger.info("收到停止热键 (F12)，准备停止...")
            self._stop_requested = True

        # F12 = 0x7B
        self.ola.register_hotkey(0x7B, 0, on_stop)
        logger.info("热键已注册: F12 停止")

    def stop(self):
        """请求停止"""
        self._stop_requested = True
        self.state_mgr.set_state(State.STOPPED)

    def run(self):
        """运行主循环"""
        logger.info("=" * 50)
        logger.info("GameBot 启动，按 F12 停止")
        logger.info("=" * 50)

        while not self._stop_requested:
            current_state = self.state_mgr.state

            if current_state == State.LOBBY:
                self._handle_lobby()

            elif current_state == State.MATCHING:
                self._handle_matching()

            elif current_state == State.BATTLE:
                self._handle_battle()

            elif current_state == State.SETTLEMENT:
                self._handle_settlement()

            elif current_state == State.STOPPED:
                break

            else:
                logger.warning(f"未知状态: {current_state}")
                self.state_mgr.set_state(State.LOBBY)

        self._cleanup()
        logger.info("GameBot 已停止")

    # ==================== 状态处理 ====================

    def _handle_lobby(self):
        """大厅状态处理"""
        logger.info("当前状态: 大厅")

        # 检测是否在大厅（找图匹配）
        if self._check_in_lobby():
            logger.info("检测到在大厅，准备匹配...")
            if self._click_match_button():
                self.state_mgr.set_state(State.MATCHING)
            else:
                logger.warning("未找到匹配按钮")
                self.ola.sleep(self.config.timing.state_check_interval)
        else:
            # 可能还在结算或加载中
            logger.info("未检测到大厅标志，等待中...")
            self.ola.sleep(self.config.timing.state_check_interval)

    def _handle_matching(self):
        """匹配状态处理"""
        logger.info("当前状态: 匹配中")

        start_time = time.time()
        timeout = self.config.timing.match_timeout

        while not self._stop_requested:
            if time.time() - start_time > timeout:
                logger.warning("匹配超时")
                self.state_mgr.set_state(State.LOBBY)
                return

            # 检测是否已进入副本
            if self._check_in_battle():
                self.summon_module.reset_count()
                self.state_mgr.set_state(State.BATTLE)
                self._battle_count += 1
                logger.info(f"进入副本 (第 {self._battle_count} 次)")
                return

            self.ola.sleep(self.config.timing.state_check_interval)

    def _handle_battle(self):
        """战斗状态处理"""
        timing = self.config.timing
        npc_region = self.config.get_region("npc_area")
        interval = timing.battle_loop_interval
        battle_start = time.time()
        timeout = timing.battle_timeout

        logger.info("战斗开始，进入召唤+合成循环")

        # 初始化阶段：连续召唤7次快速填满空位
        if self.summon_module.summon_count == 0:
            logger.info("初始化阶段，连续召唤7次填满空位")
            init_summon_count = 7
            for i in range(init_summon_count):
                # 直接召唤，无需检查金币
                self.summon_module.execute_summon([])
                logger.info(f"初始化召唤 {i+1}/{init_summon_count}")
                self.ola.sleep(interval)
            # 初始化召唤完成，等待一下让NPC出现
            self.ola.sleep(interval)

        while not self._stop_requested:
            # 超时检测
            if time.time() - battle_start > timeout:
                logger.warning(f"战斗超时 ({timeout}s)")
                break

            # 检测战斗是否结束
            if self._check_battle_end():
                logger.info("战斗结束")
                self.state_mgr.set_state(State.SETTLEMENT)
                return

            # 1. 截图 NPC 区域 → YOLO 检测
            frame = self.ola.capture_to_numpy(
                npc_region.x1, npc_region.y1, npc_region.x2, npc_region.y2
            )
            if frame is None:
                logger.warning("截图失败，跳过本次循环")
                self.ola.sleep(interval)
                continue

            npcs = self.detector.detect(frame, npc_region)
            logger.info(f"当前 NPC 数量: {len(npcs)}")

            # 2. 识别金钱
            gold = self.gold_detector.detect()
            logger.info(f"当前金钱: {gold}")

            # 3. 合成：找到可合成配对并执行
            # 3a. 先尝试合成非保护 NPC
            merge_count = self.merge_module.merge_all(npcs, include_protected=False)
            if merge_count > 0:
                # 合成后需要重新检测（NPC 数量/位置变化）
                logger.info(f"执行了 {merge_count} 次合成，等待后重新检测")
                self.ola.sleep(interval)
                continue

            # 3b. 如果没有可合成的，且格位满无法召唤，再尝试合成保护 NPC
            can_summon, reason = self.summon_module.can_summon(gold, npcs)
            if not can_summon and "格位" in reason:
                logger.info("格位已满且无其他可合成，尝试合成保护 NPC")
                merge_count = self.merge_module.merge_all(npcs, include_protected=True)
                if merge_count > 0:
                    logger.info(f"执行了 {merge_count} 次保护 NPC 合成，等待后重新检测")
                    self.ola.sleep(interval)
                    continue

            # 4. 召唤：判断是否可召唤
            if can_summon:
                self.summon_module.execute_summon(npcs)
                # 召唤后等待新 NPC 出现
                self.ola.sleep(interval)
                continue
            else:
                logger.debug(f"不召唤: {reason}")

            # 5. 无操作可做，等待下一轮
            self.ola.sleep(interval)

    def _handle_settlement(self):
        """结算状态处理"""
        logger.info("当前状态: 结算中")

        start_time = time.time()
        timeout = self.config.timing.settlement_timeout

        while not self._stop_requested:
            if time.time() - start_time > timeout:
                logger.warning("结算超时")
                break

            # 检测是否回到大厅
            if self._check_in_lobby():
                logger.info("已回到大厅")
                self.state_mgr.set_state(State.LOBBY)
                return

            self.ola.sleep(self.config.timing.state_check_interval)

        # 超时也尝试回到大厅
        self.state_mgr.set_state(State.LOBBY)

    # ==================== 状态检测 ====================

    def _check_in_lobby(self) -> bool:
        """检测是否在大厅"""
        template_path = self.config.get_template_path("lobby")
        if not template_path:
            # 未配置模板，假设在大厅
            return True

        x1, y1, x2, y2 = self.ola.get_client_rect()
        return self.ola.template_exists(x1, y1, x2, y2, template_path, self.config.match_threshold)

    def _check_in_battle(self) -> bool:
        """检测是否已进入副本（战斗界面）"""
        # 通过检测 NPC 区域是否有 NPC 来判断
        npc_region = self.config.get_region("npc_area")
        frame = self.ola.capture_to_numpy(
            npc_region.x1, npc_region.y1, npc_region.x2, npc_region.y2
        )
        if frame is None:
            return False

        npcs = self.detector.detect(frame, npc_region)
        if len(npcs) > 0:
            logger.info(f"检测到 {len(npcs)} 个 NPC，确认已进入副本")
            return True
        return False

    def _check_battle_end(self) -> bool:
        """检测战斗是否结束"""
        template_path = self.config.get_template_path("battle_end")
        if not template_path:
            return False

        x1, y1, x2, y2 = self.ola.get_client_rect()
        return self.ola.template_exists(x1, y1, x2, y2, template_path, self.config.match_threshold)

    def _click_match_button(self) -> bool:
        """点击匹配按钮"""
        template_path = self.config.get_template_path("match_btn")
        if not template_path:
            logger.warning("未配置匹配按钮模板")
            return False

        x1, y1, x2, y2 = self.ola.get_client_rect()
        result = self.ola.find_template(x1, y1, x2, y2, template_path, self.config.match_threshold)
        if not result:
            return False

        bx = result.get("x", 0) + result.get("w", 0) // 2
        by = result.get("y", 0) + result.get("h", 0) // 2
        logger.info(f"点击匹配按钮 ({bx}, {by})")
        self.ola.left_click(bx, by)
        self.ola.delay(1000)
        return True

    # ==================== 清理 ====================

    def _cleanup(self):
        """清理资源"""
        if self.ola:
            self.ola.cleanup()
