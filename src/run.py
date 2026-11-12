#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# @FileName  :run.py
# @Time      :2026/11/11 21:02:43
# @Author    :Lucas


import sys
import logging
import time
from airtest.core.api import auto_setup
from src.flows import buy_in_mall
from src.device import connect_mini_program
from src.paths import OUT_DIR


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s",
        )
    logger.info("开始执行商城购买冒烟。。。")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    start = time.time()

    auto_setup(__file__)
    try:
        connect_mini_program("军棋")
        buy_in_mall()
        logger.info("冒烟通过，耗时 %.1fs", time.time() - start)
        return 0
    except Exception:
        logger.exception("冒烟失败, 耗时: %.1fs", time.time() - start)
        return 1

if __name__ == "__main__":
    sys.exit(main())