# game-qa-ui-automation

微信小程序「军棋」商城购买的 UI 自动化冒烟。

## 环境
Python >= 3.11，Windows（依赖 pywinauto 找窗口）

```powershell
uv sync

## 运行
先打开小程序窗口，然后：
uv run run.py

退出码 0 = 通过，1 = 失败。截图输出在 ResultScreenshot/。

## 结构
- device.py   连接微信小程序窗口
- flow_mall.py 商城购买业务流程与检查点
- run.py      入口、日志、退出码