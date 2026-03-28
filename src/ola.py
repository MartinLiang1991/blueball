import time
import logging
import ctypes
from typing import Optional, Tuple, List, Dict

from olaplug import OLAPlugServer

logger = logging.getLogger(__name__)


class OLA:
    """OLA 插件统一封装层"""

    def __init__(self, config):
        self.config = config
        self.server = OLAPlugServer()
        # 注册 OLA 插件
        ret = self.server.Reg(
            self.server.UserCode,
            self.server.SoftCode,
            self.server.FeatureList
        )
        if ret != 1:
            raise RuntimeError(f"OLA 注册失败，返回值: {ret}")
        self._hwnd: int = 0
        self._running = False

    @property
    def hwnd(self) -> int:
        return self._hwnd

    @property
    def is_bound(self) -> bool:
        return self._hwnd != 0

    def find_window(self) -> int:
        """查找游戏窗口"""
        hwnd = self.server.FindWindow(
            self.config.window_class_name,
            self.config.window_title
        )
        logger.error(hwnd)
        return hwnd

    def bind_window(self) -> bool:
        """绑定游戏窗口"""
        hwnd = self.find_window()
        if hwnd == 0:
            logger.error("未找到游戏窗口")
            return False
        self._hwnd = hwnd
        ret = self.server.BindWindow(
            hwnd,
            self.config.bind_display,
            self.config.bind_mouse,
            self.config.bind_keypad,
            self.config.bind_mode
        )
        if ret != 1:
            logger.error(f"绑定窗口失败，返回值: {ret}")
            return False
        self._running = True
        logger.info(f"窗口绑定成功，hwnd={hwnd}")
        return True

    def unbind_window(self):
        """解绑窗口"""
        if self.is_bound:
            self.server.UnBindWindow()
            self._hwnd = 0
            self._running = False
            logger.info("窗口已解绑")

    def get_client_rect(self) -> Tuple[int, int, int, int]:
        """获取窗口客户区坐标 (x1, y1, x2, y2)"""
        return self.server.GetClientRect(self._hwnd)

    # ==================== 截图 ====================

    def capture(self, x1: int, y1: int, x2: int, y2: int, file: str = "") -> int:
        """截图到文件"""
        return self.server.Capture(x1, y1, x2, y2, file)

    def capture_region_bmp(self, x1: int, y1: int, x2: int, y2: int) -> Optional[bytes]:
        """截取区域并返回 BMP 数据 (bytes)"""
        data_ptr, data_len, ret = self.server.GetScreenDataBmp(x1, y1, x2, y2)
        if ret != 1 or data_ptr == 0:
            return None
        bmp_data = self.server.GetImageBmpData(data_ptr)
        self.server.FreeImageData(data_ptr)
        if isinstance(bmp_data, tuple):
            # 返回格式可能是 (ptr, size, ret)
            if bmp_data[2] == 1 and bmp_data[0] != 0:
                size = bmp_data[1]
                raw_ptr = bmp_data[0]
                buf = (ctypes.c_ubyte * size)()
                ctypes.memmove(buf, raw_ptr, size)
                return bytes(buf)
            return None
        return bmp_data if bmp_data else None

    def capture_to_numpy(self, x1: int, y1: int, x2: int, y2: int):
        """截取区域并返回 numpy BGR 数组 (用于 YOLO)"""
        try:
            import cv2
            import numpy as np
        except ImportError:
            logger.error("需要安装 opencv-python 和 numpy")
            return None

        data_ptr, data_len, stride, ret = self.server.GetScreenData(x1, y1, x2, y2)
        if ret != 1 or data_ptr == 0:
            return None

        width = x2 - x1
        height = y2 - y1
        buf = (ctypes.c_ubyte * (stride * height))()
        ctypes.memmove(buf, data_ptr, stride * height)
        self.server.FreeImageData(data_ptr)

        arr = np.frombuffer(buf, dtype=np.uint8).reshape((height, stride // 3, 3))
        # 截取实际宽度（stride 可能包含对齐填充）
        arr = arr[:, :width, :]
        return arr

    # ==================== 找图 ====================

    def find_template(self, x1: int, y1: int, x2: int, y2: int,
                      template_path: str, threshold: float = 0.8) -> Optional[Dict]:
        """在指定区域找图，返回匹配结果 {x, y, w, h, score} 或 None"""
        result = self.server.MatchWindowsFromPath(
            x1, y1, x2, y2, template_path, threshold, 0, 0.0, 1.0
        )
        if not result:
            return None
        return result

    def template_exists(self, x1: int, y1: int, x2: int, y2: int,
                        template_path: str, threshold: float = 0.8) -> bool:
        """判断指定区域是否存在模板图片"""
        return self.find_template(x1, y1, x2, y2, template_path, threshold) is not None

    # ==================== OCR ====================

    def ocr(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """OCR 识别指定区域的文字"""
        return self.server.Ocr(x1, y1, x2, y2)

    def ocr_v5(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """OCR V5 识别指定区域的文字"""
        return self.server.OcrV5(x1, y1, x2, y2)

    # ==================== 鼠标操作 ====================

    def move_to(self, x: int, y: int):
        """移动鼠标到指定坐标"""
        self.server.MoveTo(x, y)

    def left_click(self, x: int, y: int = None):
        """左键单击"""
        if y is not None:
            self.move_to(x, y)
        self.server.LeftClick()

    def left_down(self):
        """左键按下"""
        self.server.LeftDown()

    def left_up(self):
        """左键抬起"""
        self.server.LeftUp()

    def drag(self, x1: int, y1: int, x2: int, y2: int,
             down_delay: int = 50, move_delay: int = 80, up_delay: int = 50):
        """拖拽操作：从 (x1,y1) 拖到 (x2,y2)"""
        self.move_to(x1, y1)
        self.server.Delay(down_delay)
        self.left_down()
        self.server.Delay(move_delay)
        self.move_to(x2, y2)
        self.server.Delay(up_delay)
        self.left_up()

    # ==================== 键盘操作 ====================

    def key_press(self, vk_code: int):
        """按键"""
        self.server.KeyPress(vk_code)

    def key_press_char(self, key_str: str):
        """按键（字符方式）"""
        self.server.KeyPressChar(key_str)

    # ==================== 延时 ====================

    def delay(self, ms: int):
        """延时（毫秒）"""
        self.server.Delay(ms)

    def delay_random(self, min_ms: int, max_ms: int):
        """随机延时"""
        self.server.Delays(min_ms, max_ms)

    def sleep(self, seconds: float):
        """Python sleep（秒）"""
        time.sleep(seconds)

    # ==================== 热键 ====================

    def start_hotkey_hook(self):
        self.server.StartHotkeyHook()

    def register_hotkey(self, keycode: int, modifiers: int, callback):
        self.server.RegisterHotkey(keycode, modifiers, callback)

    # ==================== 清理 ====================

    def cleanup(self):
        """释放资源"""
        self.unbind_window()
        self.server.ReleaseObj()
        logger.info("OLA 资源已释放")
