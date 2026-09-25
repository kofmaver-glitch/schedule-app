"""Тестовый запуск парсера для 4 курса."""

from parser.schedule_builder import build_schedule

print("Парсинг 4 курса:")
df4 = build_schedule(
    docx_path="schedule4k.docx",
    output_path="assets/schedule_4.xlsx",
    course=4,
    specialty="ЛД",
)

print("\nПервые 10 строк:")
print(df4.head(10).to_string())