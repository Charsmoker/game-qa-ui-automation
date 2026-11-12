#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :paths.py
# @Time      :2026/11/12 21:01:14
# @Author    :Lucas


"""集中管理项目路径。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # src -> 项目根
SHOT_DIR = ROOT / "Screenshot"
OUT_DIR = ROOT / "ResultScreenshot"
