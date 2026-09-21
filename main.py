"""
Точка входа приложения.
Шаг 4: кнопка и экран расписания.
"""

import flet as ft
from datetime import date

from data.filters import get_courses, get_groups, get_schedule_for_date


def main(page: ft.Page):
    """Главная функция приложения."""
    page.title = "Расписание"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Данные из Excel ---
    courses = get_courses()
    initial_course = courses[0] if courses else None
    initial_groups = get_groups(initial_course) if initial_course else []

    # --- Выпадашка курса ---
    course_dropdown = ft.Dropdown(
        label="Курс",
        options=[ft.dropdown.Option(str(c)) for c in courses],
        value=str(initial_course) if initial_course else None,
        width=300,
    )

    # --- Выпадашка группы ---
    group_dropdown = ft.Dropdown(
        label="Группа",
        options=[ft.dropdown.Option(g) for g in initial_groups],
        value=initial_groups[0] if initial_groups else None,
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

    # --- Экран выбора ---
    def show_selection():
        content.controls.clear()

        continue_button = ft.FilledButton(
            content="Продолжить →",
            width=300,
            on_click=lambda e: show_schedule(group_dropdown.value),
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

    # --- Экран расписания ---
    def show_schedule(group: str):
        if not group:
            return

        today = date.today()
        df = get_schedule_for_date(group, today)

        content.controls.clear()

        back_button = ft.TextButton(
            content="← Назад",
            on_click=lambda e: show_selection(),
        )

        title = ft.Text(
            group,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        date_str = today.strftime("%d.%m.%Y")

        # --- Список пар ---
        if df.empty:
            pairs_list = [
                ft.Text(f"На {date_str} пар нет", color=ft.Colors.GREY_700),
            ]
        else:
            pairs_list = []
            for _, row in df.iterrows():
                # Строка с аудиторией
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
                    back_button,
                    title,
                    ft.Text(date_str, size=14, color=ft.Colors.GREY_700),
                    ft.Container(height=10),
                    *pairs_list,
                ]),
                padding=20,
            )
        )
        page.update()

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
    show_selection()


if __name__ == "__main__":
    ft.run(main)