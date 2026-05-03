"""데코레이터 - 실패 시 상세 로깅."""

import functools
import inspect
import re

from loguru import logger
from playwright.sync_api import Locator

from common.step_context import get_current_step, get_current_step_module


def _unescape_unicode(text: str) -> str:
    def replace_unicode(match):
        return chr(int(match.group(1), 16))
    text = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, text)
    text = re.sub(r'\\([가-힣])', r'\1', text)
    return text


def _get_caller_method():
    for frame in inspect.stack():
        func_name = frame.function
        if func_name in ('wrapper', 'check'):
            continue
        if 'self' in frame.frame.f_locals:
            obj = frame.frame.f_locals['self']
            if hasattr(obj, 'page') and obj.__class__.__name__ != 'Base':
                return f'{obj.__class__.__name__}.{func_name}'
    return None


def _format_args(args, kwargs) -> str:
    parts = []
    for arg in args:
        if isinstance(arg, Locator):
            parts.append(_unescape_unicode(str(arg)))
        elif isinstance(arg, str):
            parts.append(f"'{arg}'")
        else:
            parts.append(str(arg))
    for k, v in kwargs.items():
        parts.append(f'{k}={v}')
    return ', '.join(parts)


def log_on_failure(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        caller = _get_caller_method()
        class_name = caller or self.__class__.__name__
        args_str = _format_args(args, kwargs)

        step_name = get_current_step()
        step_module = get_current_step_module()
        if step_name and step_module:
            logger.debug(f'[{step_module}] [{step_name}] {func.__name__}({args_str})')
        elif step_name:
            logger.debug(f'[{step_name}] {func.__name__}({args_str})')
        else:
            logger.debug(f'{class_name}.{func.__name__}({args_str})')

        try:
            return func(self, *args, **kwargs)
        except Exception:
            for frame in inspect.stack():
                if 'tenacity' in frame.filename:
                    raise

            logger.error('=' * 50)
            step_name = get_current_step()
            step_module = get_current_step_module()
            if step_name and step_module:
                logger.error(f'[{step_module}] {step_name}')
            elif step_name:
                logger.error(f'[Step] {step_name}')
            if caller:
                logger.error(f'{caller} -> {func.__name__} 실패')
            else:
                logger.error(f'{self.__class__.__name__}.{func.__name__} 실패')

            if hasattr(self, 'get_context_info'):
                logger.error(f'Context: {self.get_context_info()}')

            for i, arg in enumerate(args):
                if isinstance(arg, Locator):
                    locator_str = _unescape_unicode(str(arg))
                    logger.error(f'arg[{i}] (Locator): {locator_str}')
                    logger.error(f'  count: {arg.count()}')
                elif isinstance(arg, str):
                    logger.error(f"arg[{i}] (str): '{arg}'")
                else:
                    logger.error(f'arg[{i}]: {arg}')

            if kwargs:
                logger.error(f'kwargs: {kwargs}')
            logger.error('=' * 50)
            raise

    return wrapper
