# -*- encoding=utf8 -*-
__author__ = "pc"

from airtest.core.api import *
from pywinauto import findwindows
import win32gui

def connect_wechat_mini_program(keyword="军棋"):
    handles = findwindows.find_windows(title_re=f".*{keyword}.*")
    
    for hwnd in handles:
        title = win32gui.GetWindowText(hwnd)
        # 微信小程序窗口标题通常是 "微信" 或者小程序的名称
        # 你可以在这里打印出来看看，确认哪个是小程序窗口
        print(f"发现窗口: {title}, 句柄: {hwnd}")
        
        if keyword in title: 
            # 一旦找到，直接连接并退出函数
            print(f"成功连接窗口: {title}")
            connect_device(f"Windows:///{hwnd}")
            return True
            
    print("未能找到符合条件的窗口")
    return False




if connect_wechat_mini_program():
    auto_setup(__file__)
    touch(Template(r"tpl1794314774787.png", record_pos=(0.335, 0.814), resolution=(564, 1046)))
    touch(Template(r"tpl1794314850626.png", record_pos=(-0.115, -0.491), resolution=(564, 1046)))
    touch(Template(r"tpl1794314857616.png", record_pos=(-0.23, -0.083), resolution=(564, 1046)))
    touch(Template(r"tpl1794314933796.png", record_pos=(-0.002, 0.238), resolution=(564, 1046)))

    touch(Template(r"tpl1794314882511.png", record_pos=(0.005, 0.619), resolution=(564, 1046)))
    touch(Template(r"tpl1794314888551.png", record_pos=(0.337, -0.486), resolution=(564, 1046)))
    touch(Template(r"tpl1794314896096.png", record_pos=(-0.417, -0.683), resolution=(564, 1046)))

