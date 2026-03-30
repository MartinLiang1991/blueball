import json
import os
import logging
from dataclasses import dataclass, field
from typing import Dict, Any

logger = logging.getLogger(__name__)


@dataclass
class Region:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    def contains(self, x: int, y: int) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2


@dataclass
class TimingConfig:
    battle_loop_interval: float = 2.0
    merge_wait: float = 0.3
    summon_wait: float = 0.5
    state_check_interval: float = 3.0
    match_timeout: int = 60
    battle_timeout: int = 600
    settlement_timeout: int = 30


@dataclass
class SummonConfig:
    base_cost: int = 1
    cost_increment: int = 1
    initial_slots: int = 7
    slots_per_summons: int = 5
    cost_table: list = None

    def __post_init__(self):
        if self.cost_table is None:
            self.cost_table = []

    def get_cost(self, summon_count: int) -> int:
        """获取召唤费用，优先使用费用表"""
        if self.cost_table and summon_count < len(self.cost_table):
            return self.cost_table[summon_count]
        # 降级使用旧公式
        return self.base_cost + summon_count * self.cost_increment

    def get_slot_count(self, summon_count: int) -> int:
        return self.initial_slots + (summon_count // self.slots_per_summons)


@dataclass
class YoloConfig:
    model_path: str = "yolov8/best.pt"
    confidence: float = 0.5
    img_size: int = 640


@dataclass
class ProtectedNPC:
    """受保护的 NPC 配置"""
    name: str
    star: int


@dataclass
class MergeStrategyConfig:
    protected: list = field(default_factory=list)
    max_star: int = 4

    def is_protected(self, name: str, star: int) -> bool:
        """检查 NPC 是否受保护"""
        for p in self.protected:
            if isinstance(p, dict):
                if p.get("name") == name and p.get("star") == star:
                    return True
            elif isinstance(p, ProtectedNPC):
                if p.name == name and p.star == star:
                    return True
        return False


class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.config_path):
            logger.warning(f"配置文件不存在: {self.config_path}，使用默认配置")
            self._data = {}
            return
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
        logger.info(f"配置已加载: {self.config_path}")

    @property
    def window_title(self) -> str:
        return self._data.get("window", {}).get("title", "")

    @property
    def window_class_name(self) -> str:
        return self._data.get("window", {}).get("class_name", "")

    @property
    def process_name(self) -> str:
        return self._data.get("window", {}).get("process_name", "")

    @property
    def bind_display(self) -> str:
        return self._data.get("bind", {}).get("display", "gdi")

    @property
    def bind_mouse(self) -> str:
        return self._data.get("bind", {}).get("mouse", "windows")

    @property
    def bind_keypad(self) -> str:
        return self._data.get("bind", {}).get("keypad", "windows")

    @property
    def bind_mode(self) -> int:
        return self._data.get("bind", {}).get("mode", 0)

    def get_region(self, name: str) -> Region:
        r = self._data.get("regions", {}).get(name, {})
        return Region(
            x1=r.get("x1", 0), y1=r.get("y1", 0),
            x2=r.get("x2", 0), y2=r.get("y2", 0)
        )

    def get_template_path(self, name: str) -> str:
        return self._data.get("templates", {}).get(name, "")

    def get_button(self, name: str) -> tuple[int, int]:
        """获取按钮坐标，返回 (x, y)"""
        btn = self._data.get("buttons", {}).get(name, {})
        return btn.get("x", 0), btn.get("y", 0)

    @property
    def match_threshold(self) -> float:
        return self._data.get("match_threshold", 0.8)

    @property
    def summon(self) -> SummonConfig:
        s = self._data.get("召唤", {})
        return SummonConfig(
            base_cost=s.get("base_cost", 1),
            cost_increment=s.get("cost_increment", 1),
            initial_slots=s.get("初始格位", 7),
            slots_per_summons=s.get("每次新增格位召唤次数", 5),
            cost_table=s.get("费用表", [])
        )

    @property
    def timing(self) -> TimingConfig:
        t = self._data.get("timing", {})
        return TimingConfig(
            battle_loop_interval=t.get("battle_loop_interval", 2.0),
            merge_wait=t.get("merge_wait", 0.3),
            summon_wait=t.get("summon_wait", 0.5),
            state_check_interval=t.get("state_check_interval", 3.0),
            match_timeout=t.get("match_timeout", 60),
            battle_timeout=t.get("battle_timeout", 600),
            settlement_timeout=t.get("settlement_timeout", 30)
        )

    @property
    def yolo(self) -> YoloConfig:
        y = self._data.get("yolo", {})
        return YoloConfig(
            model_path=y.get("model_path", "yolov8/best.pt"),
            confidence=y.get("confidence", 0.5),
            img_size=y.get("img_size", 640)
        )

    @property
    def log_level(self) -> str:
        return self._data.get("log_level", "INFO")

    @property
    def merge_strategy(self) -> MergeStrategyConfig:
        m = self._data.get("merge_strategy", {})
        return MergeStrategyConfig(
            protected=m.get("protected", []),
            max_star=m.get("max_star", 4)
        )

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    @property
    def enhance_cost_table(self) -> list:
        """强化费用表，如 [100, 200, 400, 600, 1000, 1500, 1800, 2500, 3000, 3500]"""
        return self._data.get("强化费用表", [])

    @property
    def card_priority(self) -> dict:
        """卡牌词条优先级，如 {"千刃横飞": 1, "终焉风狱": 2, ...}"""
        return self._data.get("词条优先级", {})
