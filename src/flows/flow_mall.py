#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :flow_mall.py
# @Time      :2026/11/11 21:05:50
# @Author    :Lucas

from airtest.core.api import touch, Template, snapshot, assert_exists
from src.paths import SHOT_DIR, OUT_DIR


TPL = {
    "mall_icon":   Template(str(SHOT_DIR/"mall_icon.png"), record_pos=(0.335, 0.814),  resolution=(564, 1046)),
    "goods_card":  Template(str(SHOT_DIR/"goods_card.png"), record_pos=(-0.115, -0.491), resolution=(564, 1046)),
    "goods_open":  Template(str(SHOT_DIR/"goods_open.png"), record_pos=(-0.23, -0.083),  resolution=(564, 1046)),
    "buy_btn":     Template(str(SHOT_DIR/"buy_btn.png"), record_pos=(-0.002, 0.238),  resolution=(564, 1046)),
    "pay_confirm": Template(str(SHOT_DIR/"pay_confirm.png"), record_pos=(0.005, 0.619),   resolution=(564, 1046)),
    "pay_ok":      Template(str(SHOT_DIR/"pay_ok.png"), record_pos=(0.337, -0.486),  resolution=(564, 1046)),
    "back_home":   Template(str(SHOT_DIR/"back_home.png"), record_pos=(-0.417, -0.683), resolution=(564, 1046)),
}

def buy_in_mall():
    # ① 进入商城
    touch(TPL["mall_icon"])
    assert_exists(TPL["goods_card"], "未进入商城：商品列表不存在")
    snapshot(str(OUT_DIR/"01_Mall.png"))
    # ② 选商品进详情
    touch(TPL["goods_card"])
    touch(TPL["goods_open"])
    assert_exists(TPL["buy_btn"], "未进入商品详情：购买按钮不存在")
    snapshot(str(OUT_DIR/"02_Details.png"))

    # ③ 购买并确认
    touch(TPL["buy_btn"])
    touch(TPL["pay_confirm"])
    assert_exists(TPL["pay_ok"], "购买失败：未出现成功提示")
    snapshot(str(OUT_DIR/"03_Buy_Success.png"))

    touch(TPL["back_home"])