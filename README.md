# game-qa-ui-automation

微信小程序「军棋」商城购买的 UI 自动化冒烟。

## 环境

Python >= 3.11，Windows（依赖 pywinauto 找窗口）

```powershell
uv sync
```

## 配置

首次运行前复制配置模板：

```powershell
Copy-Item config.example.yaml config.yaml
```

## 运行

先打开小程序窗口，然后：

```powershell
uv run python -m src.run
```
注意：命令需在项目根目录执行。
> CI 环境建议设置 `PYTHONUTF8=1`，否则中文日志在控制台可能乱码。

## 退出码

- 0 = 通过
- 1 = 流程失败
- 2 = 环境未就绪（窗口没开、设备掉线、配置缺失或非法）
- 3 = 脚本错误 / 未预期异常（框架 bug）



## 结构

- `src/run.py`：入口、日志、退出码
- `src/device/window.py`：连接微信小程序窗口
- `src/flows/flow_mall.py`：商城购买业务流程与检查点
- `src/paths.py`：集中管理项目路径
- `src/errors.py`：错误类型
- `ResultScreenshot`：截图输出