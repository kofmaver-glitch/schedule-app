"""
Фильтрация расписания: по группе, по дате, по диапазону.
"""

from datetime import date, datetime
import pandas as pd

from data.loader import load_schedule


def get_courses() -> list:
    """Возвращает список всех курсов."""
    df = load_schedule()
    return sorted(df["Курс"].unique().tolist())


def get_groups(course=None) -> list:
    """
    Возвращает список групп.
    Если указан course — только группы этого курса.
    """
    df = load_schedule()
    if course is not None:
        df = df[df["Курс"] == course]
    return sorted(df["Группа"].unique().tolist())


def get_schedule_for_date(group: str, target_date: date) -> pd.DataFrame:
    """
    Возвращает все пары для группы на конкретную дату.
    Отсортировано по времени.
    """
    df = load_schedule()
    date_str = target_date.strftime("%Y-%m-%d")
    result = df[(df["Группа"] == group) & (df["Дата"] == date_str)]
    return result.sort_values("Часы").reset_index(drop=True)


def get_schedule_for_week(group: str, start_date: date) -> pd.DataFrame:
    """
    Возвращает расписание на неделю (7 дней от start_date).
    """
    df = load_schedule()
    end_date = start_date + pd.Timedelta(days=6)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    result = df[
        (df["Группа"] == group)
        & (df["Дата"] >= start_str)
        & (df["Дата"] <= end_str)
    ]
    return result.sort_values(["Дата", "Часы"]).reset_index(drop=True)


def get_all_dates(group: str) -> list:
    """Возвращает список всех дат, в которые у группы есть пары."""
    df = load_schedule()
    group_df = df[df["Группа"] == group]
    return sorted(group_df["Дата"].unique().tolist())


def get_current_pair(group: str, now=None):
    """
    Возвращает текущую пару (если сейчас идёт занятие).
    Или None, если сейчас нет пары.
    """
    if now is None:
        now = datetime.now()

    today = now.date()
    df = get_schedule_for_date(group, today)

    if df.empty:
        return None

    current_time = now.strftime("%H:%M")

    for _, row in df.iterrows():
        time_range = row["Время"].replace(" ", "")
        if "–" in time_range:
            start, end = time_range.split("–")
        elif "-" in time_range:
            start, end = time_range.split("-")
        else:
            continue

        if start <= current_time <= end:
            return row.to_dict()

    return None