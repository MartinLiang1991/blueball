"""YOLO NPC 实时监视测试脚本"""
import time
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from ola import OLA
from detector import YOLODetector


def main():
    config = Config()
    ola = OLA(config)

    if not ola.bind_window():
        print("窗口绑定失败，请确认游戏已启动")
        return

    detector = YOLODetector(config)
    # 使用右侧棋盘区域
    region = config.get_region("右侧棋盘区域")

    print("=" * 60)
    print("YOLO NPC 实时监视")
    print(f"检测区域: 右侧棋盘 ({region.x1}, {region.y1}, {region.x2}, {region.y2})")
    print("每 2 秒检测一次，按 Ctrl+C 退出")
    print("=" * 60)
    print()

    detect_count = 0
    total_npcs = 0
    start_time = time.time()

    try:
        while True:
            detect_count += 1
            timestamp = time.strftime("%H:%M:%S")
            elapsed = int(time.time() - start_time)

            # 截图
            frame = ola.capture_to_numpy(
                region.x1, region.y1, region.x2, region.y2, temp=False  # 保存到 img 目录
            )

            if frame is None:
                print(f"[{timestamp}] 截图失败")
                time.sleep(2)
                continue

            # 检测 NPC
            npcs = detector.detect(frame, region)
            total_npcs += len(npcs)

            # 输出结果
            print(f"\n{'='*60}")
            print(f"检测 #{detect_count} | 时间: {timestamp} | 运行时长: {elapsed}s")
            print(f"{'='*60}")
            print(f"检测到 {len(npcs)} 个 NPC (累计: {total_npcs})")

            if npcs:
                for i, npc in enumerate(npcs):
                    print(f"  [{i+1}] {npc.name} | {npc.star}星 | "
                          f"坐标=({npc.cx}, {npc.cy}) | 置信度={npc.confidence:.2f}")
            else:
                print("  (无)")

            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print("监视结束")
        print(f"总检测次数: {detect_count}")
        print(f"总检测到 NPC 数: {total_npcs}")
        print(f"运行时长: {int(time.time() - start_time)} 秒")
        print(f"{'='*60}")
    finally:
        ola.cleanup()


if __name__ == "__main__":
    main()
