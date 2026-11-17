#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :run.py
# @Time      :2026/11/11 21:02:43
# @Author    :Lucas


import sys
import logging
import time

from airtest.core.api import auto_setup

from src.flows import buy_in_mall
from src.device import connect_mini_program
from src.paths import OUT_DIR, RUNNING_LOG_DIR
from src.config.dictConfig import init_logger
from src.errors import EnvError, FlowError


init_logger(log_file_path=str(RUNNING_LOG_DIR / "UIAutoMation.log"))
logger = logging.getLogger(__name__)


def main():
    """商城购买冒烟入口。
    0: 成功
    1: 流程失败（元素没找到、断言失败）
    2: 环境未就绪（窗口没开、设备掉线）
    3: 未预期异常（框架 bug）
    """
    start = time.time()
    logger.info("开始执行商城购买冒烟。。。")
    code = 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    auto_setup(__file__)

    try:
        connect_mini_program(keyword="军棋", timeout=30)
        buy_in_mall()
    except EnvError as e:
        # 环境问题：不打堆栈，因为这是预期内的情况
        logger.error("环境异常，未就绪: %s", e)
        # 环境未就绪（窗口没开、设备掉线）
        code = 2
    except FlowError as e:
        # 业务流程失败：保留异常链，能看出是哪个元素、由什么引起
        logger.exception("流程异常、失败: %s", e)
        # 流程失败（元素没找到、断言失败）
        code = 1
    except Exception as e:
        # 兜底：脚本 bug 或没分类到的错误
        logger.exception("未知异常: %s", e)
        # 未预期异常（框架 bug）
        code = 3
    else:
        logger.info("商城购买冒烟执行成功！")
    finally:
        logger.info("商城购买冒烟执行结束，耗时 %.2fs", time.time() - start)

    return code


if __name__ == "__main__":
    sys.exit(main())