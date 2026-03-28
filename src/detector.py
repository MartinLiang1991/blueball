import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class NPCInfo:
    """NPC 检测结果"""
    name: str           # NPC 种类名（如 "安妮"）
    star: int           # 星级 1-4
    cx: int             # 中心 x（客户区坐标）
    cy: int             # 中心 y（客户区坐标）
    confidence: float   # 置信度
    width: int = 0
    height: int = 0


class YOLODetector:
    """YOLO NPC 检测器"""

    def __init__(self, config):
        self.config = config
        self.yolo_cfg = config.yolo
        self.model = None
        self._class_names: List[str] = []
        self._load_model()

    def _load_model(self):
        try:
            from ultralytics import YOLO
            self.model = YOLO(self.yolo_cfg.model_path)
            self._class_names = list(self.model.names.values())
            logger.info(f"YOLO 模型已加载: {self.yolo_cfg.model_path}，类别数: {len(self._class_names)}")
            logger.info(f"类别列表: {self._class_names}")
        except Exception as e:
            logger.error(f"加载 YOLO 模型失败: {e}")
            raise

    def detect(self, frame, region) -> List[NPCInfo]:
        """
        检测 NPC 区域内的所有 NPC。

        Args:
            frame: numpy BGR 数组（整个截图或 NPC 区域截图）
            region: config.Region，NPC 区域坐标

        Returns:
            NPCInfo 列表，按置信度降序排列
        """
        if self.model is None:
            logger.error("YOLO 模型未加载")
            return []

        try:
            import numpy as np

            # 如果 frame 是完整截图，先裁剪 NPC 区域
            h, w = frame.shape[:2]
            if w > region.width + 10 or h > region.height + 10:
                frame = frame[region.y1:region.y2, region.x1:region.x2]

            results = self.model(
                frame,
                conf=self.yolo_cfg.confidence,
                imgsz=self.yolo_cfg.img_size,
                verbose=False
            )

            npcs = []
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])

                    # 获取类别名称，解析种类和星级
                    class_name = self._class_names[cls_id] if cls_id < len(self._class_names) else f"class_{cls_id}"
                    name, star = self._parse_class_name(class_name)

                    # 计算中心坐标（转换为窗口客户区坐标）
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cx = int((x1 + x2) / 2) + region.x1
                    cy = int((y1 + y2) / 2) + region.y1

                    npcs.append(NPCInfo(
                        name=name,
                        star=star,
                        cx=cx,
                        cy=cy,
                        confidence=conf,
                        width=int(x2 - x1),
                        height=int(y2 - y1)
                    ))

            npcs.sort(key=lambda n: n.confidence, reverse=True)
            logger.debug(f"检测到 {len(npcs)} 个 NPC")
            for npc in npcs:
                logger.debug(f"  {npc.name} {npc.star}星 ({npc.cx}, {npc.cy}) conf={npc.confidence:.2f}")

            return npcs

        except Exception as e:
            logger.error(f"YOLO 推理异常: {e}")
            return []

    @staticmethod
    def _parse_class_name(class_name: str) -> tuple:
        """
        解析 YOLO 类别名称为 (种类名, 星级)。

        假设类别命名格式为 "名称_星级"（如 "安妮_1", "安妮_2"）。
        如果无法解析星级，默认返回 1 星。
        """
        if "_" in class_name:
            parts = class_name.rsplit("_", 1)
            name = parts[0]
            try:
                star = int(parts[1])
                return name, star
            except ValueError:
                pass
        return class_name, 1
