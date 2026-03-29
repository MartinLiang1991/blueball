"""YOLO NPC 检测 — 指定图片检测"""
import cv2
import time
from collections import Counter
import os
from ultralytics import YOLO

# === 配置 ===
model = YOLO("D:/weilanxingqiu2/best.pt")
CONF = 0.3

# 固定检测区域（相对于游戏窗口内部的坐标）
ROI_X1, ROI_Y1 = 349, 532   # 左上
ROI_X2, ROI_Y2 = 488, 847   # 右下

testfile = r"F:\projects\weilanOla\blueball\Screenshot\img\capture_1774747257241.png"


def get_class_statistics(results, model):
    """获取检测结果的统计信息"""
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return {}

    class_ids = boxes.cls.cpu().numpy().astype(int) if boxes.cls is not None else []
    class_counts = Counter(class_ids)

    stats = {}
    for class_id, count in class_counts.items():
        class_name = model.names[class_id] if class_id in model.names else f"未知类别{class_id}"
        stats[class_name] = count

    return stats


def print_statistics(stats):
    """打印统计信息"""
    print("\n" + "=" * 50)
    print(f"检测统计 ({time.strftime('%H:%M:%S')})")
    print("-" * 50)

    if not stats:
        print("未检测到任何物体")
    else:
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
        for class_name, count in sorted_stats:
            print(f"  {class_name}: {count}个")
        total = sum(stats.values())
        print(f"总计: {total}个物体")
    print("=" * 50)


def detect_test_file(test_file_path, use_roi=False):
    """
    检测指定的测试图片文件

    Args:
        test_file_path: 测试图片文件路径
        use_roi: 是否使用ROI区域进行检测
    """
    if not os.path.exists(test_file_path):
        print(f"错误: 测试文件不存在: {test_file_path}")
        return

    print(f"正在检测测试文件: {test_file_path}")
    print(f"使用ROI检测: {'是' if use_roi else '否'}")

    # 读取测试图片
    img = cv2.imread(test_file_path)
    if img is None:
        print(f"错误: 无法读取图片文件: {test_file_path}")
        return

    print(f"图片尺寸: {img.shape[1]}x{img.shape[0]} (宽x高)")

    # 准备要检测的区域
    if use_roi:
        height, width = img.shape[:2]
        if (ROI_X1 >= 0 and ROI_X2 <= width and ROI_Y1 >= 0 and ROI_Y2 <= height and
                ROI_X1 < ROI_X2 and ROI_Y1 < ROI_Y2):
            roi = img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]
            print(f"使用ROI区域: ({ROI_X1}, {ROI_Y1}) -> ({ROI_X2}, {ROI_Y2})")
            print(f"ROI尺寸: {roi.shape[1]}x{roi.shape[0]} (宽x高)")
        else:
            print("警告: ROI坐标超出图片范围，将检测整张图片")
            roi = img
    else:
        roi = img

    # 进行检测
    print("正在运行YOLO检测...")
    start_time = time.time()
    results = model(roi, verbose=False, conf=CONF)
    elapsed_time = time.time() - start_time

    # 获取统计信息
    stats = get_class_statistics(results, model)

    # 打印统计信息
    print(f"\n检测完成，耗时: {elapsed_time:.2f}秒")
    print_statistics(stats)

    # 显示结果
    annotated_img = results[0].plot()

    if use_roi:
        output_img = img.copy()
        output_img[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2] = annotated_img
    else:
        output_img = annotated_img

    # 保存结果图片
    save_path = f"detection_result_{os.path.basename(test_file_path)}"
    cv2.imwrite(save_path, output_img)
    print(f"结果已保存到: {save_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 命令行指定文件: python test_detect_game.py <图片路径>
        filepath = sys.argv[1]
        use_roi_input = input("是否使用ROI区域进行检测？(y/n): ").lower()
        use_roi = (use_roi_input == 'y')
    else:
        # 使用默认测试文件
        filepath = testfile
        use_roi = False

    detect_test_file(filepath, use_roi)
