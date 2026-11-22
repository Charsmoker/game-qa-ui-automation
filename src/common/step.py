#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :step.py
# @Time      :2026/11/22 15:43:54
# @Author    :Lucas

"""业务步骤的计时与日志。"""

import logging
import time
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def step(name: str):
    """包住一个业务步骤，记录开始、成功/失败、以及耗时。

    用法：
        with step("进入商城"):
            _tap("mall_icon")
            _check_exists("goods_card", "未进入商城：商品列表不存在")
    """
    start = time.perf_counter()
    logger.info("▶ %s", name)
    try:
        yield
    except Exception:
        logger.exception("❌ %s 失败: %2fs", name, time.perf_counter() - start)
        raise
    else:
        logger.info("✅ %s 成功 (耗时 %.2fs)", name, time.perf_counter() - start)