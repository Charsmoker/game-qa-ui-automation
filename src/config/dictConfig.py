#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :dictConfig.py
# @Time      :2026/11/16 20:30:55
# @Author    :Lucas


import copy
import logging.config
from pathlib import Path

from src.config.settings import LoggingConfig
from src.paths import DEFAULT_LOG_DIR 

LOG_SETTING ={
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file_fmt": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
        },
        "console_fmt": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_fmt",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "file_fmt",
            "level": "DEBUG",
            "filename": str(DEFAULT_LOG_DIR  / "UIAutoMation.log"),   # 占位，实际由入参覆盖
            "when": "D",
            "interval": 1,
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "root": {
        "handlers": ["console", "file"], 
        "level": "DEBUG"
    },
}


def init_logger(log_file_path: str | Path, logging_cfg: LoggingConfig) -> None:
    """按配置初始化日志。

    :param log_file_path: 日志文件完整路径
    :param logging_cfg: 日志相关配置（级别、保留天数、编码）
    """
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    console_level = logging_cfg.console_level
    file_level = logging_cfg.file_level
    # root 必须取两者中更低的那一级，否则 DEBUG 记录在到达文件 handler 之前就被拦掉了
    root_level = min(getattr(logging, console_level), getattr(logging, file_level))

    cfg = copy.deepcopy(LOG_SETTING)
    cfg["handlers"]["console"]["level"] = console_level
    cfg["handlers"]["file"].update(
        {
            "filename": str(log_path),
            "level": file_level,
            "backupCount": logging_cfg.backup_days,
            "encoding": logging_cfg.encoding,
        }
    )
    cfg["root"]["level"] = logging.getLevelName(root_level)

    logging.config.dictConfig(cfg)