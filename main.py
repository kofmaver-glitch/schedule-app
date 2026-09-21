"""
Точка входа приложения.
Шаг 6: выбор дня + скролл.
"""

import flet as ft
from datetime import date, timedelta

from data.filters import get_courses, get_groups, get_schedule_for_date
from data.user_settings import get_setting, set_setting, remove_setting


KEY_COURSE = "selected_course"
KEY_GROUP = "selected_group"


def main(page: ft.Page):
    """Главная функция приложения."""
    page.title = "Расписание"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Данные ---
    courses = get_courses()
    initial_course = courses[0] if courses else None

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

    def on_course_change(e):
        selected_course = int(course_dropdown.value)
        new_groups = get_groups(selected_course)
        group_dropdown.options = [ft.dropdown.Option(g) for g in new_groups]
        group_dropdown.value = new_groups[0] if new_groups else None
        page.update()

    course_dropdown.on_change = on_course_change

    # --- Контейнер ---
    content = ft.Column(expand=True)

    # --- Состояние ---
    state = {
        "current_date": date.today(),
        "group": saved_group,
    }

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
        state["group"] = group_dropdown.value
        state["current_date"] = date.today()
        show_schedule()

    # --- Смена группы ---
    def change_group():
        remove_setting(KEY_COURSE)
        remove_setting(KEY_GROUP)
        show_selection()

    # --- Навигация по датам ---
    def go_prev_day():
        state["current_date"] -= timedelta(days=1)
        show_schedule()

    def go_next_day():
        state["current_date"] += timedelta(days=1)
        show_schedule()

    def go_today():
        state["current_date"] = date.today()
        show_schedule()

    # --- Экран расписания ---
    def show_schedule():
        group = state["group"]
        if not group:
            show_selection()
            return

        target_date = state["current_date"]
        df = get_schedule_for_date(group, target_date)

        content.controls.clear()

        # --- Верхняя панель ---
        top_bar = ft.Row([
            ft.TextButton(content="←", on_click=lambda e: change_group()),
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

        # --- Дата и день недели ---
        weekday = _weekday_ru(target_date.weekday())
        date_str = target_date.strftime("%d.%m.%Y")
        is_today = target_date == date.today()

        # --- Навигация по дням ---
        date_nav = ft.Row([
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                on_click=lambda e: go_prev_day(),
            ),
            ft.Column([
                ft.Text(
                    weekday,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    date_str,
                    size=13,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                on_click=lambda e: go_next_day(),
            ),
        ])

        # --- Кнопка «Сегодня» — только если не сегодня ---
        nav_controls = [date_nav]
        if not is_today:
            nav_controls.append(
                ft.TextButton(
                    content="← Сегодня",
                    on_click=lambda e: go_today(),
                ),
            )

        # --- Список пар ---
        if df.empty:
            pairs_list = [
                ft.Container(
                    content=ft.Text("Пар нет 🎉", color=ft.Colors.GREY_700),
                    padding=20,
                ),
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
                content=ft.Column(
                    controls=[
                        top_bar,
                        ft.Container(height=5),
                        *nav_controls,
                        ft.Container(height=15),
                        *pairs_list,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=20,
                expand=True,
            )
        )
        page.update()

    # --- День недели ---
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

    if saved_group:
        state["group"] = saved_group
        show_schedule()
    else:
        show_selection()


if __name__ == "__main__":
    ft.run(main)