"""
Сохранение настроек пользователя в JSON-файл.
"""

import json
from pathlib import Path


SETTINGS_PATH = "user_settings.json"


def _read_settings() -> dict:
    """Читает настройки из файла. Если файла нет — возвращает пустой dict."""
    path = Path(SETTINGS_PATH)
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _write_settings(data: dict) -> None:
    """Записывает настройки в файл."""
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_setting(key: str, default=None):
    """Читает одну настройку по ключу."""
    data = _read_settings()
    return data.get(key, default)


def set_setting(key: str, value) -> None:
    """Записывает одну настройку."""
    data = _read_settings()
    data[key] = value
    _write_settings(data)


def remove_setting(key: str) -> None:
    """Удаляет одну настройку."""
    data = _read_settings()
    if key in data:
        del data[key]
        _write_settings(data)


def clear_all() -> None:
    """Удаляет все настройки."""
    _write_settings({})