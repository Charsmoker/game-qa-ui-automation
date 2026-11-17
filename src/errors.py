#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :errors.py
# @Time      :2026/11/17 20:15:45
# @Author    :Lucas


class AutoTestError(Exception):
    """自动化测试相关的异常基类。

    有了基类，上层可以用一句 except AutoTestError 兜住所有自动化相关异常，
    而不会误抓 KeyError、NameError 这类真正的代码 bug。
    """
    pass


class EnvError(AutoTestError):
    """环境问题：窗口没开、设备掉线、配置缺失。
    
    特征：重跑一次可能就好了；该找的是环境或配置，不是开发。
    """
    pass


class FlowError(AutoTestError):
    """流程问题：流程设计不合理、流程步骤缺失，没走到。
    
    特征：重跑还是失败；说明被测功能或测试脚本本身有问题。
    """
    pass


class ElementNotFoundError(FlowError):
    """元素没找到：控件、按钮、文本、图片等。
    
    归在 FlowError 下，因为绝大多数情况是页面改版、模板过期，
    属于“测试资产要维护”，而不是“环境没准备好”。
    """
    pass