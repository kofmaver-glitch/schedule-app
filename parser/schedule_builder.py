"""
Главный парсер: собирает всё расписание из Word в Excel.
Работает для любого курса — принимает параметры.
"""

from docx import Document
import pandas as pd
from pathlib import Path

from parser.cell_parser import parse_cell
from parser.date_builder import build_date, format_date
from parser.constants import get_time, SUBJECTS


# Индексы столбцов в исходной таблице
COL_GROUP = 0
COL_HOURS = 1
COL_DAY_START = 2  # дальше идут дни месяца


def build_schedule(
    docx_path: str,
    output_path: str,
    course: int,
    specialty: str = "ЛД",
) -> pd.DataFrame:
    """
    Главная функция: читает docx, возвращает DataFrame.
    
    docx_path — путь к .docx файлу
    output_path — путь для сохранения .xlsx
    course — номер курса (3, 4, ...)
    specialty — специальность (ЛД, Ст, ...)
    """
    
    doc = Document(docx_path)
    
    # Основное расписание — таблицы 0-8 (для 3 курса)
    # Для 4 курса структура похожа — берём первые 9 таблиц
    main_tables = doc.tables[0:9]
    
    rows = []
    
    for table_idx, table in enumerate(main_tables):
        print(f"  Обрабатываю таблицу №{table_idx}...")
        table_rows = _parse_table(table, course, specialty)
        rows.extend(table_rows)
    
    df = pd.DataFrame(rows)
    
    # Заменяем NaN на пустые строки
    df = df.fillna("")
    
    # Сохраняем в Excel
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"  ✅ Сохранено: {output_path}")
    print(f"  Всего записей: {len(df)}")
    
    return df


def _parse_table(table, course: int, specialty: str) -> list:
    """
    Обрабатывает одну таблицу.
    Возвращает список словарей (по одному на каждую пару).
    """
    result = []
    
    # Определяем, какие месяцы в каких столбцах
    month_by_col = _map_months_to_columns(table)
    
    # Строка 1 содержит числа месяца
    days_row = table.rows[1]
    
    # Текущая группа (объединённая ячейка)
    current_group = None
    
    # Проходим по всем строкам с данными (начиная с 2-й)
    for row_idx in range(2, len(table.rows)):
        row = table.rows[row_idx]
        
        # Обновляем группу, если она указана в этой строке
        group_cell = row.cells[COL_GROUP].text.strip()
        if group_cell:
            current_group = group_cell
        
        if not current_group:
            continue
        
        # Часы занятий (1-2, 3-4 и т.д.)
        hours = row.cells[COL_HOURS].text.strip()
        if not hours:
            continue
        
        # Проходим по всем дням месяца (столбцы с 2-го и далее)
        for col_idx in range(COL_DAY_START, len(row.cells)):
            # Число месяца
            day_text = days_row.cells[col_idx].text.strip()
            if not day_text or not day_text.isdigit():
                continue
            day = int(day_text)
            
            # Месяц для этого столбца
            month_name = month_by_col.get(col_idx)
            if not month_name:
                continue
            
            # Собираем дату
            try:
                date_obj = build_date(day, month_name)
            except ValueError:
                continue
            
            # Содержимое ячейки
            cell_text = row.cells[col_idx].text.strip()
            if not cell_text or cell_text == "\xa0":
                continue
            
            # Разбираем ячейку
            parsed = parse_cell(cell_text)
            if not parsed:
                continue
            
            # Название предмета из расшифровки
            subject_name = SUBJECTS.get(parsed["код"], parsed["код"])
            
            # Время пары — в зависимости от курса
            time_str = get_time(course, hours)
            
            result.append({
                "Курс": course,
                "Специальность": specialty,
                "Группа": current_group,
                "Дата": format_date(date_obj),
                "День_недели": _weekday_ru(date_obj),
                "Часы": hours,
                "Время": time_str,
                "Тип": parsed["тип"],
                "Код": parsed["код"],
                "Предмет": subject_name,
                "Аудитория": parsed["аудитория"],
                "Дистант": parsed["дистант"],
            })
    
    return result


def _map_months_to_columns(table) -> dict:
    """
    Определяет, к какому столбцу какой месяц относится.
    Возвращает {индекс столбца: название месяца}.
    """
    result = {}
    header_row = table.rows[0]
    
    # Идём по столбцам, начиная с 2-го
    last_month = None
    for col_idx in range(COL_DAY_START, len(header_row.cells)):
        cell_text = header_row.cells[col_idx].text.strip().lower()
        if cell_text in ("сентябрь", "октябрь", "ноябрь", "декабрь",
                         "январь", "февраль", "март", "апрель"):
            last_month = cell_text
        result[col_idx] = last_month
    
    return result


def _weekday_ru(d) -> str:
    """Возвращает день недели по-русски."""
    days = ["Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"]
    return days[d.weekday()]


if __name__ == "__main__":
    # Тестовый запуск — 3 курс
    print("Парсинг 3 курса:")
    df3 = build_schedule(
        docx_path="schedule.docx",
        output_path="assets/schedule_3.xlsx",
        course=3,
        specialty="ЛД",
    )
    
    print("\nПервые 10 строк:")
    print(df3.head(10).to_string())