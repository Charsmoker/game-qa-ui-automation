#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :run.py
# @Time      :2026/11/11 21:02:43
# @Author    :Lucas


import sys
from airtest.core.api import auto_setup
from device import connect_mini_program
from flow_mall import buy_in_mall
import logging,time

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(
        level=logging.INFO, 
        # format='%(asctime)s - %(levelname)s - %(message)s'
        format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s",
        )
    logger.info("开始执行商城购买冒烟。。。")
    start = time.time()

    auto_setup(__file__)
    try:
        connect_mini_program("军棋")
        buy_in_mall()
        logger.info(f"商城购买冒烟执行成功，耗时: {time.time()-start:.1f}秒")
        return 0
    except Exception:
        logger.exception(f"冒烟失败, 耗时: {time.time()-start:.1f}秒")
        return 1

if __name__ == "__main__":
    sys.exit(main())