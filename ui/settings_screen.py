"""
Экран настроек приложения.
"""

import flet as ft
from ui.themes import THEMES, apply_theme


def create_settings_screen(
    page,
    current_group,
    on_change_group,
    on_back,
    get_setting,
    set_setting,
    KEY_THEME,
):
    """
    Создаёт экран настроек.
    
    page — страница Flet
    current_group — текущая группа
    on_change_group — колбэк для смены группы
    on_back — колбэк возврата назад
    get_setting / set_setting — функции из user_settings
    KEY_THEME — ключ для сохранения темы
    """
    
    # Текущая тема
    current_theme = get_setting(KEY_THEME) or "dark"
    
    # Радиокнопки для тем
    theme_radios = []
    
    def on_theme_change(e):
        """При выборе темы — применяем и сохраняем."""
        selected = e.control.value
        set_setting(KEY_THEME, selected)
        apply_theme(page, selected)
    
    for theme_key, theme_data in THEMES.items():
        theme_radios.append(
            ft.Radio(
                value=theme_key,
                label=f"{theme_data['icon']}  {theme_data['name']}",
            )
        )
    
    theme_group = ft.RadioGroup(
        content=ft.Column(theme_radios, spacing=5),
        value=current_theme,
        on_change=on_theme_change,
    )
    
    # Кнопка «Назад»
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: on_back(),
    )
    
    # Кнопка «Сменить группу»
    change_group_button = ft.TextButton(
        content=f"Текущая: {current_group}  →",
        on_click=lambda e: on_change_group(),
    )
    
    # Сборка экрана
    return ft.Container(
        content=ft.Column([
            # Верхняя панель
            ft.Row([
                back_button,
                ft.Text("⚙ Настройки", size=20, weight=ft.FontWeight.BOLD, expand=True),
            ]),
            
            ft.Divider(),
            
            # Секция «Группа»
            ft.Text("Группа", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Сменить выбранную группу", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(height=5),
            change_group_button,
            
            ft.Divider(),
            
            # Секция «Тема»
            ft.Text("Тема оформления", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Выберите цветовую схему", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(height=5),
            theme_group,
            
            ft.Divider(),
            
            # Секция «О приложении»
            ft.Text("О приложении", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("VMedA.day", size=14),
            ft.Text("Версия 0.1", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text("Расписание для студентов", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
        ], scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True,
    )