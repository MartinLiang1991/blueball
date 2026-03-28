---
name: implement-uicheck
overview: 创建 UI 校验模块 src/uicheck.py，OCR 识别"主界面校验"区域判断是否包含角色名，返回是否在主界面。
todos:
  - id: add-data-prop
    content: 在 config.py Config 类中添加 data property 暴露 _data 字典
    status: completed
  - id: create-uicheck
    content: 新建 src/uicheck.py，实现 UICheck.is_main_screen() 方法
    status: completed
    dependencies:
      - add-data-prop
  - id: update-init
    content: 更新 src/__init__.py 导出 UICheck
    status: completed
    dependencies:
      - create-uicheck
---

## 产品概述

实现一个 UI 状态校验方法，用于判断当前游戏界面是否处于主界面。

## 核心功能

- OCR 识别 config.json 中 `regions["主界面校验"]` 区域 (96,107 - 180,129) 的文字
- 判断识别结果是否包含 config.json 中顶层 `"角色名"` 的值（"車马炮"）
- 包含返回 True（在主界面），不包含返回 False（不在主界面）

## 实现方案

复用现有 `gold.py` 模块的构造模式（`__init__(config, ola)` + `ola.ocr()` + `config.get_region()`），新建 `uicheck.py` 模块。

### 修改范围

1. **`src/config.py`** — 添加 `data` property 暴露 `_data` 字典（已有 `summon.py` 第20行通过 `config.data` 访问，需补齐；同时可从中读取 `角色名`）
2. **`src/uicheck.py`** — 新建 UICheck 类，实现 `is_main_screen() -> bool`
3. **`src/__init__.py`** — 添加 UICheck 导出

### 关键实现细节

- `UICheck.__init__` 中缓存区域坐标和角色名：`config.get_region("主界面校验")` + `config.data.get("角色名", "")`
- `is_main_screen()` 调用 `self.ola.ocr(x1, y1, x2, y2)` 获取文字，用 `角色名 in text` 判断
- OCR 结果做 `strip()` 去除空白，空结果直接返回 False
- 参照 `gold.py` 的异常处理模式，OCR 失败时返回 False 并记录日志

### 目录结构

```
f:\projects\weilanOla\blueball\
├── src/
│   ├── config.py     # [MODIFY] 添加 data property
│   ├── uicheck.py    # [NEW] UI 校验模块
│   └── __init__.py   # [MODIFY] 导出 UICheck
```