"""스텝 컨텍스트 - 현재 실행 중인 BDD 스텝 추적."""

from pathlib import Path
import threading

_current_step = threading.local()


def set_current_step(step_name: str, step_func=None) -> None:
    _current_step.name = step_name
    if step_func:
        original_func = step_func
        while hasattr(original_func, '__wrapped__'):
            original_func = original_func.__wrapped__
        file_path = original_func.__code__.co_filename
        _current_step.module = Path(file_path).stem
    else:
        _current_step.module = None


def get_current_step() -> str | None:
    return getattr(_current_step, 'name', None)


def get_current_step_module() -> str | None:
    return getattr(_current_step, 'module', None)


def clear_current_step() -> None:
    _current_step.name = None
    _current_step.module = None
