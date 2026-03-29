"""YOLO NPC 检测单元测试"""
import os
import cv2
from src import Config, YOLODetector


def test_from_folder():
    """检测 Screenshot/img 目录下的图片"""
    config = Config()
    detector = YOLODetector(config)
    npc_region = config.get_region("右侧棋盘区域")

    # 图片目录
    img_dir = os.path.join(os.path.dirname(__file__), "Screenshot", "img")
    
    if not os.path.exists(img_dir):
        print(f"目录不存在: {img_dir}")
        return

    # 获取所有图片文件
    valid_ext = (".png", ".jpg", ".jpeg", ".bmp")
    files = [f for f in os.listdir(img_dir) if f.lower().endswith(valid_ext)]
    files.sort()
    
    if not files:
        print(f"目录中没有图片文件: {img_dir}")
        return

    print(f"=" * 60)
    print(f"检测目录: {img_dir}")
    print(f"共 {len(files)} 张图片")
    print(f"=" * 60)
    print()

    for i, filename in enumerate(files):
        filepath = os.path.join(img_dir, filename)
        print(f"[{i+1}/{len(files)}] {filename}")
        
        # 读取图片
        frame = cv2.imread(filepath)
        if frame is None:
            print(f"  图片加载失败")
            continue

        # 检测 NPC
        npcs = detector.detect(frame, npc_region)

        print(f"  检测到 {len(npcs)} 个 NPC:")
        for j, npc in enumerate(npcs):
            print(f"    [{j+1}] {npc.name} {npc.star}星 "
                  f"坐标=({npc.cx}, {npc.cy}) "
                  f"置信度={npc.confidence:.2f}")
        print()


def test_from_file(filepath: str):
    """检测指定图片文件"""
    config = Config()
    detector = YOLODetector(config)
    npc_region = config.get_region("右侧棋盘区域")

    if not os.path.exists(filepath):
        print(f"文件不存在: {filepath}")
        return

    print(f"=" * 60)
    print(f"检测文件: {filepath}")
    print(f"=" * 60)
    print()

    # 读取图片
    frame = cv2.imread(filepath)
    if frame is None:
        print(f"图片加载失败")
        return

    # 检测 NPC
    npcs = detector.detect(frame, npc_region)

    print(f"检测到 {len(npcs)} 个 NPC:")
    for i, npc in enumerate(npcs):
        print(f"  [{i+1}] {npc.name} {npc.star}星 "
              f"坐标=({npc.cx}, {npc.cy}) "
              f"置信度={npc.confidence:.2f}")
    print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 检测指定文件
        test_from_file(sys.argv[1])
    else:
        # 检测目录
        test_from_folder()
