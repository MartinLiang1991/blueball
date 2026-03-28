import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)


class State(Enum):
    """游戏状态枚举"""
    IDLE = auto()          # 空闲/未初始化
    LOBBY = auto()         # 大厅
    MATCHING = auto()      # 匹配中
    BATTLE = auto()        # 副本战斗中
    SETTLEMENT = auto()    # 结算中
    STOPPED = auto()       # 已停止


class StateManager:
    """状态机管理器"""

    def __init__(self):
        self._state = State.IDLE
        self._listeners = []

    @property
    def state(self) -> State:
        return self._state

    def set_state(self, new_state: State):
        old_state = self._state
        if old_state == new_state:
            return
        self._state = new_state
        logger.info(f"状态转换: {old_state.name} -> {new_state.name}")
        for listener in self._listeners:
            try:
                listener(old_state, new_state)
            except Exception as e:
                logger.error(f"状态监听器异常: {e}")

    def add_listener(self, callback):
        """注册状态变更监听器 callback(old_state, new_state)"""
        self._listeners.append(callback)

    def is_battle_state(self) -> bool:
        return self._state == State.BATTLE

    def is_running(self) -> bool:
        return self._state not in (State.IDLE, State.STOPPED)
