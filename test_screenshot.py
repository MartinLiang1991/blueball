"""单独测试 OLA 截图功能"""
import sys
sys.path.insert(0, 'src')

from ola import OLA
from config import Config

def main():
    config = Config()
    ola = OLA(config)

    # 绑定窗口
    if not ola.bind_window():
        print("绑定窗口失败")
        return

    # 测试区域：右侧棋盘
    x1, y1, x2, y2 = 349, 532, 488, 847
    print(f"测试区域: ({x1}, {y1}, {x2}, {y2})")

    # 测试 1: GetScreenData
    print("\n=== 测试 GetScreenData ===")
    try:
        data_ptr, data_len, stride, ret = ola.server.GetScreenData(x1, y1, x2, y2)
        print(f"返回值: ptr={data_ptr}, len={data_len}, stride={stride}, ret={ret}")
    except Exception as e:
        print(f"异常: {e}")

    # 测试 2: GetScreenDataBmp
    print("\n=== 测试 GetScreenDataBmp ===")
    try:
        data_ptr, data_len, ret = ola.server.GetScreenDataBmp(x1, y1, x2, y2)
        print(f"返回值: ptr={data_ptr}, len={data_len}, ret={ret}")
        if ret == 1 and data_ptr != 0:
            bmp_data = ola.server.GetImageBmpData(data_ptr)
            print(f"BMP 数据: {type(bmp_data)}, {len(bmp_data) if bmp_data else 0} bytes")
            ola.server.FreeImageData(data_ptr)
    except Exception as e:
        print(f"异常: {e}")

    # 测试 3: capture 方法（保存到文件）
    print("\n=== 测试 capture（保存文件）===")
    ret = ola.capture(x1, y1, x2, y2, "test_capture.png")
    print(f"返回值: {ret}")

    # 测试 4: capture_to_numpy
    print("\n=== 测试 capture_to_numpy ===")
    img = ola.capture_to_numpy(x1, y1, x2, y2)
    if img is not None:
        print(f"成功: shape={img.shape}")
    else:
        print("失败")

    ola.cleanup()

if __name__ == "__main__":
    main()
