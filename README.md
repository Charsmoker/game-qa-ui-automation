# game-qa-ui-automation

微信小程序「军棋」商城购买的 UI 自动化冒烟。

## 环境

Python >= 3.11，Windows（依赖 pywinauto 找窗口）

```powershell
uv sync
```

## 运行

先打开小程序窗口，然后：

```powershell
uv run python -m src.run
```
注意：命令需在项目根目录执行。

退出码 0 = 通过，1 = 失败。截图输出在 `ResultScreenshot/`。

> CI 环境建议设置 `PYTHONUTF8=1`，否则中文日志在控制台可能乱码。

## 结构

- `src/run.py`：入口、日志、退出码
- `src/device/window.py`：连接微信小程序窗口
- `src/flows/flow_mall.py`：商城购买业务流程与检查点
- `src/paths.py`：集中管理项目路径

