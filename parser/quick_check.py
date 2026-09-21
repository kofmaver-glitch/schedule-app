"""
Быстрая проверка: смотрим статистику по расписанию.
"""

import pandas as pd

df = pd.read_excel("assets/schedule.xlsx")

print(f"Всего записей: {len(df)}")
print(f"Колонки: {list(df.columns)}")
print()

print("=" * 60)
print("Первые 15 строк:")
print("=" * 60)
print(df.head(15).to_string())

print()
print("=" * 60)
print("Уникальные группы:")
print("=" * 60)
print(sorted(df["Группа"].unique()))

print()
print("=" * 60)
print("Даты:")
print("=" * 60)
dates = sorted(df["Дата"].unique())
print(f"Всего дат: {len(dates)}")
print(f"Первая: {dates[0]}")
print(f"Последняя: {dates[-1]}")

print()
print("=" * 60)
print("Проверка: воскресенья (должно быть 0):")
print("=" * 60)
sundays = df[df["День_недели"] == "Воскресенье"]
print(f"Записей на воскресеньях: {len(sundays)}")

print()
print("=" * 60)
print("Проверка: 4 ноября 2026 (праздник, должно быть 0):")
print("=" * 60)
holiday = df[df["Дата"] == "2026-11-04"]
print(f"Записей: {len(holiday)}")

print()
print("=" * 60)
print("Типы занятий:")
print("=" * 60)
print(df["Тип"].value_counts())

print()
print("=" * 60)
print("Часы занятий:")
print("=" * 60)
print(df["Часы"].value_counts().sort_index())