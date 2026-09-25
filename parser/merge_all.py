"""
Объединяет расписания всех курсов в один Excel.
"""

import pandas as pd
from pathlib import Path


def merge_schedules():
    """Объединяет все .xlsx в единый assets/schedule.xlsx."""
    
    files = [
        "assets/schedule_3.xlsx",
        "assets/schedule_4.xlsx",
    ]
    
    dfs = []
    for f in files:
        path = Path(f)
        if path.exists():
            df = pd.read_excel(f)
            print(f"  Загружено {len(df)} записей из {f}")
            dfs.append(df)
        else:
            print(f"  ⚠️  Файл {f} не найден, пропускаем")
    
    if not dfs:
        print("  ❌ Нет данных для объединения")
        return
    
    merged = pd.concat(dfs, ignore_index=True)
    
    # Сортируем: сначала по курсу, потом по группе, потом по дате, потом по часам
    merged = merged.sort_values(
        ["Курс", "Группа", "Дата", "Часы"]
    ).reset_index(drop=True)
    
    # Сохраняем
    output = "assets/schedule.xlsx"
    merged.to_excel(output, index=False)
    
    print(f"\n  ✅ Объединено: {len(merged)} записей")
    print(f"  Сохранено: {output}")
    
    # Статистика
    print(f"\n  По курсам:")
    for course in sorted(merged["Курс"].unique()):
        count = len(merged[merged["Курс"] == course])
        groups = sorted(merged[merged["Курс"] == course]["Группа"].unique())
        print(f"    Курс {course}: {count} записей, {len(groups)} групп")
    
    return merged


if __name__ == "__main__":
    print("Объединение расписаний:")
    merge_schedules()