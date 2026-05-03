"""환경 변수 파서 - YAML에서 dot notation으로 값을 가져온다."""

import os
from pathlib import Path

import yaml

_ENV_VARS: dict = {}


def _find_configs_dir() -> Path:
    cwd = Path.cwd()
    for p in [cwd, *cwd.parents]:
        cand = p / 'configs'
        if cand.is_dir():
            return cand
    return cwd


def load_env_vars(env: str | None = None) -> dict:
    """환경 변수를 로드한다. pytest_configure에서 호출."""
    global _ENV_VARS
    env = env or os.getenv('ENV', 'qa')
    cfg_dir = _find_configs_dir()
    yml = cfg_dir / f'vars.{env}.yaml'
    if yml.exists():
        with yml.open(encoding='utf-8') as f:
            _ENV_VARS = yaml.safe_load(f) or {}
    return _ENV_VARS


def envstr(token: str) -> str:
    """dot notation으로 YAML 값을 가져온다.

    예: envstr('store.option') → vars.qa.yaml의 store.option 값
    """
    if not _ENV_VARS:
        load_env_vars()
    cur = _ENV_VARS
    for part in token.split('.'):
        cur = cur[part]
    return str(cur)


def get_i18n_text(namespace: str, key: str, lang: str = 'KO') -> str:
    """다국어 텍스트를 가져온다.

    KO → store.key
    EN → store.key_en
    ZH → store.key_zh
    JA → store.key_ja
    """
    suffix = '' if lang == 'KO' else f'_{lang.lower()}'
    localized_key = f'{namespace}.{key}{suffix}'
    try:
        return envstr(localized_key)
    except KeyError as e:
        raise KeyError(f'i18n key not found: {localized_key} (key:{key} lang:{lang})') from e
