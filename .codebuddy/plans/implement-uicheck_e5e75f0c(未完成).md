---
name: implement-uicheck
overview: 创建 UI 校验模块 src/uicheck.py，通过 OCR 识别"主角面校验"区域是否包含角色名来判断是否处于主界面。同时更新 config.py 添加角色名访问属性。
todos:
  - id: add-role-name-prop
    content: 在 config.py Config 类中添加 角色名 property
    status: pending
  - id: create-uicheck
    content: 新建 src/uicheck.py，实现 UICheck.is_main_screen() 方法
    status: pending
  - id: update-init
    content: 更新 src/__init__.py 导出 UICheck
    status: pending
    dependencies:
      - create-uicheck
---

## 用户需求

创建一个 UI 校验方法，通过 OLA OCR 识别主界面校验区域是否包含角色名，从而判断当前 UI 是否处于主界面。

## 核心功能

- 读取 config.json 中 `主角面校验` 区域坐标 (96,107 - 180,129)
- 调用 OLA OCR 识别该区域文字
- 判断识别结果是否包含角色名 `車马炮`
- 包含返回 True（在主界面），不包含返回 False（不在主界面）

## 技术方案

### 实现方式

复用现有 `ola.py` 的 `OCR` 方法和 `config.py` 的 `get_region()` 模式，新建 `UICheck` 模块。

### 修改范围

1. **`src/config.py`** — Config 类添加 `角色名` property，从 `self._data.get("角色名", "")` 读取
2. **`src/uicheck.py`** — 新建 UICheck 类，实现 `is_main_screen() -> bool`
3. **`src/__init__.py`** — 添加 `from .uicheck import UICheck` 导出

### 关键实现细节

- `is_main_screen()` 使用 `config.get_region("主角面校验")` 获取区域坐标
- 调用 `ola.ocr(x1, y1, x2, y2)` 识别文字
- 用 `角色名 in ocr_text` 判断（OCR 可能存在少量识别误差，后续可加模糊匹配）
- OCR 结果做 `strip()` 去除空白，记录日志方便调试