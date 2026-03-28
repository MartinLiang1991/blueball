import logging

logger = logging.getLogger(__name__)


class UICheck:
    """UI 校验模块：通过 OCR 判断当前处于哪个界面"""

    def __init__(self, config, ola):
        self.config = config
        self.ola = ola

        region = config.get_region("主界面校验")
        self._x1 = region.x1
        self._y1 = region.y1
        self._x2 = region.x2
        self._y2 = region.y2
        self._角色名 = config.data.get("角色名", "")

    def is_main_screen(self) -> bool:
        """
        判断当前 UI 是否处于主界面。

        通过 OCR 识别"主界面校验"区域是否包含角色名来判断。

        Returns:
            True 表示在主界面，False 表示不在主界面
        """
        if not self._角色名:
            logger.warning("未配置角色名，无法校验主界面")
            return False

        try:
            text = self.ola.ocr(self._x1, self._y1, self._x2, self._y2)
            if not text or not text.strip():
                logger.debug("主界面校验区域 OCR 结果为空")
                return False

            found = self._角色名 in text.strip()
            logger.debug(f"主界面校验: OCR='{text.strip()}', 包含'{self._角色名}'={found}")
            return found

        except Exception as e:
            logger.error(f"主界面校验异常: {e}")
            return False

    def get_ocr_text(self) -> str:
        """获取主界面校验区域的 OCR 识别结果"""
        try:
            text = self.ola.ocr(self._x1, self._y1, self._x2, self._y2)
            return text.strip() if text else ""
        except Exception as e:
            logger.error(f"获取 OCR 文本异常: {e}")
            return ""
