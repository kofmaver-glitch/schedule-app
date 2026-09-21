"""
Сборка даты из числа + месяца + года.
Определение года по месяцу.
"""

from datetime import date
from parser.constants import MONTH_TO_YEAR, MONTH_TO_NUM


def build_date(day: int, month_name: str) -> date:
    """
    Собирает дату из числа и названия месяца.
    Год определяется автоматически (сентябрь-декабрь → 2026, 
    январь-август → 2027).
    """
    month_name = month_name.strip().lower()
    year = MONTH_TO_YEAR.get(month_name)
    month_num = MONTH_TO_NUM.get(month_name)
    
    if not year or not month_num:
        raise ValueError(f"Неизвестный месяц: {month_name}")
    
    return date(year, month_num, day)


def is_sunday(d: date) -> bool:
    """Проверяет, воскресенье ли это."""
    return d.weekday() == 6


def format_date(d: date) -> str:
    """Возвращает дату в формате YYYY-MM-DD."""
    return d.strftime("%Y-%m-%d")