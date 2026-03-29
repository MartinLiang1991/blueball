import logging
import time

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

    def return_to_main(self, max_attempts: int = 20) -> bool:
        """
        点击返回主界面按钮，直到回到主界面。

        Args:
            max_attempts: 最大尝试次数，默认 10 次

        Returns:
            True 表示成功回到主界面，False 表示超时
        """
        btn_x, btn_y = self.config.get_button("返回主界面")
        if btn_x == 0 and btn_y == 0:
            logger.error("未配置返回主界面按钮坐标")
            return False

        for attempt in range(1, max_attempts + 1):
            logger.info(f"返回主界面尝试 {attempt}/{max_attempts}")
            # 点击返回按钮
            self.ola.left_click(btn_x, btn_y)
            # 等待界面切换
            self.ola.server.Delay(1000)
            # 检测是否在主界面
            if self.is_main_screen():
                logger.info("已成功返回主界面")
                return True

        logger.warning(f"超过最大尝试次数 {max_attempts}，未能返回主界面")
        return False

    def find_team(self, max_attempts: int = 30) -> str:
        """
        自动找队伍：回到主界面 -> 点击聊天 -> 点击招募 -> 识别队伍标题

        Args:
            max_attempts: 最大循环尝试次数，默认 10 次

        Returns:
            队伍招募标题 OCR 结果，失败返回空字符串
        """
        chat_x, chat_y = self.config.get_button("主界面聊天")
        if chat_x == 0 and chat_y == 0:
            logger.error("未配置主界面聊天按钮坐标")
            return ""

        # 获取组队招募文字区域坐标
        recruit_text_region = self.config.get_region("组队招募文字")
        # 获取组队招募标题区域坐标
        recruit_title_region = self.config.get_region("组队招募标题")

        for attempt in range(1, max_attempts + 1):
            logger.info(f"找队伍尝试 {attempt}/{max_attempts}")

            # 1. 回到主界面
            if not self.is_main_screen():
                logger.info("当前不在主界面，先返回主界面")
                if not self.return_to_main():
                    logger.error("返回主界面失败")
                    continue
                self.ola.server.Delay(500)

            # 2. 点击主界面聊天按钮
            logger.info("点击主界面聊天按钮")
            self.ola.left_click(chat_x, chat_y)
            self.ola.server.Delay(800)

            # 3. OCR 识别"组队招募文字"区域
            recruit_text = self.ola.ocr(
                recruit_text_region.x1, recruit_text_region.y1,
                recruit_text_region.x2, recruit_text_region.y2
            )
            recruit_text = recruit_text.strip() if recruit_text else ""
            logger.info(f"组队招募文字 OCR 结果: '{recruit_text}'")

            # 4. 判断是否为"招募"
            if "招募" in recruit_text:
                # 点击招募文字区域（使用区域中心坐标）
                recruit_x = (recruit_text_region.x1 + recruit_text_region.x2) // 2
                recruit_y = (recruit_text_region.y1 + recruit_text_region.y2) // 2
                logger.info(f"点击招募")
                self.ola.left_click(recruit_x, recruit_y)

                # 5. 循环 OCR 识别"组队招募标题"区域，每隔 300ms 一次
                while True:
                    self.ola.server.Delay(300)

                    title_text = self.ola.ocr(
                        recruit_title_region.x1, recruit_title_region.y1,
                        recruit_title_region.x2, recruit_title_region.y2
                    )
                    title_text = title_text.strip() if title_text else ""
                    logger.info(f"组队招募标题 OCR 结果: '{title_text}'")

                    # 6. 判断标题是否包含目标模式
                    target_patterns = ["合作模式-彩虹1层", "合作模式-彩虹2层", "合作模式-彩虹3层"]
                    is_target = any(pattern in title_text for pattern in target_patterns)

                    if not is_target:
                        # 未找到符合条件的队伍，继续循环 OCR
                        logger.info("未找到符合条件的队伍，继续等待...")
                        continue

                    # 找到目标队伍，点击加入按钮
                    logger.info("检测到目标队伍，点击加入按钮")
                    join_x, join_y = self.config.get_button("加入")
                    if join_x != 0 or join_y != 0:
                        # 点击加入按钮
                        self.ola.left_click(join_x, join_y)
                        self.ola.server.Delay(100)

                        # 检查是否成功加入队伍
                        # 如果"组队招募文字"区域识别不到文字，或文字不等于"招募"，则成功
                        recruit_check = self.ola.ocr(
                            recruit_text_region.x1, recruit_text_region.y1,
                            recruit_text_region.x2, recruit_text_region.y2
                        )
                        recruit_check = recruit_check.strip() if recruit_check else ""

                        if not recruit_check or recruit_check != "招募":
                            logger.info("已成功加入队伍或进入游戏界面")
                            return title_text
                        else:
                            logger.info("加入队伍失败，继续尝试")
                            # 继续循环 OCR 寻找下一个队伍
                    else:
                        logger.warning("未配置加入按钮坐标")
                        break
            else:
                logger.info("未找到招募按钮，重新尝试")
                self.ola.server.Delay(500)

        logger.warning(f"超过最大尝试次数 {max_attempts}，未能找到队伍")
        return ""

    def is_in_battle(self) -> bool:
        """
        判断当前 UI 是否处于战斗界面。

        通过 OCR 识别"战斗界面校验"区域是否等于角色名来判断。

        Returns:
            True 表示在战斗界面，False 表示不在战斗界面
        """
        if not self._角色名:
            logger.warning("未配置角色名，无法校验战斗界面")
            return False

        try:
            region = self.config.get_region("战斗界面校验")
            text = self.ola.ocr(region.x1, region.y1, region.x2, region.y2)
            if not text or not text.strip():
                logger.debug("战斗界面校验区域 OCR 结果为空")
                return False

            is_battle = text.strip() == self._角色名
            logger.debug(f"战斗界面校验: OCR='{text.strip()}', 等于'{self._角色名}'={is_battle}")
            return is_battle

        except Exception as e:
            logger.error(f"战斗界面校验异常: {e}")
            return False

    def check_battle_end(self) -> bool:
        """
        检查战斗是否结束。

        进行双重校验（OCR + is_in_battle），重复3次。
        每次校验前都点击"防遮盖"按钮两次（间隔1秒），避免遮盖导致识别错误。
        只有3次都识别到战斗结束，才认为真的战斗结束。

        Returns:
            True 表示战斗已结束，False 表示战斗未结束
        """
        try:
            # 获取防遮盖按钮坐标
            防遮盖_x, 防遮盖_y = self.config.get_button("防遮盖")
            logger.info(f"防遮盖按钮坐标: ({防遮盖_x}, {防遮盖_y})")

            # 双重校验重复3次
            for i in range(3):
                logger.info(f"===== 战斗结束校验 第 {i+1}/3 次 =====")
                # 每次校验前点击防遮盖按钮两次
                if 防遮盖_x > 0 and 防遮盖_y > 0:
                    logger.info(f"点击防遮盖按钮 #1: ({防遮盖_x}, {防遮盖_y})")
                    self.ola.left_click(防遮盖_x, 防遮盖_y)
                    time.sleep(1)
                    logger.info(f"点击防遮盖按钮 #2: ({防遮盖_x}, {防遮盖_y})")
                    self.ola.left_click(防遮盖_x, 防遮盖_y)
                    time.sleep(0.5)
                else:
                    logger.warning(f"防遮盖按钮坐标无效: ({防遮盖_x}, {防遮盖_y}), 跳过点击")

                # 只用 is_in_battle 检查（角色名是否显示）判断是否离开战斗
                not_in_battle = not self.is_in_battle()
                logger.info(f"是否不在战斗界面: {not_in_battle}")

                # 校验通过
                if not_in_battle:
                    logger.info(f"第 {i+1} 次校验通过")
                    if i < 2:
                        # 不是最后一次，等待后继续校验
                        time.sleep(2)
                    continue
                else:
                    logger.info(f"第 {i+1} 次校验失败, 返回 False")
                    return False

            # 3次都通过，认为战斗结束
            logger.info("战斗结束校验: 3次校验均通过，确认战斗结束")

            # 循环点击"战斗结束"按钮并尝试返回主界面
            战斗结束_x, 战斗结束_y = self.config.get_button("战斗结束")
            if 战斗结束_x > 0 and 战斗结束_y > 0:
                for i in range(10):
                    logger.info(f"点击战斗结束按钮 #{i+1}: ({战斗结束_x}, {战斗结束_y})")
                    self.ola.left_click(战斗结束_x, 战斗结束_y)
                    time.sleep(1)
                    # 尝试返回主界面
                    if self.return_to_main(20):
                        logger.info("已成功返回主界面")
                        return True
                logger.warning("尝试多次后未能返回主界面")
            else:
                logger.warning(f"战斗结束按钮坐标无效: ({战斗结束_x}, {战斗结束_y})")

            return True

        except Exception as e:
            logger.error(f"战斗结束校验异常: {e}")
            return False

    def is_ready(self) -> bool:
        """
        检查是否处于队伍中待准备状态。

        通过 OCR 识别"准备检测"区域是否包含"本次"或"准备"来判断。

        Returns:
            True 表示在待准备状态，False 表示不在待准备状态
        """
        try:
            region = self.config.get_region("准备检测")
            text = self.ola.ocr(region.x1, region.y1, region.x2, region.y2)
            if not text or not text.strip():
                logger.debug("准备检测区域 OCR 结果为空")
                return False

            is_ready = "本次" in text.strip() or "准备" in text.strip()
            logger.debug(f"准备检测: OCR='{text.strip()}', 包含'本次'或'准备'={is_ready}")
            return is_ready

        except Exception as e:
            logger.error(f"准备检测异常: {e}")
            return False
