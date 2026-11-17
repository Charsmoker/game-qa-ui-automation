#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :flow_mall.py
# @Time      :2026/11/11 21:05:50
# @Author    :Lucas

import logging

from airtest.core.api import touch, Template, snapshot, assert_exists
from airtest.core.error import TargetNotFoundError
from src.paths import SHOT_DIR, OUT_DIR
from src.errors import ElementNotFoundError

logger = logging.getLogger(__name__)

TPL = {
    "mall_icon":   Template(str(SHOT_DIR/"mall_icon.png"), record_pos=(0.335, 0.814),  resolution=(564, 1046)),
    "goods_card":  Template(str(SHOT_DIR/"goods_card.png"), record_pos=(-0.115, -0.491), resolution=(564, 1046)),
    "goods_open":  Template(str(SHOT_DIR/"goods_open.png"), record_pos=(-0.23, -0.083),  resolution=(564, 1046)),
    "buy_btn":     Template(str(SHOT_DIR/"buy_btn.png"), record_pos=(-0.002, 0.238),  resolution=(564, 1046)),
    "pay_confirm": Template(str(SHOT_DIR/"pay_confirm.png"), record_pos=(0.005, 0.619),   resolution=(564, 1046)),
    "pay_ok":      Template(str(SHOT_DIR/"pay_ok.png"), record_pos=(0.337, -0.486),  resolution=(564, 1046)),
    "back_home":   Template(str(SHOT_DIR/"back_home.png"), record_pos=(-0.417, -0.683), resolution=(564, 1046)),
}

def _tap(name: str) -> None:
    """点击指定的控件
    点击模板元素；找不到时转成 ElementNotFoundError，并带上元素名。
    """
    try:
        touch(TPL[name])
    except TargetNotFoundError as e:
        raise ElementNotFoundError(f"未找到控件: {name}") from e

def _check_exists(name: str, msg: str) -> None:
    """
    检查指定的控件是否存在
    断言元素存在；失败时转成 ElementNotFoundError。
    """
    try:
        assert_exists(TPL[name], msg)
    except (AssertionError, TargetNotFoundError) as e:
        raise ElementNotFoundError(f"{msg} （元素: {name}）") from e

def buy_in_mall():
    # ① 进入商城
    _tap("mall_icon")
    _check_exists("goods_card", "未进入商城：商品列表不存在")
    snapshot(str(OUT_DIR/"01_Mall.png"))
    # ② 选商品进详情
    _tap("goods_card")
    _tap("goods_open")
    _check_exists("buy_btn", "未进入商品详情：购买按钮不存在")
    snapshot(str(OUT_DIR/"02_Details.png"))

    # ③ 购买并确认
    _tap("buy_btn")
    _tap("pay_confirm")
    _check_exists("pay_ok", "购买失败：未出现成功提示")
    snapshot(str(OUT_DIR/"03_Buy_Success.png"))

    _tap("back_home")