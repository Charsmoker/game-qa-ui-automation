#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :device.py
# @Time      :2026/11/11 21:00:34
# @Author    :Lucas

import time,logging

logger = logging.getLogger(__name__)

class WindowNotFoundError(Exception):
    """Raised when a window is not found."""
    pass

def connect_mini_program(keyword="军棋", timeout=30):
    ## 函数内导入，避免非 Windows 环境导入失败
    from pywinauto import findwindows
    import win32gui
    from airtest.core.api import connect_device

    deadline = time.time() + timeout
    while time.time() < deadline:
        for hwnd in findwindows.find_windows(title_re=f".*{keyword}.*"):
            title = win32gui.GetWindowText(hwnd)
            
            if keyword in title: 
                logger.info("连接窗口: %s (hwnd=%s)", title, hwnd)
                connect_device(f"Windows:///{hwnd}")
                return True

        time.sleep(1)  # 等待一秒后重试
    raise WindowNotFoundError(f"未能找到符合条件的窗口: {keyword}, 请确保小程序已打开并且标题包含关键词。")
