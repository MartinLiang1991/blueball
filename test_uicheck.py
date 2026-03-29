"""主界面检测单元测试"""
import time
import logging
from src import Config, OLA, UICheck, YOLODetector
from src.gold import GoldDetector
from src.merge import MergeModule
from src.summon import SummonModule
from src.enhance import EnhanceModule
from src.decision import DecisionModule

# 配置日志输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)


def test_return_to_main():
    """返回主界面测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("返回主界面测试开始\n")

    try:
        result = check.return_to_main(max_attempts=10)
        print(f"返回主界面结果: {'成功' if result else '失败'}")

    finally:
        ola.cleanup()


def test_find_team():
    """自动找队伍测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("自动找队伍测试开始\n")

    try:
        result = check.find_team(max_attempts=10)
        print(f"\n找队伍结果: '{result}'")

    finally:
        ola.cleanup()


def test_battle_check():
    """战斗界面检测测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("战斗界面检测测试开始，每2秒检测一次，按 Ctrl+C 退出\n")

    try:
        while True:
            is_battle = check.is_in_battle()

            print(f"{'='*40}")
            print(f"是否在战斗界面: {'是' if is_battle else '否'}")
            print(f"{'='*40}\n")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n测试结束")
    finally:
        ola.cleanup()


def test_battle_end_check():
    """战斗结束检测测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("战斗结束检测测试开始，每2秒检测一次，按 Ctrl+C 退出\n")

    try:
        while True:
            battle_ended = check.check_battle_end()

            print(f"{'='*40}")
            print(f"战斗是否结束: {'是' if battle_ended else '否'}")
            print(f"{'='*40}\n")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n测试结束")
    finally:
        ola.cleanup()


def test_battle():
    """战斗流程综合测试：找队伍 -> 进入战斗 -> 战斗中检测NPC -> 等待战斗结束 -> 返回主界面"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)
    detector = YOLODetector(config)
    gold_detector = GoldDetector(config, ola)
    merge_module = MergeModule(config, ola)
    summon_module = SummonModule(config, ola)
    enhance_module = EnhanceModule(config, ola)
    decision_module = DecisionModule(config, summon_module, enhance_module, merge_module)

    # 重置计数（新副本开始）
    summon_module.reset_count()
    enhance_module.reset_count()

    # 区域配置：右侧棋盘
    right_region = config.get_region("右侧棋盘区域")

    print("战斗流程综合测试开始\n")

    try:
        # 外层循环：整个战斗流程
        while True:
            # 1. 检查是否已经在战斗
            print("=" * 40)
            print("步骤1: 检查战斗状态")
            print("=" * 40)
            in_battle = check.is_in_battle()
            if in_battle:
                print("已在战斗中，跳过找队伍")
                break
            else:
                # 2. 找队伍
                print("\n" + "=" * 40)
                print("步骤2: 寻找队伍")
                print("=" * 40)
                team_result = check.find_team(max_attempts=10)
                if not team_result:
                    print("找队伍失败，测试终止")
                    return
                print(f"成功加入队伍: {team_result}")

                # 3. 等待进入战斗界面
                print("\n" + "=" * 40)
                print("步骤3: 等待进入战斗界面")
                print("=" * 40)
                max_wait = 20  # 最多等待60秒
                waited = 0
                prepare_clicked = False  # 是否已点击准备
                prepare_time = 0  # 点击准备的时间
                ready_to_restart = False  # 是否需要重新开始

                while waited < max_wait:
                    time.sleep(1)
                    waited += 1

                    # 检测是否在战斗界面
                    if check.is_in_battle():
                        in_battle = True
                        print(f"已进入战斗界面（等待 {waited} 秒）")
                        break

                    # 检测是否处于准备状态
                    if check.is_ready():
                        if not prepare_clicked:
                            # 点击战斗准备按钮
                            prepare_x, prepare_y = config.get_button("战斗准备")
                            if prepare_x != 0 or prepare_y != 0:
                                print(f"检测到准备状态，点击战斗准备按钮 ({prepare_x}, {prepare_y})")
                                ola.left_click(prepare_x, prepare_y)
                                time.sleep(0.5)  # 等待界面刷新

                                # 再次 OCR 确认是否点击成功（显示"取消准备"表示成功）
                                region = config.get_region("准备检测")
                                confirm_text = ola.ocr(region.x1, region.y1, region.x2, region.y2)
                                confirm_text = confirm_text.strip() if confirm_text else ""
                                if "取消准备" in confirm_text:
                                    print(f"点击成功，已进入准备状态（OCR: '{confirm_text}')")
                                    prepare_clicked = True
                                    prepare_time = waited
                                    continue
                                else:
                                    print(f"点击后 OCR 结果: '{confirm_text}'，未检测到'取消准备'")
                            continue
                        else:
                            # 已点击准备，检查是否超过20秒未进入战斗
                            if waited - prepare_time >= 20:
                                print(f"点击准备后超过20秒未进入战斗，返回主界面重新开始")
                                check.return_to_main(max_attempts=10)
                                ready_to_restart = True
                                break

                    print(f"等待进入战斗... ({waited}/{max_wait})")

                # 如果准备超时，重新开始整个流程
                if ready_to_restart:
                    print("准备超时，流程重新开始")
                    time.sleep(2)
                    continue

                if not in_battle:
                    print("超时未进入战斗界面，测试终止")
                    return

                break  # 成功进入战斗，跳出外层循环

        # 进入战斗后，关闭伤害数值显示（飘字开关）
        print("\n" + "=" * 40)
        print("步骤3.5: 关闭伤害数值显示")
        print("=" * 40)
        pop_x, pop_y = config.get_button("飘字开关")
        if pop_x != 0 or pop_y != 0:
            print(f"点击飘字开关 ({pop_x}, {pop_y}) 关闭伤害数值显示")
            ola.left_click(pop_x, pop_y)
            time.sleep(0.3)
        else:
            print("未配置飘字开关按钮坐标")

        # 定义检测函数（供步骤3.6和步骤4使用）
        def detect_all_npcs():
            """检测右侧棋盘的 NPC"""
            frame_right = ola.capture_to_numpy(
                right_region.x1, right_region.y1, right_region.x2, right_region.y2
            )
            if frame_right is not None:
                return detector.detect(frame_right, right_region)
            return []

        # 步骤3.6: 初始阶段连续召唤7次填满空位
        print("\n" + "=" * 40)
        print("步骤3.6: 初始阶段连续召唤7次填满空位")
        print("=" * 40)
        init_summon_count = 7
        for i in range(init_summon_count):
            print(f"初始召唤 #{i+1}/{init_summon_count}")
            # 检测当前空位
            current_npcs = detect_all_npcs()
            current_kongwei = sum(1 for n in current_npcs if n.name == "kongwei")
            print(f"  当前空位: {current_kongwei}")
            if current_kongwei <= 0:
                print("  空位已满，停止初始召唤")
                break
            # 执行召唤
            summon_module.execute_summon(current_npcs)
            time.sleep(0.8)  # 快速连续召唤，间隔短一些
        print("初始召唤完成")

        # 4. 战斗中检测 NPC
        print("\n" + "=" * 40)
        print("步骤4: 战斗中检测 NPC（每2秒检测一次）")
        print("=" * 40)
        battle_ended = False
        max_battle_wait = 1200  # 最多等待10分钟
        waited = 0
        npc_detect_count = 0

        while waited < max_battle_wait:
            # 检测战斗是否结束（check_battle_end 内部已包含双重校验：OCR检测 + is_in_battle）
            if check.check_battle_end():
                battle_ended = True
                print(f"\n战斗结束（战斗时长 {waited} 秒，共检测 {npc_detect_count} 次）")
                break

            # 每2秒检测一次 NPC
            npc_detect_count += 1
            print(f"\n{'='*50}")
            print(f"战斗检测 #{npc_detect_count} [{time.strftime('%H:%M:%S')}]")
            print(f"{'='*50}")

            # 1. 检测所有 NPC（包含 kongwei）
            npcs = detect_all_npcs()
            # 过滤掉空位 kongwei
            npcs_real = [n for n in npcs if n.name != "kongwei"]
            print(f"  NPC 总数: {len(npcs_real)}（空位: {len(npcs) - len(npcs_real)}）")
            for npc in npcs_real:
                print(f"    - {npc.name} {npc.star}星 置信度={npc.confidence:.2f}")

            # 2. 检测当前金币
            gold = gold_detector.detect()
            print(f"  持有金钱: {gold}")

            # 3. 使用决策模块决定下一步操作
            # 通过 NPC 星级计算召唤次数：1星=1次，2星=2次，3星=4次
            summon_count = summon_module.calc_summon_count(npcs)
            action, detail = decision_module.decide(
                gold=gold,
                summon_count=summon_count,
                npcs=npcs
            )

            # 4. 执行决策
            if action == "enhance":
                print(f"  >> 执行强化 (费用: {detail.get('cost')})")
                success = enhance_module.execute_enhance()
                if success:
                    print(f"  >> 强化成功")
                    time.sleep(1)
                    continue
                else:
                    print(f"  >> 强化失败")

            elif action == "summon":
                print(f"  >> 执行召唤 (费用: {detail.get('cost')})")
                summon_module.execute_summon(npcs)
                time.sleep(1)
                continue

            elif action == "merge":
                # 合成非保护腾空位后继续循环（让下一轮决策是否召唤）
                npc_info = detail.get("npc", {})
                print(f"  >> 合成非保护 {npc_info.get('name')} {npc_info.get('star')}星")
                merge_count = merge_module.merge_all(npcs_real, include_protected=False)
                if merge_count > 0:
                    time.sleep(1)
                    continue

            elif action == "merge_protected":
                # 合成保护腾空位后继续循环
                npc_info = detail.get("npc", {})
                print(f"  >> 合成保护 {npc_info.get('name')} {npc_info.get('star')}星")
                merge_count = merge_module.merge_all(npcs_real, include_protected=True, max_merge_star=1)
                if merge_count > 0:
                    time.sleep(1)
                    continue

            elif action == "wait":
                reason = detail.get("reason", "unknown")
                if reason == "save_for_enhance":
                    print(f"  >> 存钱等待强化 (需要: {detail.get('need')}, 当前: {detail.get('have')})")
                else:
                    print(f"  >> 等待 (无可用操作)")

            # 等待下次检测
            time.sleep(2)
            waited += 2

        if not battle_ended:
            print("超时战斗未结束，测试终止")
            return

        # 5. 返回主界面
        print("\n" + "=" * 40)
        print("步骤5: 返回主界面")
        print("=" * 40)
        time.sleep(2)  # 等待结算界面
        if check.return_to_main(max_attempts=10):
            print("成功返回主界面")
        else:
            print("返回主界面失败")

        print("\n" + "=" * 40)
        print("战斗流程测试完成")
        print("=" * 40)

    finally:
        ola.cleanup()


def main():
    print("请选择测试项目：")
    print("1. 主界面检测（循环）")
    print("2. 返回主界面")
    print("3. 自动找队伍")
    print("4. 战斗界面检测（循环）")
    print("5. 战斗结束检测（循环）")
    print("6. 战斗流程综合测试")
    print("7. 强化功能测试")
    print("8. 强化抽卡循环测试（强化按钮已点击）")
    print()

    choice = input("请输入选项 (1/2/3/4/5/6/7/8): ").strip()

    if choice == "1":
        test_main_screen()
    elif choice == "2":
        test_return_to_main()
    elif choice == "3":
        test_find_team()
    elif choice == "4":
        test_battle_check()
    elif choice == "5":
        test_battle_end_check()
    elif choice == "6":
        test_battle()
    elif choice == "7":
        test_enhance()
    elif choice == "8":
        test_enhance_loop()
    else:
        print("无效选项")


def test_main_screen():
    """主界面检测测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("主界面检测测试开始，每2秒检测一次，按 Ctrl+C 退出\n")

    try:
        while True:
            ocr_result = check.get_ocr_text()
            is_main = check.is_main_screen()

            print(f"{'='*40}")
            print(f"OCR 识别结果: {ocr_result}")
            print(f"角色名: {config.data.get('角色名', '')}")
            print(f"是否在主界面: {'是' if is_main else '否'}")
            print(f"{'='*40}\n")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n测试结束")
    finally:
        ola.cleanup()


def test_enhance():
    """强化功能测试"""
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)
    gold_detector = GoldDetector(config, ola)
    summon_module = SummonModule(config, ola)
    enhance_module = EnhanceModule(config, ola)

    # 重置计数
    summon_module.reset_count()
    enhance_module.reset_count()

    # 初始化检测器
    detector = YOLODetector(config)
    right_region = config.get_region("右侧棋盘区域")

    print("=" * 50)
    print("强化功能测试")
    print("=" * 50)
    print()

    try:
        # 检查是否在战斗界面
        if not check.is_in_battle():
            print("错误: 请在战斗界面进行强化测试")
            return

        # 1. 检测当前金币
        print("步骤1: 检测金币数量")
        print("-" * 30)
        gold = gold_detector.detect()
        print(f"当前金币: {gold}")
        print()

        # 2. 检测 NPC 以推断召唤次数
        print("步骤2: 检测 NPC 推断召唤次数")
        print("-" * 30)
        npcs = detector.detect_from_window(right_region)
        npc_count = summon_module.get_current_npc_count(npcs)
        # 召唤次数 = 1星=1次，2星=2次，3星=4次
        summon_count = summon_module.calc_summon_count(npcs)
        print(f"检测到 NPC 数量: {npc_count}")
        print(f"召唤次数（星级计算）: {summon_count}")
        print(f"强化解锁所需: {enhance_module.UNLOCK_SUMMON_COUNT}")
        print(f"强化已解锁: {'是' if enhance_module.is_unlocked(summon_count) else '否'}")
        print()

        # 3. 检测当前强化等级
        print("步骤3: 检测强化状态")
        print("-" * 30)
        print(f"当前强化等级: {enhance_module.enhance_count}")
        print(f"强化是否已达上限: {'是' if enhance_module.is_max_level() else '否'}")
        if not enhance_module.is_max_level():
            cost = enhance_module.get_cost()
            print(f"下一级强化费用: {cost}")
        print()

        # 4. 判断是否可以强化
        print("步骤4: 判断是否可以强化")
        print("-" * 30)
        can_enhance, reason = enhance_module.can_enhance(summon_count, gold)
        print(f"结果: {reason}")
        print()

        # 5. 如果可以强化，询问是否执行
        if can_enhance:
            print("=" * 50)
            user_input = input("是否执行强化？(y/n): ").strip().lower()
            print("=" * 50)

            if user_input == 'y' or user_input == 'yes' or user_input == '是':
                print("\n开始执行强化...")
                print()

                # 执行强化
                result = enhance_module.execute_enhance()

                if result:
                    print()
                    print("=" * 50)
                    print("强化成功！")
                    print(f"强化后等级: {enhance_module.enhance_count}")
                    print("=" * 50)
                else:
                    print()
                    print("=" * 50)
                    print("强化失败！")
                    print("=" * 50)
            else:
                print("用户取消强化")
        else:
            print("当前条件下无法强化，跳过执行")

    finally:
        ola.cleanup()


def test_enhance_loop():
    """强化抽卡循环测试（假设强化按钮已点击，每隔5秒执行一次抽卡）"""
    import logging
    from src.enhance import EnhanceModule

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )

    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    enhance_module = EnhanceModule(config, ola)
    enhance_module.reset_count()

    print("=" * 50)
    print("强化抽卡循环测试（强化按钮已点击）")
    print("每隔5秒执行一次抽卡，按 Ctrl+C 退出")
    print("=" * 50)
    print()

    try:
        enhance_count = 0
        while True:
            print(f"\n{'='*40}")
            print(f"第 {enhance_count + 1} 次抽卡")
            print(f"{'='*40}")

            # 等待5秒
            print("等待 5 秒...")
            time.sleep(5)

            # 检查是否在抽卡阶段（"请选择"）
            draw_region = config.get_region("开始抽卡识别")
            text = ola.ocr(draw_region.x1, draw_region.y1, draw_region.x2, draw_region.y2)
            text = text.strip() if text else ""
            print(f"OCR 检测结果: '{text}'")

            if "请选择" not in text:
                print("未检测到抽卡阶段，跳过本次")
                continue

            print("检测到抽卡阶段，开始选择卡牌...")

            # 选择卡牌
            success = enhance_module.select_card()
            if success:
                print("卡牌选择成功")
                enhance_count += 1
                enhance_module._enhance_count = enhance_count
                print(f"累计强化次数: {enhance_count}")
            else:
                print("卡牌选择失败")

            # 等待抽卡完成
            time.sleep(1)

            # 确认抽卡完成
            for _ in range(5):
                text = ola.ocr(draw_region.x1, draw_region.y1, draw_region.x2, draw_region.y2)
                text = text.strip() if text else ""
                if "请选择" not in text:
                    print("抽卡完成")
                    break
                time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n测试结束")
    finally:
        ola.cleanup()


if __name__ == "__main__":
    main()
