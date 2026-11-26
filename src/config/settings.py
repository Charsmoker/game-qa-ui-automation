#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @FileName  :settings.py
# @Time      :2026/11/22 16:00:32
# @Author    :Lucas


"""应用配置：从 config.yaml 读取、校验、解析成绝对路径。"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from src.errors import ConfigError
from src.paths import ROOT, DEFAULT_OUT_DIR , DEFAULT_LOG_DIR 

CONFIG_FILE = ROOT / "config.yaml"

# 用 Literal 限定取值：写错级别会在加载时立刻报错，而不是运行到一半才发现
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class DeviceConfig(BaseModel):
    # extra="forbid"：配置文件里出现未知字段就报错，能抓住拼写错误
    model_config = ConfigDict(extra="forbid")

    keyword: str = Field(default="军棋", min_length=1, description="窗口标题包含的关键字")
    timeout: int = Field(default=30, ge=1, le=600, description="查找窗口的超时秒数")


class PathsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    output_dir: Path = Field(default=DEFAULT_OUT_DIR , description="截图输出目录")
    running_log_dir: Path = Field(default=DEFAULT_LOG_DIR , description="运行日志目录")

    @model_validator(mode="after")
    def _to_absolute(self) -> "PathsConfig":
        """相对路径统一按项目根解析，避免又变成"依赖当前工作目录"。"""
        if not self.output_dir.is_absolute():
            self.output_dir = (ROOT / self.output_dir).resolve()
        if not self.running_log_dir.is_absolute():
            self.running_log_dir = (ROOT / self.running_log_dir).resolve()
        return self


class LoggingConfig(BaseModel):
    # 日志设置
    model_config = ConfigDict(extra="forbid")

    console_level: LogLevel = "INFO"
    file_level: LogLevel = "DEBUG"
    backup_days: int = Field(default=7, ge=1, le=365)
    encoding: str = "utf-8"


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    device: DeviceConfig = Field(default_factory=DeviceConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_setting(path: Path | None = None) -> Settings:
    """加载并校验配置。

    :param path: 配置文件路径，默认项目根目录下的 config.yaml
    :raises ConfigError: 文件不存在、YAML 语法错误、字段校验失败
    """
    cfg_path = path or CONFIG_FILE

    # ① 文件不存在
    if not cfg_path.is_file():
        raise ConfigError(
            f"配置文件不存在：{cfg_path}\n"
            f"提示：在项目根目录执行 `Copy-Item config.example.yaml config.yaml`"
        )

    # ② 读不出来（权限、编码）
    try:
        text = cfg_path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConfigError(f"配置文件无法读取：{cfg_path}\n{e}") from e

    # ③ YAML 语法错误
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ConfigError(f"配置文件 YAML 语法错误：{cfg_path}\n{e}") from e

    # ④ 顶层结构不对
    if raw is None:            # 空文件 → 全部走默认值
        raw = {}
    if not isinstance(raw, dict):
        raise ConfigError(f"配置文件顶层必须是键值对：{cfg_path}")

    # ⑤ 字段校验
    try:
        return Settings(**raw)
    except ValidationError as e:
        detail = "\n".join(
            f"  - {' -> '.join(str(p) for p in err['loc']) or '(根)':<26}{err['msg']}"
            for err in e.errors()
        )
        raise ConfigError(f"配置校验失败：{cfg_path}\n{detail}") from e