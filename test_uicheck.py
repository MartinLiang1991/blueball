"""主界面检测单元测试"""
import time
from src import Config, OLA, UICheck


def main():
    config = Config()
    ola = OLA(config)

    # 绑定游戏窗口
    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    check = UICheck(config, ola)

    print("主界面检测测试开始，每2秒检测一次，按 Ctrl+C 退出\n")

    try:
        while True:
            # 获取 OCR 结果
            ocr_result = check.get_ocr_text()
            # 检测是否在主界面
            is_main = check.is_main_screen()

            # 输出结果
            print(f"{'='*40}")
            print(f"OCR 识别结果: {ocr_result}")
            print(f"角色名: {config.data.get('角色名', '')}")
            print(f"是否在主界面: {'是' if is_main else '否'}")
            print(f"{'='*40}\n")

            # 等待2秒
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n测试结束")
    finally:
        ola.cleanup()


if __name__ == "__main__":
    main()
