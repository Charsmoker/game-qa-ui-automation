#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :dictConfig.py
# @Time      :2026/11/16 20:30:55
# @Author    :Lucas


import logging.config
import os
import copy
from datetime import datetime
from src.paths import RUNNING_LOG_DIR


LOG_SETTING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "file_fmt": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
            },
            "console_fmt": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console_fmt",
                "level": "INFO",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "file_fmt",
                "level": "DEBUG",
                "filename": RUNNING_LOG_DIR,
                "when": "D",
                "interval": 1,
                "backupCount": 7,
                "encoding": "utf-8"
            }
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        }
    }


def init_logger(log_file_path: str | None = None):
    """
    :param log_file_path: 日志文件完整路径；不传默认在启动目录下 RunningLog/UIAutoMation.log
    """
    if log_file_path is None:
        log_file_path = str(RUNNING_LOG_DIR / "UIAutoMation.log")

    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    cfg = copy.deepcopy(LOG_SETTING)
    cfg["handlers"]["file"]["filename"] = log_file_path
    # 然后再应用日志配置
    logging.config.dictConfig(cfg)
