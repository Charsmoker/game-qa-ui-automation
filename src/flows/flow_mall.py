#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :flow_mall.py
# @Time      :2026/11/11 21:05:50
# @Author    :Lucas

from pathlib import Path

from airtest.core.api import touch, Template, snapshot, assert_exists
from airtest.core.error import TargetNotFoundError

from src.paths import SHOT_DIR
from src.errors import ElementNotFoundError, ScriptError
from src.common.step import step


TPL = {
    "mall_icon":   Template(str(SHOT_DIR/"mall_icon.png"), record_pos=(0.335, 0.814),  resolution=(564, 1046)),
    "Switch_tabs":  Template(str(SHOT_DIR/"Switch_tabs.png"), record_pos=(-0.115, -0.491), resolution=(564, 1046)),
    "Buy_Button":  Template(str(SHOT_DIR/"Buy_Button.png"), record_pos=(-0.23, -0.083),  resolution=(564, 1046)),
    "buy_btn_true":     Template(str(SHOT_DIR/"buy_btn_true.png"), record_pos=(-0.002, 0.238),  resolution=(564, 1046)),
    "pay_confirm": Template(str(SHOT_DIR/"pay_confirm.png"), record_pos=(0.005, 0.619),   resolution=(564, 1046)),
    "myBag":      Template(str(SHOT_DIR/"myBag.png"), record_pos=(0.337, -0.486),  resolution=(564, 1046)),
    "back_home":   Template(str(SHOT_DIR/"back_home.png"), record_pos=(-0.417, -0.683), resolution=(564, 1046)),
    "exit_btn": Template(str(SHOT_DIR/"exit_btn.png"), record_pos=(-0.002, 0.238), resolution=(564, 1046)),
}

def _get(name: str) -> Template:
    """按名字取模板；名字不存在时给出可用列表，而不是裸 KeyError。"""
    try:
        return TPL[name]
    except KeyError:
        raise ScriptError(f"元素名未定义：{name}\n可用元素：{sorted(TPL)}") from None

def _tap(name: str) -> None:
    """点击指定的控件
    点击模板元素；找不到时转成 ElementNotFoundError，并带上元素名。
    """
    try:
        touch(_get(name))
    except TargetNotFoundError as e:
        raise ElementNotFoundError(f"未找到控件: {name}") from e

def _check_exists(name: str, msg: str) -> None:
    """
    检查指定的控件是否存在
    断言元素存在；失败时转成 ElementNotFoundError。
    """
    try:
        assert_exists(_get(name), msg)
    except (AssertionError, TargetNotFoundError) as e:
        raise ElementNotFoundError(f"{msg} （元素: {name}）") from e

def buy_in_mall(out_dir: Path) -> None:
    """执行商城购买流程。

    :param out_dir: 截图输出目录，由调用方传入（来自配置）
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    # ① 进入商城
    with step("进入商城"):
        _tap("mall_icon")
        _check_exists("Switch_tabs", "未进入商城：商品列表不存在")
        snapshot(str(out_dir/"01_Mall.png"))
    # ② 选商品进详情
    with step("选商品进详情"):
        _tap("Switch_tabs")
        _tap("Buy_Button")
        _check_exists("buy_btn_true", "未进入商品详情：购买按钮不存在")
        snapshot(str(out_dir/"02_Details.png"))

    # ③ 关闭商品详情，切换背包页签
    with step("关闭商品详情，切换背包页签"):
        # _tap("buy_btn_true")
        # _tap("pay_confirm")
        _tap("exit_btn")
        _tap("myBag")
        _check_exists("myBag", "切换失败，找不到背包页签")
        snapshot(str(out_dir/"03_Buy_Success.png"))
    # ④ 返回首页
    with step("返回首页"):
        _tap("back_home")
        snapshot(str(out_dir/"04_Back_Home_Success.png"))