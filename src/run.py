#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :run.py
# @Time      :2026/11/11 21:02:43
# @Author    :Lucas


import logging
import sys
import time

from airtest.core.api import auto_setup

from src.config.dictConfig import init_logger
from src.config.settings import load_setting
from src.device import connect_mini_program
from src.errors import ConfigError, EnvError, FlowError, ScriptError
from src.flows import buy_in_mall


logger = logging.getLogger(__name__)
LOG_FILENAME = "UIAutoMation.log"


def main():
    """商城购买冒烟入口。
    0: 成功
    1: 流程失败（元素没找到、断言失败）
    2: 环境未就绪（窗口没开、设备掉线、配置缺失或非法）
    3: 脚本错误 / 未预期异常（框架 bug）
    """
    # 配置加载必须在日志初始化之前，所以这里只能用 stderr，用不了 logger
    try:
        settings = load_setting()
    except ConfigError as e:
        print(f"[配置错误] {e}", file=sys.stderr)
        return 2

    init_logger(settings.paths.running_log_dir / LOG_FILENAME, settings.logging)

    logger.info("开始执行商城购买冒烟。。。")
    logger.info(
        "生效配置: keyword=%s timeout=%s output=%s",
        settings.device.keyword,
        settings.device.timeout,
        settings.paths.output_dir,
    )

    start = time.time()
    code = 0

    auto_setup(__file__)
    try:
        connect_mini_program(settings.device.keyword, settings.device.timeout)
        buy_in_mall(settings.paths.output_dir)
    except EnvError as e:
        logger.error("环境异常，未就绪: %s", e)
        code = 2
    except FlowError as e:
        logger.exception("流程异常、失败: %s", e)
        code = 1
    except ScriptError as e:
        logger.error("脚本错误：%s", e)
        code = 3
    except Exception as e:
        logger.exception("未知异常: %s", e)
        code = 3
    else:
        logger.info("商城购买冒烟执行成功！")
    finally:
        logger.info("退出码: %d（0=通过 1=流程失败 2=环境 3=脚本错误）", code)
        logger.info("商城购买冒烟执行结束，耗时 %.2fs", time.time() - start)

    return code

if __name__ == "__main__":
    sys.exit(main())