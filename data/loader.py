"""
Загрузка расписания из Excel.
"""

import pandas as pd
from pathlib import Path

# Путь к файлу расписания
SCHEDULE_PATH = "assets/schedule.xlsx"

# Кэш — чтобы не читать файл каждый раз
_schedule_cache = None


def load_schedule() -> pd.DataFrame:
    """
    Загружает расписание из Excel в DataFrame.
    При повторном вызове возвращает кэш.
    """
    global _schedule_cache

    if _schedule_cache is None:
        path = Path(SCHEDULE_PATH)
        if not path.exists():
            raise FileNotFoundError(f"Файл расписания не найден: {SCHEDULE_PATH}")

        df = pd.read_excel(SCHEDULE_PATH)

        # Заменяем все NaN на пустые строки
        df = df.fillna("")

        _schedule_cache = df
        print(f"Загружено {len(_schedule_cache)} записей из {SCHEDULE_PATH}")

    return _schedule_cache


def reload_schedule() -> pd.DataFrame:
    """Принудительно перечитывает файл (сброс кэша)."""
    global _schedule_cache
    _schedule_cache = None
    return load_schedule()