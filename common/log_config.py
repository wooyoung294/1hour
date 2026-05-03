"""Loguru 설정 - pyproject.toml에서 로깅 설정을 읽어온다."""

import os
from pathlib import Path
import sys

from loguru import logger
import tomllib

_logger_initialized = False


def _find_pyproject() -> Path | None:
    cwd = Path.cwd()
    for p in [cwd, *cwd.parents]:
        candidate = p / 'pyproject.toml'
        if candidate.exists():
            return candidate
    return None


def get_log_config() -> dict:
    pyproject_path = _find_pyproject()
    if not pyproject_path:
        return {}
    with open(pyproject_path, 'rb') as f:
        config = tomllib.load(f)
    return config.get('tool', {}).get('logging', {})


def setup_logger():
    global _logger_initialized
    if _logger_initialized:
        return logger
    _logger_initialized = True

    logger.remove()
    config = get_log_config()
    log_level = config.get('debug_level') if os.getenv('DEBUG') else config.get('level', 'INFO')

    logger.add(
        sys.stderr,
        format=config.get('format', '{time:HH:mm:ss} | {level} | {message}'),
        level=log_level,
        colorize=True,
    )
    logger.add(
        config.get('file_path', 'logs/test.log'),
        format=config.get('file_format', '{time} | {level} | {message}'),
        rotation=config.get('rotation', '1 day'),
        retention=config.get('retention', '7 days'),
        level='DEBUG',
    )
    return logger
