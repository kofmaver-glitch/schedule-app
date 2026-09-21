"""
Главный парсер: собирает всё расписание из Word в Excel.
"""

from docx import Document
import pandas as pd
from pathlib import Path

from parser.cell_parser import parse_cell
from parser.date_builder import build_date, format_date
from parser.constants import TIME_SLOTS, SUBJECTS


# Индексы столбцов в исходной таблице
COL_GROUP = 0
COL_HOURS = 1
COL_DAY_START = 2  # дальше идут дни месяца


def build_schedule(docx_path: str = "schedule.docx", 
                   output_path: str = "assets/schedule.xlsx") -> pd.DataFrame:
    """Главная функция: читает docx, возвращает DataFrame."""
    
    doc = Document(docx_path)
    
    # Обрабатываем только таблицы основного расписания (№0-№8)
    # №9 — зачёты/экзамены, №10 — расшифровка. Пока пропускаем.
    main_tables = doc.tables[0:9]
    
    rows = []
    
    for table_idx, table in enumerate(main_tables):
        print(f"Обрабатываю таблицу №{table_idx}...")
        table_rows = _parse_table(table)
        rows.extend(table_rows)
    
    df = pd.DataFrame(rows)
    
    # Заменяем NaN на пустые строки (для чистого Excel)
    df = df.fillna("")
    
    # Сохраняем в Excel
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"\n✅ Сохранено: {output_path}")
    print(f"Всего записей: {len(df)}")
    
    return df


def _parse_table(table) -> list:
    """
    Обрабатывает одну таблицу.
    Возвращает список словарей (по одному на каждую пару).
    """
    result = []
    
    # Строка 0 — шапка с месяцами
    # Строка 1 — числа месяца
    # Строки 2+ — данные
    
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
        if not hours or hours not in TIME_SLOTS:
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
            
            result.append({
                "Курс": 3,
                "Группа": current_group,
                "Дата": format_date(date_obj),
                "День_недели": _weekday_ru(date_obj),
                "Часы": hours,
                "Время": TIME_SLOTS[hours],
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
    df = build_schedule()
    print("\nПервые 10 строк:")
    print(df.head(10))