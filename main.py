"""
Точка входа приложения.
Шаг 5: сохранение выбора группы (через JSON-файл).
"""

import flet as ft
from datetime import date

from data.filters import get_courses, get_groups, get_schedule_for_date
from data.user_settings import get_setting, set_setting, remove_setting


# Ключи настроек
KEY_COURSE = "selected_course"
KEY_GROUP = "selected_group"


def main(page: ft.Page):
    """Главная функция приложения."""
    page.title = "Расписание"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Данные из Excel ---
    courses = get_courses()
    initial_course = courses[0] if courses else None

    # --- Читаем сохранённый выбор из файла ---
    saved_course = get_setting(KEY_COURSE)
    saved_group = get_setting(KEY_GROUP)

    if saved_course is None:
        saved_course = str(initial_course) if initial_course else None

    # --- Выпадашка курса ---
    course_dropdown = ft.Dropdown(
        label="Курс",
        options=[ft.dropdown.Option(str(c)) for c in courses],
        value=str(saved_course) if saved_course else None,
        width=300,
    )

    # --- Выпадашка группы ---
    current_groups = get_groups(int(saved_course)) if saved_course else []
    group_dropdown = ft.Dropdown(
        label="Группа",
        options=[ft.dropdown.Option(g) for g in current_groups],
        value=saved_group if saved_group in current_groups else (current_groups[0] if current_groups else None),
        width=300,
    )

    # --- Обновление групп при смене курса ---
    def on_course_change(e):
        selected_course = int(course_dropdown.value)
        new_groups = get_groups(selected_course)
        group_dropdown.options = [ft.dropdown.Option(g) for g in new_groups]
        group_dropdown.value = new_groups[0] if new_groups else None
        page.update()

    course_dropdown.on_change = on_course_change

    # --- Контейнер для содержимого ---
    content = ft.Column()

    # --- Сохранение выбора ---
    def save_selection():
        set_setting(KEY_COURSE, course_dropdown.value)
        set_setting(KEY_GROUP, group_dropdown.value)

    # --- Экран выбора ---
    def show_selection():
        content.controls.clear()

        continue_button = ft.FilledButton(
            content="Продолжить →",
            width=300,
            on_click=lambda e: on_continue(),
        )

        content.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Выберите группу", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    course_dropdown,
                    group_dropdown,
                    ft.Container(height=20),
                    continue_button,
                ]),
                padding=20,
            )
        )
        page.update()

    # --- Обработка «Продолжить» ---
    def on_continue():
        save_selection()
        show_schedule(group_dropdown.value)

    # --- Смена группы ---
    def change_group():
        remove_setting(KEY_COURSE)
        remove_setting(KEY_GROUP)
        show_selection()

    # --- Экран расписания ---
    def show_schedule(group: str):
        if not group:
            show_selection()
            return

        today = date.today()
        df = get_schedule_for_date(group, today)

        content.controls.clear()

        # --- Верхняя панель: назад / группа / ⚙ ---
        top_bar = ft.Row([
            ft.TextButton(
                content="←",
                on_click=lambda e: change_group(),
            ),
            ft.Text(
                group,
                size=18,
                weight=ft.FontWeight.BOLD,
                expand=True,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                on_click=lambda e: change_group(),
            ),
        ])

        # --- Дата ---
        date_str = today.strftime("%d.%m.%Y")
        weekday = _weekday_ru(today.weekday())

        # --- Список пар ---
        if df.empty:
            pairs_list = [
                ft.Text(f"На {date_str} пар нет", color=ft.Colors.GREY_700),
            ]
        else:
            pairs_list = []
            for _, row in df.iterrows():
                if row["Аудитория"]:
                    aud_text = f"Ауд. {row['Аудитория']}"
                else:
                    aud_text = "—"

                pairs_list.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"{row['Время']}  •  {row['Тип']}",
                                size=12,
                                color=ft.Colors.GREY_700,
                            ),
                            ft.Text(
                                row["Предмет"],
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(aud_text, size=13),
                        ]),
                        padding=12,
                        bgcolor=ft.Colors.GREY_100,
                        border_radius=10,
                    )
                )

        content.controls.append(
            ft.Container(
                content=ft.Column([
                    top_bar,
                    ft.Text(f"{weekday}, {date_str}", size=14, color=ft.Colors.GREY_700),
                    ft.Container(height=10),
                    *pairs_list,
                ]),
                padding=20,
            )
        )
        page.update()

    # --- День недели по-русски ---
    def _weekday_ru(weekday: int) -> str:
        days = ["Понедельник", "Вторник", "Среда", "Четверг",
                "Пятница", "Суббота", "Воскресенье"]
        return days[weekday]

    # --- Заголовок ---
    header = ft.Container(
        content=ft.Column([
            ft.Text("📅 Расписание", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("ВМедА им. С.М. Кирова", size=14, color=ft.Colors.GREY_700),
        ]),
        padding=20,
    )

    # --- Сборка ---
    page.add(header, content)

    # --- Что показать при запуске? ---
    if saved_group:
        show_schedule(saved_group)
    else:
        show_selection()


if __name__ == "__main__":
    ft.run(main)