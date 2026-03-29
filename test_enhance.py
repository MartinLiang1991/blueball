"""强化模块单元测试"""
import unittest
from unittest.mock import Mock, MagicMock, patch
from src.enhance import EnhanceModule


class MockConfig:
    """模拟配置对象"""
    def __init__(self):
        self.enhance_cost_table = [100, 200, 400, 600, 1000, 1500, 1800, 2500, 3000, 3500]
        self.card_priority = {
            "暴风": 1,
            "闪电": 2,
            "穿透": 3,
        }
        # 模拟按钮坐标
        self._buttons = {
            "强化": (500, 300),
            "中间卡牌": (400, 400),
        }
        # 模拟区域
        self._regions = {
            "开始抽卡识别": MockRegion(100, 100, 200, 150),
            "强化卡牌识别": MockRegion(150, 200, 350, 400),
        }

    def get_button(self, name: str):
        return self._buttons.get(name, (0, 0))

    def get_region(self, name: str):
        return self._regions.get(name, MockRegion(0, 0, 0, 0))


class MockRegion:
    """模拟区域对象"""
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class MockOLA:
    """模拟 OLA 对象"""
    def __init__(self):
        self.called = []

    def left_click(self, x, y):
        self.called.append(("left_click", x, y))

    def delay(self, ms):
        self.called.append(("delay", ms))

    def ocr(self, x1, y1, x2, y2):
        return "请选择"

    def ocr_details(self, x1, y1, x2, y2):
        return None


class TestEnhanceModule(unittest.TestCase):
    """强化模块测试"""

    def setUp(self):
        """测试前准备"""
        self.config = MockConfig()
        self.ola = MockOLA()
        self.enhance = EnhanceModule(self.config, self.ola)

    def test_enhance_count_initial(self):
        """测试初始强化计数为0"""
        self.assertEqual(self.enhance.enhance_count, 0)

    def test_reset_count(self):
        """测试重置强化计数"""
        self.enhance._enhance_count = 5
        self.enhance.reset_count()
        self.assertEqual(self.enhance.enhance_count, 0)

    def test_get_cost(self):
        """测试获取强化费用"""
        # 初始状态，费用为 100
        self.assertEqual(self.enhance.get_cost(), 100)

        # 强化一次后，费用为 200
        self.enhance._enhance_count = 1
        self.assertEqual(self.enhance.get_cost(), 200)

        # 强化五次后，费用为 1000
        self.enhance._enhance_count = 5
        self.assertEqual(self.enhance.get_cost(), 1000)

    def test_get_cost_max_level(self):
        """测试达到最大等级时费用为0"""
        self.enhance._enhance_count = 10  # 超过费用表长度
        self.assertEqual(self.enhance.get_cost(), 0)

    def test_is_unlocked(self):
        """测试强化解锁判断"""
        # 召唤次数 < 7，未解锁
        self.assertFalse(self.enhance.is_unlocked(5))
        self.assertFalse(self.enhance.is_unlocked(6))

        # 召唤次数 >= 7，已解锁
        self.assertTrue(self.enhance.is_unlocked(7))
        self.assertTrue(self.enhance.is_unlocked(10))

    def test_is_max_level(self):
        """测试强化上限判断"""
        # 未达上限
        self.assertFalse(self.enhance.is_max_level())
        self.enhance._enhance_count = 5
        self.assertFalse(self.enhance.is_max_level())

        # 达到上限
        self.enhance._enhance_count = 10
        self.assertTrue(self.enhance.is_max_level())

    def test_can_enhance_not_unlocked(self):
        """测试强化未解锁时不能强化"""
        can_enhance, reason = self.enhance.can_enhance(summon_count=5, gold=1000)
        self.assertFalse(can_enhance)
        self.assertIn("强化未解锁", reason)

    def test_can_enhance_max_level(self):
        """测试强化已达上限时不能强化"""
        self.enhance._enhance_count = 10
        can_enhance, reason = self.enhance.can_enhance(summon_count=10, gold=1000)
        self.assertFalse(can_enhance)
        self.assertIn("强化已达上限", reason)

    def test_can_enhance_not_enough_gold(self):
        """测试金币不足时不能强化"""
        can_enhance, reason = self.enhance.can_enhance(summon_count=10, gold=50)
        self.assertFalse(can_enhance)
        self.assertIn("金币不足", reason)

    def test_can_enhance_success(self):
        """测试可以强化的情况"""
        can_enhance, reason = self.enhance.can_enhance(summon_count=10, gold=500)
        self.assertTrue(can_enhance)
        self.assertIn("可强化", reason)

    def test_execute_enhance_no_button(self):
        """测试未配置强化按钮时返回失败"""
        self.enhance.enhance_btn = (0, 0)
        result = self.enhance.execute_enhance()
        self.assertFalse(result)

    def test_execute_enhance_success(self):
        """测试强化成功执行"""
        self.enhance.ola.ocr = Mock(return_value="请选择")
        result = self.enhance.execute_enhance()

        # 验证点击了强化按钮
        self.assertTrue(any(c[0] == "left_click" and c[1] == 500 and c[2] == 300
                           for c in self.ola.called))

    def test_execute_enhance_ocr_fail(self):
        """测试OCR识别失败时返回失败"""
        self.enhance.ola.ocr = Mock(return_value="")
        result = self.enhance.execute_enhance()
        self.assertFalse(result)

    def test_find_best_card_with_priority(self):
        """测试查找最优卡牌"""
        ocr_result = {
            "words": [
                {"text": "暴风之力", "x": 100, "y": 100},
                {"text": "普通卡牌", "x": 200, "y": 200},
                {"text": "闪电打击", "x": 300, "y": 300},
            ]
        }
        best_card = self.enhance._find_best_card(ocr_result)
        self.assertIsNotNone(best_card)
        self.assertEqual(best_card["text"], "暴风之力")
        self.assertEqual(best_card["priority"], 1)

    def test_find_best_card_second_priority(self):
        """测试第二优先级卡牌"""
        ocr_result = {
            "words": [
                {"text": "普通卡牌1", "x": 100, "y": 100},
                {"text": "闪电打击", "x": 200, "y": 200},
            ]
        }
        best_card = self.enhance._find_best_card(ocr_result)
        self.assertIsNotNone(best_card)
        self.assertEqual(best_card["text"], "闪电打击")
        self.assertEqual(best_card["priority"], 2)

    def test_find_best_card_no_match(self):
        """测试没有匹配卡牌时返回None"""
        ocr_result = {
            "words": [
                {"text": "普通卡牌1", "x": 100, "y": 100},
                {"text": "普通卡牌2", "x": 200, "y": 200},
            ]
        }
        best_card = self.enhance._find_best_card(ocr_result)
        self.assertIsNone(best_card)

    def test_find_best_card_empty_words(self):
        """测试OCR结果为空时返回None"""
        ocr_result = {"words": []}
        best_card = self.enhance._find_best_card(ocr_result)
        self.assertIsNone(best_card)

    def test_click_default_card(self):
        """测试点击默认卡牌"""
        result = self.enhance._click_default_card()
        self.assertTrue(result)
        # 验证点击了中间卡牌按钮
        self.assertTrue(any(c[0] == "left_click" and c[1] == 400 and c[2] == 400
                           for c in self.ola.called))

    def test_click_default_card_no_button(self):
        """测试未配置中间卡牌按钮时返回失败"""
        self.enhance.middle_card_btn = (0, 0)
        result = self.enhance._click_default_card()
        self.assertFalse(result)


class TestEnhanceModuleCostTable(unittest.TestCase):
    """强化费用表测试"""

    def test_default_cost_table(self):
        """测试默认费用表"""
        config = MockConfig()
        config.enhance_cost_table = None
        ola = MockOLA()
        enhance = EnhanceModule(config, ola)

        # 验证默认费用表
        expected = [100, 200, 400, 600, 1000, 1500, 1800, 2500, 3000, 3500]
        self.assertEqual(enhance.cost_table, expected)

    def test_custom_cost_table(self):
        """测试自定义费用表"""
        config = MockConfig()
        config.enhance_cost_table = [50, 100, 200, 300]
        ola = MockOLA()
        enhance = EnhanceModule(config, ola)

        self.assertEqual(enhance.cost_table, [50, 100, 200, 300])
        self.assertEqual(enhance.get_cost(), 50)
        enhance._enhance_count = 2
        self.assertEqual(enhance.get_cost(), 200)


if __name__ == "__main__":
    unittest.main()
