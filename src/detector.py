import logging
from dataclasses import dataclass
from typing import List, Optional

import cv2
import numpy as np

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
        except Exception as e:
            logger.error(f"加载 YOLO 模型失败: {e}")
            raise

    def detect(self, frame, region=None) -> List[NPCInfo]:
        """
        检测 frame 中的所有 NPC。

        Args:
            frame: numpy BGR 数组（直接传入要检测的图片）
            region: 可选，用于坐标偏移。如果 frame 是截取的子区域，
                    传入 region 可将检测坐标转换为窗口客户区坐标

        Returns:
            NPCInfo 列表，按置信度降序排列
        """
        if self.model is None:
            logger.error("YOLO 模型未加载")
            return []

        try:
            # 直接检测，不做额外裁剪
            results = self.model(frame, verbose=False, conf=self.yolo_cfg.confidence)

            # 偏移量：region 用于将局部坐标转换为窗口坐标
            offset_x = region.x1 if region else 0
            offset_y = region.y1 if region else 0

            npcs = []
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])

                    class_name = self._class_names[cls_id] if cls_id < len(self._class_names) else f"class_{cls_id}"
                    name, star = self._parse_class_name(class_name)

                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cx = int((x1 + x2) / 2) + offset_x
                    cy = int((y1 + y2) / 2) + offset_y

                    npcs.append(NPCInfo(
                        name=name, star=star,
                        cx=cx, cy=cy,
                        confidence=conf,
                        width=int(x2 - x1),
                        height=int(y2 - y1)
                    ))

            npcs.sort(key=lambda n: n.confidence, reverse=True)
            logger.debug(f"检测到 {len(npcs)} 个 NPC")
            return npcs

        except Exception as e:
            logger.error(f"YOLO 推理异常: {e}")
            return []

    def detect_file(self, image_path, region=None) -> List[NPCInfo]:
        """
        便捷方法：传入图片路径直接检测。

        Args:
            image_path: 图片文件路径
            region: 可选，坐标偏移
        """
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"无法读取图片: {image_path}")
            return []
        return self.detect(img, region)

    @staticmethod
    def _parse_class_name(class_name: str) -> tuple[str, int]:
        """解析 YOLO 类别名称为 (种类名, 星级)。"""
        import re
        # 先尝试下划线分隔: "安妮_2" → ("安妮", 2)
        if "_" in class_name:
            parts = class_name.rsplit("_", 1)
            try:
                return parts[0], int(parts[1])
            except ValueError:
                pass
        # 再尝试末尾数字: "anni2" → ("anni", 2)
        m = re.match(r"^(.+?)(\d+)$", class_name)
        if m:
            return m.group(1), int(m.group(2))
        return class_name, 1
